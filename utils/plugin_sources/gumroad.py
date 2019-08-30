from loguru import logger
import webbrowser
import browser_cookie3
import requests
import pathlib

from lxml import html
from bs4 import BeautifulSoup


class GumroadProducts():
    ''' Manager class for handling gumroad plugins. '''

    def __init__(self, url='https://gumroad.com/library'):
        self.url = url
        self.__cookiejar = None
        self.__session = None
        self.__products_list = []

    @property
    def cookiejar(self):
        if self.__cookiejar is None:
            self.__cookiejar = browser_cookie3.load()
        return self.__cookiejar

    @property
    def session(self):
        if self.__session is None:
            for cookie in self.cookiejar:

                if cookie.name == '_gumroad_guid':
                    self.__session = cookie.value
                    logger.info(self.__session)

        return self.__session

    def login(self):
        logger.info('Open browser for login into gumroad')

        webbrowser.open(self.url)

        while True:
            if self.session is None:
                return

    def list(self, force_reload=False):
        ''' Wrapper for listing products to cache its content '''

        if self.__products_list == [] or force_reload is True:
            self.__products_list = self.__list_products()
        return self.__products_list

    def __list_products(self):
        ''' Lists all available gumroad products. '''

        logger.info("Loading gumroad products")
        products = []

        # Check if there is an existing gumroad session to use.
        if self.session is None:
            self.login()

        library_response = requests.get(self.url, cookies=self.cookiejar)
        library_tree = html.fromstring(library_response.content)

        # Extract all library product elements (and filter out the parent library-products element)
        library_products = [
            element
            for element in library_tree.xpath("//div[contains(@class, 'library-product')]")
            if 'library-products' not in element.attrib['class']
        ]

        # Fill the products list with informations
        for library_product in library_products:
            # Gumroad Product Name
            product_name = library_product.xpath("*//h1[@itemprop='name']/strong/text()")[0]
            # logger.debug("product_name: " + product_name)

            # Gumroad Product URL
            data_id = library_product.attrib['data-id']
            product_url = f'https://gumroad.com/library/purchases/{data_id}'
            # logger.debug("product_url: " + product_url)

            product_object = GumroadProduct(name=product_name, url=product_url, products_manager=self)
            product_object.html_element = library_product

            products.append(product_object)

        return products

    def __repr__(self):
        return f"GumroadProducts(url={self.url})"


class GumroadProduct():
    def __init__(self, name, url, products_manager):
        self.name = name
        self.url = url
        self.products_manager = products_manager
        self.html_element = None

    @property
    def cookiejar(self):
        return self.products_manager.cookiejar

    @property
    def download_links(self):
        ''' Returns the download links of the given product url. '''

        links = []

        if self.products_manager.session is None:
            self.products_manager.login()

        # New request towards the product url to receive the download link
        product_url_response = requests.get(self.url, cookies=self.cookiejar)
        product_tree = html.fromstring(product_url_response.content)

        # Product download link
        download_site_url = product_tree.xpath(
            "*//a[contains(@class, 'download')]")[0].attrib['href']
        logger.info(f"Listing download links for '{self.name}': {download_site_url}")

        # Download link content
        download_site = requests.get(download_site_url, cookies=self.cookiejar)
        download_site_tree = html.fromstring(download_site.content)

        download_link_rows = download_site_tree.xpath("//li[contains(@class, 'file-row-container')]")
        # logger.debug(download_link_rows)

        for row in download_link_rows:

            # LINK TEXT
            # $x("//div[contains(@class, 'file-row-left')]/span/text()");
            link_text = row.xpath("*//div[contains(@class, 'file-row-left')]/span/text()")[0]
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
            head = requests.head(link_request_url, allow_redirects=True)
            logger.debug(head.headers)
            # download_link_response = requests.get(link_request_url, cookies=self.cookiejar)

            # logger.debug(download_link_response.content)
            # logger.debug(f"response headers: {download_link_response.headers}")
            # actual_download_link = download_link_response.headers.get('location')

            # <button class = "button-default button-small js-download-trigger js-track-click-event" data-event-name = "download_click" data-url = "/r/3796d83deb25466b1add5b9dfc5d6f63/lPbJ__J0F78QjC5gJLjVyQ==" > Download < /button >

            # ... the actual link should be in the header of the response:
            # logger.debug(f"actual download link: {actual_download_link}")



        # class = "product library-product relative js-product"

    def __repr__(self):
        return f'GumroadProduct(name="{self.name}", url="{self.url}")'
