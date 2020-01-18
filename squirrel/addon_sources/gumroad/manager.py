import asyncio

from pathlib import Path

import aiohttp

import requests
# from requests_html import HTMLSession


from loguru import logger
from lxml import html
import json

from squirrel.addon_sources.website import WebsiteSource

from squirrel.addon_sources.debug import debug_html_request
from .product import GumroadProduct


class GumroadProducts():
    ''' Manager class for handling gumroad addons. '''

    __slots__ = (
        '__products_list',
        'aiohttp_session',
        'debug_html_requests',
        'event_loop',
        'product_search_query',
        'url',
        'website_source',
    )

    def __init__(
        self,
        url='https://gumroad.com/library',
        session_cookie_domain='gumroad.com',
        debug_html_requests=False,
        product_search_query='https://gumroad.com/discover_search?from=1&user_purchases_only=true'
    ):
        self.url = url
        self.product_search_query = product_search_query
        self.__products_list = []
        self.event_loop = asyncio.get_event_loop()
        self.website_source = WebsiteSource(
            session_cookie_domain=session_cookie_domain,
            login_url=url
        )
        self.aiohttp_session = None
        self.debug_html_requests = debug_html_requests

    def list(self, force_reload=False):
        ''' Wrapper for listing products to cache its content '''

        if self.__products_list == [] or force_reload is True:
            # Use one event loop
            loop = self.event_loop

            # Run the async function and list all products
            self.__products_list = loop.run_until_complete(
                self.__list_products()
            )

        return self.__products_list

    async def __list_products(self):
        ''' Lists all available gumroad products. '''

        logger.info("Loading gumroad products")
        products = []
        library_tree_url = self.url
        aiohttp_cookies = self.website_source.aiohttp_session_cookies

        # Create an aiohttp_session with required cookies. Don't forget to close later.
        self.aiohttp_session = aiohttp.ClientSession(cookies=aiohttp_cookies)

        # Check if there is an existing gumroad session to use.
        if self.website_source.session_cookies is None:
            self.website_source.login()

        logger.debug("Using existing browser session")

        if len(aiohttp_cookies) == 0:
            raise NotImplementedError(
                'No session cookies found. Login not successfull?')

        library_html_response = await self.aiohttp_session.get(library_tree_url)
        library_tree = html.fromstring(await library_html_response.text())

        # Save the generated HTML file for debug purposes
        if self.debug_html_requests:
            debug_html_request(filename='library_html', html_data=html.tostring(
                library_tree, pretty_print=True))

        # FIXME: Due to the fact, that Gumroad changed it
        search_response_for_library_products = await self.aiohttp_session.get(self.product_search_query)
        library_products_data = json.loads(await search_response_for_library_products.text())
        products_html = html.fromstring(library_products_data["products_html"])

        # Save the generated HTML file for debug purposes
        if self.debug_html_requests:
            debug_html_request(
                filename='library_json',
                html_data=html.tostring(products_html, pretty_print=True)
            )

        # Extract all library product elements (and filter out the parent library-products element)
        library_products = [
            element
            for element in products_html.xpath("//div[contains(@class, 'library-product')]")
            if 'library-products' not in element.attrib['class']
        ]

        logger.debug(f"Found library_products: {library_products}")

        # Fill the products list with informations
        for library_product in library_products:
            # Gumroad Product Name
            product_name = library_product.xpath(
                "*//h1[@itemprop='name']/strong/text()")[0]
            # logger.debug("product_name: " + product_name)

            # Gumroad Product URL
            data_id = library_product.attrib['data-purchase-id']
            product_url = f'https://gumroad.com/library/purchases/{data_id}'
            # logger.debug("product_url: " + product_url)

            product_object = GumroadProduct(
                name=product_name, url=product_url, products_manager=self)
            product_object.html_element = library_product

            products.append(product_object)

        # Prefetch download links
        # Gather is required for ... reasons. Otherwise everything will be executed in sequence (syncron).
        await asyncio.gather(*(product._fetch_download_links() for product in products))

        await self.aiohttp_session.close()
        return products

    def __repr__(self):
        return f"GumroadProductsManager(url={self.url})"
