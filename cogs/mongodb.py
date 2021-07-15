"""
Tenshi Discord Bot
Copyright (C) 2021 Ben Z.
This software is licensed under Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)
"""

import discord
from discord.ext import commands
import datetime
import os
import pymongo
import time
from cogs.colors import *


def convert(seconds):
    """Convert time to a human readable format"""
    ty_res = time.gmtime(seconds)
    res = time.strftime("%H hours, %M minutes and %S seconds", ty_res)

def get_size(bytes, suffix="B"):
    """Return size given bytes"""
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


pymongo_client = pymongo.MongoClient(f"mongodb+srv://{os.getenv('MongoUser')}:{os.getenv('MongoPass')}@tenshi-cluster.bvwvs.mongodb.net/database?retryWrites=true&w=majority")

# Database Retrieval
database = pymongo_client["database"]
admin_client = pymongo_client["admin"]
server_user_db = pymongo_client["server_user_db"]
admin_client = pymongo_client["admin"]

# Collection(s) retrieval
todolist = database["todolist"]
server_settings = server_user_db["server"]
user_settings = server_user_db["user"]

prefix_dict = {}
user_dict = {}

for prefix_list in server_settings.find():
    prefix_dict.update({str(prefix_list["_id"]): prefix_list["prefixes"]})  
for user in user_settings.find():
    user_dict.update({
        str(user["_id"]): {
            "supporter": user["supporter"],
            "accepted_rules": user["accepted_rules"],
            "dm_updates": user["dm_updates"],
            "embed_colors": user["embed_colors"]
            }})



class MongoDB(commands.Cog):
    """Interactions with MongoDB"""
    def __init__(self, bot):
        self.bot = bot
    
    # DevOnly Methods
    @commands.Cog.listener()
    async def on_ready(self):
        """Doing stuff on_ready"""

        start = time.monotonic()
        self.bot.prefix_dict = prefix_dict
        self.bot.user_dict = user_dict

        
        # Horrible ass method to do stuff... Fix this later please
        
        guild_list = []
        for guild in self.bot.guilds:
            guild_list.append(str(guild.id))

        print(f"{len(guild_list)} servers retrieved from discord.")

        for guild_setting in server_settings.find():
            try:
                guild_list.remove(str(guild_setting["_id"]))
            except:
                pass

        if len(guild_list)-len(guild_list) != len(guild_list):
            print(f"{len(guild_list)} servers not in server_settings, adding them...")
            
            for guild_na in guild_list:
                server_dict = {
                    "_id": str(guild_na),
                    "prefixes": ['t>', '>'],
                    "update_channel": None
                }
                server_settings.insert_one(server_dict)
                self.bot.prefix_dict[str(guild_na)] = server_dict
            print('Finished adding server_settings.')
        else:
            print("No guilds not detected in server_settings, proceeding.")

    @commands.Cog.listener()
    # Also a horrible method, please fix
    async def on_guild_join(self, guild):
        server_dict = {
            "_id": str(guild.id),
            "prefixes": ['t>', '>'],
            "update_channel": None
        }
        server_settings.insert_one(server_dict)
        self.bot.prefix_dict[str(guild.id)] = server_dict
    

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
        databases = pymongo_client.list_database_names()
        database_list = ""

        for db in databases:
            database_list = f"{database_list}\n+ {db}"
        embed_db = discord.Embed(
            title="Listing Databases",
            description=f"""```diff
{database_list}
```
            **{len(databases)}** databases currently loaded in cluster.""",
            timestamp=datetime.datetime.utcnow(),
            color=c_random_color()
        )
        return await ctx.send(embed=embed_db)

    @cloud.command(aliase=["showcollections", "showcollection"])
    async def showcol(self, ctx, db):
        """Showing Collections"""
        if db not in pymongo_client.list_database_names():
            embed_error = discord.Embed(
                title="Command Error",
                description=f"""```diff
- Database {db} not found
```""",
                timestamp=datetime.datetime.utcnow(),
                color=c_random_color()
            )
            return await ctx.send(embed=embed_error)
        database = pymongo_client[db]
        collection_list = ""
        for col in database.list_collection_names():
            collection_list = f"{collection_list}\n+ {col}"
        embed_col = discord.Embed(
            title="Listing Databases",
            description=f"""```diff
{collection_list}
```
            **{len(database.list_collection_names())}** collections currently loaded in `{db}`.""",
            timestamp=datetime.datetime.utcnow(),
            color=c_random_color()
        )
        return await ctx.send(embed=embed_col)

    @cloud.group()
    async def stats(self, ctx):
        if not ctx.invoked_subcommand:
            return

    @stats.command(aliases=['serverstats'])
    async def serverstatus(self, ctx, db):    
        if db.lower() not in pymongo_client.list_database_names():
            embed_error = discord.Embed(
                title="Command Error",
                description=f"""```diff
- Database {db} not found
```""",
                timestamp=datetime.datetime.utcnow(),
                color=c_random_color()
            )
            return await ctx.send(embed=embed_error)
        if db.lower() in ['database']:
            data = database.command("serverStatus")

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
        return await ctx.send(embed=embed)

    @stats.command()
    async def storage(self, ctx, db):
        if db.lower() not in pymongo_client.list_database_names():
            embed_error = discord.Embed(
                title="Command Error",
                description=f"""```diff
- Database {db} not found
```""",
                timestamp=datetime.datetime.utcnow(),
                color=c_random_color()
            )
            return await ctx.send(embed=embed_error)
        if db.lower() in ['database']:
            data = database.command("dbStats")

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
        return await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(MongoDB(bot))