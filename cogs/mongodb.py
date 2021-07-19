"""
Tenshi Discord Bot
Copyright (C) 2021 Ben Z.
This software is licensed under Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)
"""

import discord
from discord.ext import commands
import datetime
import os
import motor.motor_asyncio
import time
from cogs.colors import *


def convert(seconds):
    """Convert time to a human readable format"""
    ty_res = time.gmtime(seconds)
    res = time.strftime("%H hours, %M minutes and %S seconds", ty_res)

def get_size(bytes, suffix="B"):
    """Return human readable size"""
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


motor_client = motor.motor_asyncio.AsyncIOMotorClient(f"mongodb+srv://{os.getenv('MongoUser')}:{os.getenv('MongoPass')}@tenshi-cluster.bvwvs.mongodb.net/database?retryWrites=true&w=majority")

# Database Retrieval
database = motor_client["database"]
server_db = motor_client["server"]
user_db = motor_client["user"]
admin_db = motor_client["admin"]

# Collection(s) retrieval
prefixes = server_db["prefixes"]
users = user_db["users"]

prefix_cache = {}


async def cache_prefixes(bot, ctx=None):
    """Cache prefixes also send stuff to ctx if provided"""
    start = time.monotonic()
    cursor = prefixes.find()
    for prefix in await cursor.to_list(length=len(bot.guilds)):
        prefix_cache.update({str(prefix["_id"]): prefix["prefixes"]})

    bot.prefix_cache = prefix_cache

    # We need everything in a string format
    guild_list = []
    for guild in bot.guilds:
        guild_list.append(str(guild.id))

    print(f"{len(guild_list)} servers joined.")
    if ctx:
        await ctx.send(f"{len(guild_list)} servers joined.")

    cursor = prefixes.find()
    # Going through our prefix list and checking for unadded guilds
    for prefix in await cursor.to_list(length=len(bot.guilds)):
        try:
            guild_list.remove(str(prefix["_id"]))
        except:
            # Just in case
            pass

    if len(guild_list) > 0:
        print(f"{len(guild_list)} servers not detected in prefixes, adding.")
        if ctx:
            await ctx.send(f"{len(guild_list)} servers not detected in prefixes, adding.")

        for guild_na in guild_list:
            prefix_insert = {
                "_id": str(guild_na),
                "prefixes": ["t>"]
            }
            bot.prefix_cache[str(guild_na)] = prefix_insert["prefixes"]
            await prefixes.insert_one(prefix_insert)

        print(f"Finished adding {len(guild_list)} to prefixes.")
        if ctx:
            await ctx.send(f"Finished adding {len(guild_list)} to prefixes.")
    else:
        print("No guilds not detected in prefixes.")
        if ctx:
            await ctx.send("No guilds not detected in prefixes.")
    
    end = time.monotonic()

    print(f"{len(prefix_cache)} prefixes in prefixes cache loaded in {(round((end - start) * 1000, 2))/1000} seconds.")
    if ctx:
        await ctx.send(f"{len(prefix_cache)} prefixes in prefixes cache loaded in {(round((end - start) * 1000, 2))/1000} seconds.")

class MongoDB(commands.Cog):
    """Interactions with MongoDB"""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """Setting up prefix cache"""
        await cache_prefixes(self.bot)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        """On guild join insert the prefix to our db and add to cache"""
        prefix_insert = {
            "_id": str(guild.id),
            "prefixes": ["t>"],
        }
        self.bot.prefix_cache[str(guild.id)] = prefix_insert["prefixes"]
        await prefixes.insert_one(prefix_insert)

    @commands.group()
    @commands.is_owner()
    async def cloud(self, ctx):
        """Cloud related commands"""
        if not ctx.invoked_subcommand:
            return await ctx.send_help("cloud")
        
    @cloud.command(
        help="List databases that are currently in our database"
    )
    async def showdb(self, ctx):
        """List databases currently in our database"""
        databases = await motor_client.list_database_names()
        database_list = ""

        for db in databases:
            database_list = f"{database_list}\n+ {db}"

        embed = discord.Embed(
            title="Listing Databases",
            description=f"""```diff
{database_list}
```
            **{len(databases)}** databases currently loaded in cluster.""",
            timestamp=datetime.datetime.utcnow(),
            color=c_random_color()
        )
        await ctx.send(embed=embed)

    @cloud.command(aliase=["showcollections", "showcollection"])
    async def showcol(self, ctx, db):
        """Showing Collections"""
        if db not in await motor_client.list_database_names():
            embed_error = discord.Embed(
                title="Error",
                description=f"""```diff
- Database {db} not found
```""",
                timestamp=datetime.datetime.utcnow(),
                color=c_get_color("red")
            )
            return await ctx.send(embed=embed_error)

        database_shiz = motor_client[db]
        collection_list = ""

        for col in await database_shiz.list_collection_names():
            collection_list = f"{collection_list}\n+ {col}"

        embed = discord.Embed(
            title="Listing Databases",
            description=f"""```diff
{collection_list}
```
            **{len(await database.list_collection_names())}** collections currently loaded in `{db}`.""",
            timestamp=datetime.datetime.utcnow(),
            color=c_random_color()
        )
        await ctx.send(embed=embed)

    @cloud.group()
    async def stats(self, ctx):
        """Show stats about our db..."""
        if not ctx.invoked_subcommand:
            await ctx.send_help("stats")

    @stats.command(aliases=['serverstats'])
    async def serverstatus(self, ctx, db):
        """Show our mongodb server status"""  
        if db.lower() not in await motor_client.list_database_names():
            embed_error = discord.Embed(
                title="Error",
                description=f"""```diff
- Database {db} not found
```""",
                timestamp=datetime.datetime.utcnow(),
                color=c_get_color("red")
            )
            return await ctx.send(embed=embed_error)

        if db.lower() in ['database']:
            data = await database.command("serverStatus")

        embed = discord.Embed(
            title="Tenshi MongoDB Statistics",
            description=f"""```asciidoc
[ Process and Version ]
= {data['process']} - {data['version']} =
[ Uptime ]
= {convert(data['uptimeEstimate'])} =
[ Connections ]
= Current: {data['connections']['current']} =
= Available: {data['connections']['available']} =
= Total Created: {data['connections']['totalCreated']} =
[ Network ]
= Data Recieved: {get_size(data['network']['bytesIn'])} =
= Data Sent: {get_size(data['network']['bytesOut'])} =
= Total Requests: {data['network']['numRequests']} =
```""",
            timetstamp=datetime.datetime.utcnow(),
            color=c_random_color()
        )
        await ctx.send(embed=embed)

    @stats.command()
    async def storage(self, ctx, db):
        if db.lower() not in await motor_client.list_database_names():
            embed_error = discord.Embed(
                title="Error",
                description=f"""```diff
- Database {db} not found
```""",
                timestamp=datetime.datetime.utcnow(),
                color=c_get_color("red")
            )
            return await ctx.send(embed=embed_error)

        if db.lower() in ['database']:
            data = await database.command("dbStats")

        embed = discord.Embed(
            title=f"{db} Database Storage",
            description=f"""```asciidoc
[ Collections ]
= {data['collections']} =
[ Objects ]
= {data['objects']} =
[ Average Object Size ]
= {get_size(data['avgObjSize'])} =
[ Total Object Size ]
= {get_size(data['dataSize'])} =
```""",
            timestamp=datetime.datetime.utcnow(),
            color=c_random_color()
        )
        await ctx.send(embed=embed)

    @commands.group()
    @commands.is_owner()
    async def recache(self, ctx):
        """Recacheing Users, Prefixes, or Guilds"""
        if ctx.invoked_subcommand is None:
            await ctx.send_help("cache")

    @recache.command()
    async def prefix(self, ctx):
        """Recache prefixes"""
        await cache_prefixes(self.bot, ctx)


def setup(bot):
    bot.add_cog(MongoDB(bot))