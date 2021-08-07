"""
Tenshi Discord Bot
Copyright (C) 2021 Ben Z.
This software is licensed under Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)
"""

import discord
from discord.ext import commands
import datetime as dt
import random as rnd
import aiohttp
import json
from gears.cosmetics import *

async def trivia_request(question_amount, category, difficulty, type):
    request_string = ""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://opentdb.com/api.php/") as request:
            return(json.loads(await request.text()))

async def trivia_info(info):
    if info.lower() in ['category']:
        url_string = "https://opentdb.com/api_category.php"
    
    elif info in [1, 2 ]:
        url_string = "https://opentdb.com/api_count.php?category="

    elif info.lower() in ['global']:
        url_string = "https://opentdb.com/api_count_global.php"

    async with aiohttp.ClientSession() as session:
        async with session.get(url_string) as request:
            return(json.loads(await request.text()))

def random_hex():
    random_number = rnd.randint(0,0xffffff)
    return(random_number)
    
class Trivia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(3.0, 10.0, commands.BucketType.user)
    async def trivia(self, ctx):
        embed = discord.Embed(
            title="",
            description="",
            timestamp=dt.datetime.utcnow(),
            color=random_hex()
        )
        return await ctx.send()
        

    @commands.command(aliases=['trueorfalse'])
    @commands.cooldown(3.0, 10.0, commands.BucketType.user)
    async def tof(self, ctx):
        pass
    @commands.command()
    @commands.cooldown(1.0, 10.0, commands.BucketType.user)
    async def triviadb():
        pass

    @triviadb.error()
    async def triviadb_error(self, ctx, error):
        pass
# Adding the Cog
def setup(bot):
    bot.add_cog(Trivia(bot))