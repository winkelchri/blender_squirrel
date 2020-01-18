import asyncio

from pathlib import Path
from datetime import datetime

import aiohttp

import requests
# from requests_html import HTMLSession


from bs4 import BeautifulSoup
from loguru import logger
from lxml import html
import json

from squirrel.addon_sources.website import WebsiteSource

from loguru import logger


class GumroadProduct():
    ''' Class for the actual gumroad product. '''

    __slots__ = (
        'name',
        'url',
        'products_manager',
        'html_element',
        'event_loop',
        '__download_links'
    )

    def __init__(self, name, url, products_manager):
        self.name = name
        self.url = url
        self.products_manager = products_manager
        self.html_element = None
        self.event_loop = products_manager.event_loop
        self.__download_links = None

    @property
    def cookiejar(self):
        return self.products_manager.cookiejar

    @property
    def download_links(self):
        ''' Returns the download links of the given product url. '''

        if self.__download_links is None:
            pass

        return self.__download_links

    async def _fetch_download_links(self):
        ''' Async function to get all download links. '''

        aiohttp_session = self.products_manager.aiohttp_session

        # New request towards the product url to receive the download link
        product_url_response = await aiohttp_session.get(self.url)
        product_tree = html.fromstring(await product_url_response.text())

        # Product download link
        download_site_url = product_tree.xpath(
            "*//a[contains(@class, 'download')]")[0].attrib['href']
        logger.info(
            f"Listing download links for '{self.name}': {download_site_url}")

        # Download link content
        download_site_response = await aiohttp_session.get(download_site_url)

        # Some links already returning a ZIP file instead of a download page
        if download_site_response.content_type == 'application/zip':
            logger.warning(f'{download_site_url} is already a ZIP file')
            return

        download_site_tree = html.fromstring(await download_site_response.read())

        download_link_rows = download_site_tree.xpath(
            "//li[contains(@class, 'file-row-container')]")
        # logger.debug(download_link_rows)

        for row in download_link_rows:

            # LINK TEXT
            # $x("//div[contains(@class, 'file-row-left')]/span/text()");
            link_text = row.xpath(
                "*//div[contains(@class, 'file-row-left')]/span/text()")[0]
            logger.debug(f"link_text: {link_text}")

            # LINK URL
            # $x("//button[text()='Download']");
            # Get the data-url of the download button ...
            download_button = row.xpath("//button[text()='Download']")[0]
            download_button_data_url = download_button.attrib['data-url']

            # ... to receive the url to request the actual download link ...
            link_request_url = f"https://gumroad.com{download_button_data_url}"
            logger.debug(f"link_request_url: {link_request_url} ")

            # ... and make a request to this url ...
            head = await aiohttp_session.head(link_request_url, allow_redirects=True)
            logger.debug(head.headers)
            # download_link_response = requests.get(link_request_url, cookies=self.cookiejar)

            # logger.debug(download_link_response.content)
            # logger.debug(f"response headers: {download_link_response.headers}")
            # actual_download_link = download_link_response.headers.get('location')

            '''
            <button
                class="button-default button-small js-download-trigger js-track-click-event"
                data-event-name="download_click"
                data-url="/r/3796d83deb25466b1add5b9dfc5d6f63/lPbJ__J0F78QjC5gJLjVyQ==">
                Download
            </button>
            '''
            # ... the actual link should be in the header of the response:
            # logger.debug(f"actual download link: {actual_download_link}")

        # class = "product library-product relative js-product"

    def __repr__(self):
        return f'GumroadProduct(name="{self.name}", url="{self.url}")'
