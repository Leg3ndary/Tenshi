"""
Tenshi Discord Bot
Copyright (C) 2021 Ben Z.
This software is licensed under Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)
"""

import discord
from discord.ext import commands
import datetime
from colors import *
import aioredis
import os


class Redis(commands.Cog):
    """Redis DB related stuff """
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.redis = await aioredis.from_url(f"""redis://{os.getenv("RedisUser")}:{os.getenv("RedisPass")}@localhost/""")
    
    @commands.command()
    async def testt(self, ctx):
        await self.bot.redis.set("my-key", "it worked loser")
        value = await self.bot.redis.get("my-key")
        await ctx.send(value)
    
    @commands.command()
    async def redis(self, ctx):
        """Access stuff about redis"""

def setup(bot):
    bot.add_cog(Redis(bot))