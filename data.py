"""
Tenshi Discord Bot
Copyright (C) 2021 Ben Z.
This software is licensed under Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)
"""

import discord
from discord.ext import commands
import datetime as dt
import random 
import asyncio
import pymongo
import os

def get_color(ctx, bot):
    color_data = bot.user_dict[str(ctx.author.id)]["embed_colors"]
    color = 0
    if color_data == "random":
        color = random.randint(0,0xffffff)
    
    if color_data == "default":
        pass

    print(ctx.command)

    return color

def random_hex():
    return random.randint(0,0xffffff)

# PyMongo DB Stuff
username = os.getenv('MongoUser')
password = os.getenv('MongoPass')

pymongo_client = pymongo.MongoClient(f"mongodb+srv://{username}:{password}@tenshi-cluster.bvwvs.mongodb.net/tenshi_db?retryWrites=true&w=majority")


# Database Retrieval
tenshi_db = pymongo_client["tenshi_db"]
server_user_db = pymongo_client["server_user_db"]
admin_client = pymongo_client["admin"]

# Collection(s) retrieval
server_settings = server_user_db["server"]
user_settings = server_user_db["user"]

# Cog Setup
class Data(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def prefix(self, ctx):
        if ctx.invoked_subcommand is None:
            data = server_settings.find_one({"_id": str(ctx.guild.id)})
            data = data["prefixes"]

            prefixes_list = ""
            for prefix in data:
                prefixes_list = f"{prefixes_list}\n{prefix}"

            embed = discord.Embed(
                title="Server Prefixes",
                description=f"""{ctx.guild.name} has {len(data)} prefixes
```fix
{prefixes_list}
```""",
                timestamp=dt.datetime.utcnow(),
                color=random_hex()
            )
            return await ctx.send(embed=embed)
    
    @prefix.command(help="Display prefix")
    async def add(self, ctx, prefix: str):
        if len(prefix) > 10:
            embed_se = discord.Embed(
                title="Prefix Too Long!",
                description=f"""{prefix} must be less then 10 characters
                Not sure why you need more then that... 
                Already a pain typing it out""",
                timestamp=dt.datetime.utcnow(),
                color=random_hex()
            )
            return await ctx.send(embed=embed_se)
        
        data = server_settings.find_one({"_id": str(ctx.guild.id)})
        data = data["prefixes"]

        if len(data) >= 5:
            embed_ne = discord.Embed(
                title="Prefix Error",
                description=f"""Your server has too many prefixes!
                You can have a max of 5 prefixes!""",
                timestamp=dt.datetime.utcnow(),
                color=random_hex()
            )
            return await ctx.send(embed=embed_ne)

        elif prefix in data:
            embed_paf = discord.Embed(
                title="Prefix already Added",
                description=f"""Prefix {prefix} is already in the database!""",
                timestamp=dt.datetime.utcnow(),
                color=random_hex()
            )
            return await ctx.send(embed=embed_paf)

        # Adding prefix to data list
        data.append(prefix)

        # Everything
        prefix_data = { "$set": { "prefixes": data } }

        # Doing it
        server_settings.update_one({"_id": str(ctx.guild.id)}, prefix_data)

        self.bot.prefix_dict[str(ctx.guild.id)] = data

        prefixes_format = ""
        for prefix in data:
            prefixes_format = f"{prefixes_format}\n{prefix}"

        embed = discord.Embed(
            title="Server Prefix Added",
            description=f"""{ctx.guild.name} has {len(data)} prefixes
```fix
{prefixes_format}
```""",
            timestamp=dt.datetime.utcnow(),
            color=random_hex()
        )
        return await ctx.send(embed=embed)

    @prefix.command()
    async def remove(self, ctx, prefix: str):
        data = server_settings.find_one({"_id": str(ctx.guild.id)})
        data = data["prefixes"]
        if prefix not in data:
            embed_nf = discord.Embed(
                title="Prefix Not Found",
                description=f"""Sorry but that prefix wasn't found!
                Make sure you're removing existing prefixes!""",
                timestamp=dt.datetime.utcnow(),
                color=random_hex()
            )
            return await ctx.send(embed=embed_nf)

        if len(data) == 1:
            embed_tl = discord.Embed(
                title="Prefix Error",
                description="""You need at least one prefix!""",
                timestamp=dt.datetime.utcnow(),
                color=random_hex()
            )
            return await ctx.send(embed=embed_tl)

        data.remove(prefix)
        prefix_data = { "$set": { "prefixes": data } }

        # Doing it
        server_settings.update_one({"_id": str(ctx.guild.id)}, prefix_data)

        self.bot.prefix_dict[str(ctx.guild.id)] = data

        prefixes_format = ""
        for prefix in data:
            prefixes_format = f"{prefixes_format}\n{prefix}"

        embed = discord.Embed(
            title="Server Prefix Removed",
            description=f"""{ctx.guild.name} has {len(data)} prefixes
```fix
{prefixes_format}
```""",
            timestamp=dt.datetime.utcnow(),
            color=random_hex()
        )
        return await ctx.send(embed=embed)

    @prefix.command()
    async def reset(self, ctx):
        embed_rusure = discord.Embed(
            title="Are you sure?",
            description=f"""This change will remove all current prefixes and replace them with 
```fix
t>
>
```
        This change is irreversable."""
        )
        embed_msg = await ctx.send(embed=embed_rusure)
        await embed_msg.add_reaction('✅')
        await embed_msg.add_reaction('❌')

        def reset_embed_check(reaction, user):
            return str(reaction.emoji) in ['✅', '❌'] and user != self.bot.user and user == ctx.author

        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=reset_embed_check, timeout=30)

        except asyncio.TimeoutError:
            embed_timeout = discord.Embed(
                title="Canceled",
                description="You didn't react within 30 seconds",
                timestamp=dt.datetime.utcnow(),
                color=random_hex()
            )
            return await ctx.send(embed=embed_timeout)

        else:
            if str(reaction.emoji) == '✅':
                prefix_data = { "$set": { "prefixes": ['t>', '>'] } }

                # Doing it
                server_settings.update_one({"_id": str(ctx.guild.id)}, prefix_data)

                self.bot.prefix_dict[str(ctx.guild.id)] = ['t>', '>']

                embed_reset = discord.Embed(
                    title="Server Prefixes Reset",
                    timestamp=dt.datetime.utcnow(),
                    color=random_hex()
                )
                return await ctx.send(embed=embed_reset)

            elif str(reaction.emoji) == '❌':
                embed_cancel = discord.Embed(
                    title="Canceled",
                    description="Cancelled Reset",
                    timestamp=dt.datetime.utcnow(),
                    color=random_hex()
                )
                return await ctx.send(embed=embed_cancel)


    # User stuff below
    @commands.group()
    async def user(self, ctx):
        if ctx.invoked_subcommand is None:
            try:
                user_data = self.bot.user_dict[str(ctx.author.id)]
                user_string = ""
                for key, value in user_data.items():
                    user_string = f"{user_string}\n[{key}]({value})"
                embed = discord.Embed(
                    title=f"{ctx.author} Settings",
                    description=f"""```md
{user_string}
```""",
                    timestamp=dt.datetime.utcnow(),
                    color=get_color(ctx, self.bot)
                )
                return await ctx.send(embed=embed)
            except:
                embed_fail = discord.Embed(
                    title="We couldn't find you!",
                    description=f"""Sorry {ctx.author.mention}, seems like we couldn't find you in our database...
                    Don't worry though, we're in the process of adding you!""",
                    timestamp=dt.datetime.utcnow(),
                    color=get_color(ctx, self.bot)
                )
                return await ctx.send(embed=embed_fail)

    @user.command()
    async def blahh(self, ctx):
        get_color(ctx, self.bot)
        return 
        
# Adding the Cog
def setup(bot):
    bot.add_cog(Data(bot))