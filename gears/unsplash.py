"""
Tenshi Discord Bot
Copyright (C) 2021 Ben Z.
This software is licensed under Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)
"""


import datetime
import aiohttp
import os


class UnsplashCache:
    """Cache for latest save data from unsplash NOT FINISHED"""
    async def set_latest_header(self, header):
        self.latest_header = header

    async def get_latest_header(self):
        return self.header

unsplash_cache = UnsplashCache()

async def unsplash_random():
    """Get a random photo from Unsplash"""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"""https://api.unsplash.com/photos/random/?client_id={os.getenv("UnsplashToken")}""") as request:
            await unsplash_cache.set_latest_header(request.headers)
            return await request.json()
    
async def unsplash_photo(type, data):
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
    