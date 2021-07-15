"""
Tenshi Discord Bot
Copyright (C) 2021 Ben Z.
This software is licensed under Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)
"""

import discord
from discord.ext import commands
import datetime
from cogs.colors import *
import aioredis
import os
import time


"""
await self.bot.redis.set("Key", "Data") Set a key
value = await self.bot.redis.get("Key")
"""


class Redis(commands.Cog):
    """Redis DB related stuff """
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """Connect to our Redis DB"""
        start = time.monotonic()
        self.bot.redis= await aioredis.from_url(
            "redis://redis-15657.c253.us-central1-1.gce.cloud.redislabs.com:15657",
            username="",
            password=os.getenv("RedisPass"),
            decode_responses=True
        )
        end = time.monotonic()
        print(f"Connected to Redis in {(round((end - start) * 1000, 2))/1000} seconds.")
    
    @commands.group()
    @commands.is_owner()
    async def redis(self, ctx):
        """Access stuff about redis"""
        if not ctx.invoked_subcommand:
            await ctx.send_help("redis")

    @redis.command()
    async def get(self, ctx, key):
        """Get a certain keys data"""
        data = await self.bot.redis.get(key)

        if not data:
            not_found = discord.Embed(
                title=f"Key {key} Not Found",
                description="""
                """
            )
            return await ctx.send(embed=not_found)

        embed = discord.Embed(
            title="Redis Key Data",
            description=f"""```
{data}
```""",
            timestamp=datetime.datetime.utcnow(),
            color=c_random_color()
        )
        await ctx.send(embed=embed)
    
    @redis.command()
    async def add(self, ctx, key, value):
        """Add something to our db"""
        try:
            await self.bot.redis.set("key", "Data")
            embed = discord.Embed(
                title=f"""Added Key""",
                description=f"""```md
[{key}]({value})
```"""
            )
            return await ctx.send(embed=embed)

        except Exception as e:
            unable = discord.Embed(
                title="Error",
                description=f"""```diff
- {e}
```""",
                timestamp=datetime.datetime.utcnow(),
                color=c_get_color("red")
            )

    @redis.command()
    async def search(self, ctx, pattern="*"):
        """List all our keys"""
        keys = ""
        for count, value in enumerate(await self.bot.redis.keys(pattern), start=1):
            keys = f"""{keys}\n{count}. {value}"""

        if keys == "":
            keys = f"""[{pattern}][None]"""

        embed = discord.Embed(
            title=f"""Redis Keys in Database - {len(await self.bot.redis.keys("*"))}""",
            description=f"""```md
{keys}
```""",
            timestamp=datetime.datetime.utcnow(),
            color=c_random_color()
        )
        await ctx.send(embed=embed)

    @redis.command()
    async def info(self, ctx):
        """Show some info about our connection"""
        embed = discord.Embed(
            title="Redis Info",
            description=f"""```asciidoc
= ACL Info =
[ User: {await self.bot.redis.acl_whoami()} ]

= Connection Info =
[ User: {await self.bot.redis.client_getname()} ]
[ ID: {await self.bot.redis.client_id()}]

= Misc =
[ Database Size (Keys): {await self.bot.redis.dbsize()} ]
```"""
        )

    @redis.command()
    async def cinfo(self, ctx):
        """Show complex info about our Redis DB"""
        data = await self.bot.redis.info()

        visual = ""

        for item in data.keys():
            visual = f"""{visual}\n[ {item.replace("_", " ").capitalize()}: {data[item]} ]"""

        embed = discord.Embed(
            title="Redis Complex Info",
            description=f"""```asciidoc
= Info =
{visual}
```""",
            timestamp=datetime.datetime.utcnow(),
            color=c_random_color()
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Redis(bot))