import webbrowser
from http.cookies import CookieError, Morsel, SimpleCookie

import browser_cookie3
from loguru import logger

import aiohttp


class WebsiteSource():
    ''' Class for handling logins to a website and reusing existing login data. '''

    def __init__(self, session_cookie_domain, login_url):
        '''

        Args:
            session_cookie_domain (str): Name of the domain the cookies are stored for.
        '''

        # FIXME: It might be possible, that a session was found but not useable.
        #        Unfortunately no errors captured last time and after new login
        #        the plugin worked again.

        self.login_url = login_url
        self.session_cookie_domain = session_cookie_domain
        self.__host_cookiejar = None
        self.__session_id = None
        self.__session_cookies = None

    @property
    def session_cookies(self):
        ''' Returns all cookies with the given session_cookie_domain
            of the host_cookiejar (all stored logins on the hosts browser)
        '''

        if self.__session_cookies is None:
            self.__session_cookies = [
                cookie
                for cookie in self.host_cookiejar
                if self.session_cookie_domain in cookie.domain
            ]
        return self.__session_cookies

    @property
    def aiohttp_session_cookies(self):
        ''' Returns an aiohttp compatible list of relevant session cookies. '''

        output_cookie = SimpleCookie()

        for cookie in self.session_cookies:
            converted_cookie = self.cookiejar_cookie_to_simplecookie(cookie)
            output_cookie.update(converted_cookie)
        return output_cookie

    @property
    def session_id(self):
        ''' Returns the first session id of the
            existing session cookies.
        '''

        if self.__session_id is None and len(self.session_cookies) > 0:
            self.__session_id = self.session_cookies[0].value

        return self.__session_id

    @property
    def host_cookiejar(self):
        ''' Whole cookie jar of the hosts browser. Don't use it as a whole
            but only use what you need.
        '''

        if self.__host_cookiejar is None:
            self.__host_cookiejar = browser_cookie3.load()
        return self.__host_cookiejar

    def cookiejar_cookie_to_simplecookie(self, cookie):
        ''' Takes a http.cookiejar.Cookie object and returns a http.cookies.SimpleCookie object. '''

        simplecookie = SimpleCookie()
        simplecookie[cookie.name] = cookie.value
        simplecookie[cookie.name]["path"] = cookie.path
        simplecookie[cookie.name]["expires"] = str(cookie.expires)
        simplecookie[cookie.name]["domain"] = str(cookie.domain)
        return simplecookie

    def login(self):
        logger.info('Open browser for login and creating a session cookie')

        webbrowser.open(self.login_url)

        while True:
            if self.session_id is None:
                return

    async def fetch(self, session, url):
        ''' Fetch method to be used in conjunction with an existing aiohttp session. '''

        # https://aiohttp.readthedocs.io/en/stable/
        async with session.get(url) as response:
            return await response.text()
