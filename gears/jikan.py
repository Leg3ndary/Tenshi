"""
Tenshi Discord Bot
Copyright (C) 2021 Ben Z.
This software is licensed under Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)
"""

import aiohttp
import datetime

class JikanGear():
    """Jikan Class that we use as a "gear" :D"""
    def __init__(self):
        self.api_url = "https://api.jikan.moe/v4"
    
    """Important Methods"""
    async def request_url(self, url: str):
        """Request a url from the API"""
        async with aiohttp.ClientSession() as jikan_session:
            async with jikan_session.get(f"https://api.jikan.moe/v4{url}") as request:
                if request.status in [200]:
                    pass
                else:
                    print(f"[ERROR] [{datetime.datetime.utcnow()}]\nError Code: {request.status}\n{await request.json()}")
                return await request.json()

    async def get_anime_by_id(self, id: str):
        """Return an anime by its ID"""
        return await self.request_url(f"/anime/{id}")







    """Old methods that need to be fixed"""
    async def get_user(username: str):
        """Get a users profile"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://api.jikan.moe/v4/users/{username}") as request:
                if request.status in [200, 404]:
                    return await request.json()
                else:
                    print(f"[ERROR] [{datetime.datetime.utcnow()}]\nError Code: {request.status}\n{await request.json()}")
                    return None

    async def get_anime(id):
        """Retrieve an anime by its given ID"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://api.jikan.moe/v4/anime/{id}") as request:
                if request.status == 200:
                    return await request.json()
                else:
                    print(f"[ERROR] [{datetime.datetime.utcnow()}]\nError Code: {request.status}\n{await request.json()}")
                    return None

    async def get_user_stats(username):
        """Retrieve an anime by its given ID"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://api.jikan.moe/v4/users/{username}/statistics") as request:
                if request.status == 200:
                    return await request.json()
                else:
                    print(f"[ERROR] [{datetime.datetime.utcnow()}]\nError Code: {request.status}\n{await request.json()}")
                    return None

    async def search_user(user):
        """Just search for a regular anime with a string"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://api.jikan.moe/v4/users?q={user}") as request:
                if request.status in [200, 404]:
                    return await request.json()
                else:
                    print(f"[ERROR] [{datetime.datetime.utcnow()}]\nError Code: {request.status}\n{await request.json()}")
                    return None

    async def search_anime(anime):
        """Search for a user"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://api.jikan.moe/v4/anime?q={anime}") as request:
                if request.status == 200:
                    return await request.json()
                else:
                    print(f"[ERROR] [{datetime.datetime.utcnow()}]\nError Code: {request.status}\n{await request.json()}")
                    return None

    async def anime_characters(anime):
        """Not finished"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://api.jikan.moe/v4/anime?q={anime}") as request:
                if request.status == 200:
                    return await request.json()
                else:
                    print(f"[ERROR] [{datetime.datetime.utcnow()}]\nError Code: {request.status}\n{await request.json()}")
                    return None

    async def get_user_updates(username):
        """Not finished"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://api.jikan.moe/v4/users/{username}/userupdates") as request:
                if request.status == 200:
                    return await request.json()
                else:
                    print(f"[ERROR] [{datetime.datetime.utcnow()}]\nError Code: {request.status}\n{await request.json()}")
                    return None

class TraceMoe():
    async def get_anime_picture(image_url):
        """Use trace.moe to try and trace the images origins"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://trace.moe/api/search?url={image_url}") as request:
                if request.status == 200:
                    return await request.json()
                else:
                    print(f"[ERROR] [{datetime.datetime.utcnow()}]\nError Code: {request.status}\n{await request.json()}")
                    return None
