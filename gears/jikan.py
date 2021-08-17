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
        self.header_data = []
        self.header_data_limit = 25
    
    """Important Methods"""
    async def request_url(self, url: str, parameters=""):
        """Request a url from the API"""
        async with self.aiohttp_session as session:
            async with session.get(f"https://api.jikan.moe/v4{url}{await self.to_url(parameters)}") as request:
                if request.status in [200, 400]:
                    pass
                else:
                    print(f"[ERROR] [{datetime.datetime.utcnow()}]\nError Code: {request.status}\n{await request.json()}")
                try:
                    await self.append_header(request.headers)
                except:
                    pass
                return await request.json()

    async def view_headers(self, header=None):
        """View header info, if None return all data on hand"""
        if not header:
            return self.header_data
        
        else:
            return self.header_data.get(header)

    async def append_header(self, header):
        """Add a header to our small database"""
        self.header_data = self.header_data[:self.header_data_limit - 1].append(header)

    async def to_url(self, dictionary: dict):
        """Create a url string based off dict"""
        if not dictionary:
            url_link = ""
        if len(dictionary) == 1:
            url_link = f"?{list(dictionary.keys())[0]}={dictionary[list(dictionary.keys())[0]]}"
        elif len(dictionary) >= 2:
            url_link = f"?{list(dictionary.keys())[0]}={dictionary[list(dictionary.keys())[0]]}"
            value = 0
            for param in dictionary.keys():
                if value == 0:
                    value = 1
                else:
                    url_link = url_link + f"&{param}={dictionary[param]}"
        return url_link

    """Anime methods"""
    async def get_anime_by_id(self, id: str):
        """Get an anime by its ID
        \nNo Params"""
        return await self.request_url(f"/anime/{id}")

    async def get_anime_characters(self, id: str):
        """Get a list of anime characters from an anime
        \nNo Params"""
        return await self.request_url(f"/anime/{id}/characters")

    async def get_anime_staff(self, id: str):
        """Get an animes staff
        \nNo Params"""
        return await self.request_url(f"/anime/{id}/staff")

    async def get_anime_episodes(self, id: str, parameters=""):
        """Get a list of an animes planned/current episodes
        \npage - int"""
        return await self.request_url(f"/anime/{id}/episodes", parameters)
    
    async def get_anime_episodes_by_id(self, id: str, episode: str):
        """Return a current episodes info with anime id and episode num
        \nNo Params"""
        return await self.request_url(f"/anime/{id}/episodes/{episode}")
    
    async def get_anime_news(self, id: str, parameters=""):
        """Get an animes current news
        \npage - int"""
        return await self.request_url(f"/anime/{id}/news", parameters)

    async def get_anime_forum(self, id: str, parameters=""):
        """Get an animes current forums
        \ntopic - all, episode or other"""
        return await self.request_url(f"/anime/{id}/forum", parameters)

    async def get_anime_videos(self, id: str):
        """Get an animes related videos
        \nNo Params"""
        return await self.request_url(f"/anime/{id}/videos")

    async def get_anime_pictures(self, id: str):
        """Get an animes related pictures
        \nNo Params"""
        return await self.request_url(f"/anime/{id}/pictures")

    async def get_anime_statistics(self, id: str):
        """Get an animes statistics
        \nNo Params"""
        return await self.request_url(f"/anime/{id}/statistics")

    async def get_anime_more_info(self, id: str):
        """Get more info about an anime
        \nNo Params"""
        return await self.request_url(f"/anime/{id}/moreinfo")

    async def get_anime_recommendations(self, id: str):
        """Get an animes recommendations from other users
        \nNo Params"""
        return await self.request_url(f"/anime/{id}/recommendations")

    async def get_anime_user_updates(self, id: str, parameters=""):
        """Get a list of users who have updated something related to anime
        \npage - int"""
        return await self.request_url(f"/anime/{id}/userupdates", parameters)

    async def get_anime_reviews(self, id: str, parameters=""):
        """Get an animes reviews
        \npage - int"""
        return await self.request_url(f"/anime/{id}/reviews", parameters)

    async def get_anime_relations(self, id: str):
        """Get a list of related animes, eg adapation, side story
        \nNo Params"""
        return await self.request_url(f"/anime/{id}/relations")

    async def get_anime_themes(self, id: str):
        """Get an animes themes (Seems to be music)
        \nNo Params"""
        return await self.request_url(f"/anime/{id}/themes")

    async def get_anime_search(self, parameters):
        """Literally search for an anime :L
        \npage - int
        \nlimit - int
        \nq - Search string
        \ntype - tv, movie, ova, special, ona or music
        \nscore - 0 to 10
        \nstatus - airing, complete or upcoming
        \nrating - g, pg, pg13, r17, r or rx
        \nsfw - boolean
        \ngenres - pass multiple with comma separation
        \norder_by - mal_id, title, type, rating, start_date, end_date, episodes, score, scored_by, rank, popularity, member, favorites
        \nsort - desc or asc
        \nletter - singular letter matching
        \nproducer - use producer id"""
        return await self.request_url(f"/anime", parameters)

    """Character Methods"""
    async def get_character_by_id(self, id: str):
        """Get a character by its id
        \nNo Params"""
        return await self.request_url(f"/characters/{id}")

    async def get_character_anime(self, id: str):
        """Get a characters anime and what role he plays in it
        \nNo Params"""
        return await self.request_url(f"/characters/{id}/anime")
    
    async def get_character_manga(self, id: str):
        """Get a characters manga, basically anime
        \nNo Params"""
        return await self.request_url(f"/characters/{id}/manga")

    async def get_character_voice_actors(self, id: str):
        """Get a character voice actors
        \nNo Params"""
        return await self.request_url(f"/characters/{id}/voices")

    async def get_character_pictures(self, id: str):
        """Get some images of a character
        \nNo Params"""
        return await self.request_url(f"/characters/{id}/pictures")

    async def get_character_search(self, parameters):
        """Get a character
        \npage - int
        \nlimit - int
        \nq - Search string
        \norder_by - mal_id, name or favorites
        \nsort - desc or asc
        \nletter - singular letter matching"""
        return await self.request_url(f"/characters", parameters)




    """Old methods that need to be fixed"""
    async def get_user(self, username: str):
        """Get a users profile"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://api.jikan.moe/v4/users/{username}") as request:
                if request.status in [200, 404]:
                    return await request.json()
                else:
                    print(f"[ERROR] [{datetime.datetime.utcnow()}]\nError Code: {request.status}\n{await request.json()}")
                    return None


    async def get_user_stats(self, username):
        """Retrieve an anime by its given ID"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://api.jikan.moe/v4/users/{username}/statistics") as request:
                if request.status == 200:
                    return await request.json()
                else:
                    print(f"[ERROR] [{datetime.datetime.utcnow()}]\nError Code: {request.status}\n{await request.json()}")
                    return None

    async def search_user(self, user):
        """Just search for a regular anime with a string"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://api.jikan.moe/v4/users?q={user}") as request:
                if request.status in [200, 404]:
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