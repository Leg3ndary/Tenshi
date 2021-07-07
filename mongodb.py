"""
Tenshi Discord Bot
Copyright (C) 2021 Ben Z.
This software is licensed under Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)
"""

import discord
from discord.ext import commands
import datetime as dt
import random as rnd
import os
import pymongo
from bson import ObjectId
import time

# Functions
def random_hex():
    random_number = rnd.randint(0,0xffffff)
    return random_number

def convert(seconds):
    ty_res = time.gmtime(seconds)
    res = time.strftime("%H hours, %M minutes and %S seconds", ty_res)

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

username = os.getenv('MongoUser')
password = os.getenv('MongoPass')

pymongo_client = pymongo.MongoClient(f"mongodb+srv://{username}:{password}@tenshi-cluster.bvwvs.mongodb.net/tenshi_db?retryWrites=true&w=majority")

# Database Retrieval
tenshi_db = pymongo_client["tenshi_db"]
admin_client = pymongo_client["admin"]
server_user_db = pymongo_client["server_user_db"]
admin_client = pymongo_client["admin"]

# Collection(s) retrieval
todolist = tenshi_db["todolist"]
blacklist = tenshi_db["blacklist"]
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

# Returning a list with all blacklisted 
# Updating and retrieving blacklist data
async def update_bl():
    blacklist_list = []
    for user in blacklist.find():
        blacklist_list.append(user["id"])
    print(f"Updated Blacklist List...\nAdding to Bot Instance")
    return blacklist_list

# fix this later use cache
def format_bl():
    blacklist_data = ""
    for user in blacklist.find():
        blacklist_data = f"{blacklist_data}\n- {user['id']} - {user['_id']} -"
    return blacklist_data

class MongoDB(commands.Cog):
    """Interactions with our database"""
    def __init__(self, bot):
        self.bot = bot
    
    # DevOnly Methods
    @commands.Cog.listener()
    async def on_ready(self):
        """creating Caches and stuff"""
        b_start = time.monotonic()
        self.bot.blacklist = await update_bl()
        b_end = time.monotonic()
        print(f"Blacklist Retrieved in {(round((b_end - b_start) * 1000, 2))/100} seconds.")
        self.bot.prefix_dict = prefix_dict
        self.bot.user_dict = user_dict
        print("Added Prefix and User Cache.")
        
        # Horrible ass method to do stuff... Fix this later please
        guild_list = []
        for guild in self.bot.guilds:
            guild_list.append(str(guild.id))

        guild_list_len = len(guild_list)
        print(f"{len(guild_list)} servers retrieved from discord.")

        for guild_setting in server_settings.find():
            try:
                guild_list.remove(str(guild_setting["_id"]))
            except:
                pass

        if guild_list_len-len(guild_list) != guild_list_len:
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
        if ctx.invoked_subcommand is None:
            return
        
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
            timestamp=dt.datetime.utcnow(),
            color=random_hex()
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
                timestamp=dt.datetime.utcnow(),
                color=random_hex()
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
            timestamp=dt.datetime.utcnow(),
            color=random_hex()
        )
        return await ctx.send(embed=embed_col)

    @cloud.group()
    async def stats(self, ctx):
        if ctx.invoked_subcommand is None:
            return

    @stats.command(aliases=['serverstats'])
    async def serverstatus(self, ctx, db):    
        if db.lower() not in pymongo_client.list_database_names():
            embed_error = discord.Embed(
                title="Command Error",
                description=f"""```diff
- Database {db} not found
```""",
                timestamp=dt.datetime.utcnow(),
                color=random_hex()
            )
            return await ctx.send(embed=embed_error)
        if db.lower() in ['tenshi_db']:
            data = tenshi_db.command("serverStatus")

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
            timetstamp=dt.datetime.utcnow(),
            color=random_hex()
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
                timestamp=dt.datetime.utcnow(),
                color=random_hex()
            )
            return await ctx.send(embed=embed_error)
        if db.lower() in ['tenshi_db']:
            data = tenshi_db.command("dbStats")
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
            timestamp=dt.datetime.utcnow(),
            color=random_hex()
        )
        return await ctx.send(embed=embed)
    
    @commands.group(aliases=['todolist'])
    @commands.is_owner()
    async def tdl(self, ctx):
        if ctx.invoked_subcommand is None:
            return

    @tdl.command()
    async def add(self, ctx, *, args):
        tdl_dict = { "Task": f"{args}" }
        tdl_data = todolist.insert_one(tdl_dict)
        embed = discord.Embed(
            title="Task Added",
            description=f"""ID: `{tdl_data.inserted_id}`
```
{args}
```""",
            timestamp=dt.datetime.utcnow(),
            color=random_hex()
        )
        return await ctx.send(embed=embed)
    
    @tdl.command()
    async def list(self, ctx):
        for item in todolist.find():
            await ctx.send(item)

    @tdl.command()
    async def remove(self, ctx, id):
        id_query = { '_id': ObjectId(id)}
        todolist.delete_one(id_query)
        await ctx.send('finished, deleted')


# Adding the Cog
def setup(bot):
    bot.add_cog(MongoDB(bot))