"""
Tenshi Discord Bot
Copyright (C) 2021 Ben Z.
This software is licensed under Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)
"""

import aiohttp
import datetime
import motor.motor_asyncio
import os

# Kinda obscure so not adding it to the cosmetics gear
coc_emojis = {
    "exp": "<:coc_exp:875929083899428884>",
    "trophym": "<:coc_trophym:875932452886048858>",
    "star": "<:star:876212642363101284>",
    "sword": "<:sword:876295641377148978>",
    "shield": "<:shield:876294810422616065>",
}

class CocClient():
    """Clash of clans Class that we use as a "gear" :D"""
    def __init__(self):
        self.token = os.getenv("CocToken")
        self.header = {"Authorization":f"Bearer {self.token}"}
        self.api_url = "https://api.clashofclans.com/v1"
        self.supercell_motor = motor.motor_asyncio.AsyncIOMotorClient(
            f"""mongodb+srv://{os.getenv("SupercellUser")}:{os.getenv("SupercellPass")}@supercell.hlwji.mongodb.net/coc?retryWrites=true&w=majority"""
        )
        self.coc = self.supercell_motor["coc"]
        self.users = self.coc["users"]
    
    """Important Methods"""
    async def request_url(self, url: str, parameters=""):
        """Request a url from the API"""
        async with aiohttp.ClientSession(headers=self.header) as session:
            async with session.get(f"{self.api_url}{url}{await self.to_url(parameters)}") as request:
                if request.status in [200, 404]:
                    pass
                else:
                    print(f"[ERROR] [{datetime.datetime.utcnow()}]\nError Code: {request.status}\n{await request.json()}")
                final = await request.json()
                final.update({"/request-status":request.status})
                return final

    async def verify_account(self):
        """Verifying an account with a post request"""

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

    """Player methods"""
    async def get_player(self, tag: str):
        """Get a player by their tag
        \nNo Params"""
        return await self.request_url(f"/players/{tag}")