"""
Tenshi Discord Bot
Copyright (C) 2021 Ben Z.
This software is licensed under Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)
"""


import aiohttp
import os


param_dict = {
    ""
}



async def unsplash_photo(type, data):
    """Move to class"""
    if str.lower(type) in ["id"]:
        url_string = f"/photos/?{data}&"

    if str.lower(type) in ["search"]:
        url_string = "/search/photos/?"
        for item in data:
            parameter = item.split("=", 1)
            if str.lower(parameter[0]) in ["search", "s", "query"]:
                url_string = url_string+f"query={parameter[1]}&"
            elif str.lower(parameter[0]) in ["order", "orderby", "ob"]:
                url_string = url_string+f"order_by={parameter[1]}&"
            elif str.lower(parameter[0]) in ["orentation", "o"]:
                url_string = url_string+f"orientation={parameter[1]}&"
            elif str.lower(parameter[0]) in ["color", "c"]:
                url_string = url_string+f"color={parameter[1]}&"

    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.unsplash.com{url_string}client_id={os.getenv('UnsplashToken')}") as request:
            return await request.json()

class Unsplash():
    """Accessing stuff about Unsplash"""
    def __init__(self):
        self.client_id = os.getenv("UnsplashToken")
        self.client_string = f"?client_id={self.client_id}"
        self.latest_header = None
        self.api_url = "https://api.unsplash.com"

    """Cache for latest save data from unsplash NOT FINISHED"""
    async def set_latest_header(self, header):
        """Set the latest header"""
        self.latest_header = header

    async def get_ratelimit_remaining(self):
        """Get rate limit remaining on requests"""
        return self.latest_header.get("X-Ratelimit-Remaining", -1)

    """Regular methods"""
    async def get_random_photo(self, params: dict={}):
        """Get a completely random photo from unsplash"""
        request_string = await self.to_url(params)
        return await self.request_url(f"""{self.api_url}/photos/random/{request_string}""")

    async def get_photo_by_id(self, photo_id: str):
        """Get a photo by its id"""
        return await self.request_url(f"""{self.api_url}/photos/{photo_id}/{self.client_string}""")

    async def get_user_profile(self, username: str):
        """Return a public users profile information"""
        return await self.request_url(f"""{self.api_url}/users/{username}/{self.client_string}""")
    
    async def get_user_portfolio(self, username: str):
        """Return a public users portfolio link"""
        return await self.request_url(f"""{self.api_url}/users/{username}/portfolio/{self.client_string}""")

    async def get_user_photos(self, username: str, params: dict):
        """Returns a list of all the users photos"""
        request_url = await self.to_url(params)
        return await self.request_url(f"""{self.api_url}/users/{username}/photos/{request_url}""")

    async def get_user_liked_photos(self, username: str, params: dict):
        """Returns a list of all the photos a user has liked"""
        request_url = await self.to_url(params)
        return await self.request_url(f"""{self.api_url}/users/{username}/likes/{request_url}""")

    async def get_user_collections(self, username: str, params: dict):
        """Returns a list of all the collections a user has made"""
        request_url = await self.to_url(params)
        return await self.request_url(f"""{self.api_url}/users/{username}/collections/{request_url}""")

    async def get_user_statistics(self, username: str, params: dict):
        """Return a users statistics"""
        request_url = await self.to_url(params)
        return await self.request_url(f"""{self.api_url}/users/{username}/statistics/{request_url}""")



    # Requesting stuff
    async def to_url(self, dictionary: dict):
        """Create a url string based off dict"""
        if not dictionary:
            url_link = "?"
        if len(dictionary) == 1:
            url_link = f"?{dictionary.keys()[0]}={dictionary[dictionary.keys()[0]]}"
        elif len(dictionary) >= 2:
            url_link = f"?{dictionary.keys()[0]}={dictionary[dictionary.keys()[0]]}"
            value = 0
            for param in dictionary.keys():
                if value == 0:
                    value = 1
                else:
                    url_link = url_link + f"&{param}={dictionary[param]}&"

        return url_link + "client_id=" + self.client_id

    async def request_url(self, url):
        """Get a url and update latest header"""
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as request:
                await self.set_latest_header(request.headers)
                return await request.json()

    async def get_param(self, method):
        """Return possible parameters from methods"""



unsplash_client = Unsplash()