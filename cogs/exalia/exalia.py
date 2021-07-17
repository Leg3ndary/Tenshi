"""
Tenshi Discord Bot
Copyright (C) 2021 Ben Z.
This software is licensed under Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)
"""

import discord
from discord.ext import commands
import datetime 
from cogs.colors import *
from cogs.exalia.inventory import *
import os
import time
import asyncio
import motor.motor_asyncio


exalia_client = motor.motor_asyncio.AsyncIOMotorClient(
    f"""mongodb+srv://{os.getenv("ExaliaUser")}:{os.getenv("ExaliaPass")}@exalia.w0dur.mongodb.net/users?retryWrites=true&w=majority"""
)

users = exalia_client["users"]

bal = users["bal"]
data = users["data"]
inv = users["inv"]

coin = "<a:tcoin:864926193878040577>"
gem = "<a:tgem:864926382424588289>"

# Easy way to get subclasses
subclass = {
    "knight": [
        "tank",
        "swordsman"
    ],
    "wizard": [
        "arcanist",
        "scholar"
    ],
    "archer": [
        "sniper",
        "hunter"
    ],
    "assassin": [
        "fighter",
        "runner"
    ],    
    "giant": [
        "golem",
        "berserker"
    ],
}

# Getting default class values, Attack, Defence, Magic, Health, Armor, Speed.
class_value = {
    "knight": {
        "default": [5, 5, 1, 5, 5, 4],
        "tank": [0, 0, 0, 4, 3, -2],
        "swordsman": [4, 1, 0, 0, 0, 0]
    },
    "wizard": {
        "default": [2, 1, 10, 4, 4, 4],
        "arcanist": [0, 0, 5, 0, 0, 0],
        "scholar": [2, 2, 1, 0, 0, 0]
    },
    "archer": {
        "default": [8, 3, 3, 4, 4, 3],
        "sniper": [5, 0, 0, 0, 0, 0],
        "hunter": [0, 0, 0, 1, 2, 2]
    },
    "assassin": {
        "default": [6, 2, 2, 3, 4, 8],
        "fighter": [3, 2, 0, 0, 0, 0],
        "runner": [2, 0, 0, 0, 0, 3]
    },
    "giant": {
        "default": [5, 5, 1, 5, 5, 4],
        "golem": [0, 0, 0, 0, 5, 0],
        "berserker": [0, 0, 0, 2, 0, 3]
    }
}


def is_registered():
    """Check if the id has an account made (If this user has started)"""
    async def predicate(ctx):
        data = await bal.find_one({
            "_id": str(ctx.author.id)
        })
        if data:
            return True
        else:
            embed = discord.Embed(
                title="Error",
                description=f"""```diff
- You need to start account first with {ctx.prefix}start!
```""",  
                timestamp=datetime.datetime.utcnow(),
                color=c_get_color("red")          
            )
            await ctx.send(embed=embed)
            return False
    return commands.check(predicate)

def multiplier(level, amount: int):
    """A simple function so we can make a multiplier which will affect all commands..."""
    multi = 1
    return round(multi * amount * round(1 + level/50))

def calculate_scores(u_class, s_class, type):
    """Calculates scores max values"""
    if type == "default":
        zipped = zip(class_value[u_class]["default"], class_value[u_class][s_class], [1, 1, 1, 1, 1, 1])
    elif type == "max":
        zipped = zip(class_value[u_class]["default"], class_value[u_class][s_class], [5, 5, 5, 5, 5, 5])
    
    final = [(x + y) * z for (x, y, z) in zipped]
    return final



class Exalia(commands.Cog):
    """Currency commands related to Exalia"""
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @commands.is_owner()
    async def exalia(self, ctx):
        """Managing things in our database related to exalia"""
        if not ctx.invoked_subcommamd:
            return await ctx.send_help("exalia")

    @exalia.command()
    async def drop(self, ctx, collection):
        """Delete a document from a collection"""

        if collection.lower() in ["bal", "balance"]:
            col = bal

        if collection.lower() in ["data"]:
            col = data

        if collection.lower() in ["inv", "inventory"]:
            col = inv

        
        await col.delete_one()


    @commands.Cog.listener()
    async def on_ready(self):
        """On ready"""
        pass

    @commands.command()
    @commands.dm_only()
    async def start(self, ctx):
        """When a user needs to start a new account to play our game."""
        cancelled = discord.Embed(
            title="Cancelled",
            description="""Cancelled starting a new character in Exalia.""",
            timestamp=datetime.datetime.utcnow(),
            color=c_get_color("red")
        )

        embed = discord.Embed(
            title=f"Welcome to Exalia {ctx.author.display_name}",
            description=f"""**We are now setting up your account...**""",
            timestamp=datetime.datetime.utcnow(),
            color=c_get_color("red")
        )
        await asyncio.sleep(1)
        message = await ctx.send(embed=embed)

        embed_1 = discord.Embed(
            title=f"Welcome to Exalia {ctx.author.display_name}",
            description=f"""~~We are now setting up your account...~~
            **What class would you like to play as?**
```md
1. Knight
2. Wizard
3. Archer
4. Assassin
5. Giant
```""",
            timestamp=datetime.datetime.utcnow(),
            color=c_get_color("yellow")
        )
        embed_1.set_footer(
            text="If at any time you would like to stop type send \"cancel\""
        )
        await message.edit(embed=embed_1)

        try:
            msg = await self.bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel and str(m.content).lower() in ["1", "2", "3", "4", "5", "knight", "wizard", "archer", "assassin", "giant", "cancel"], timeout=60)

        except asyncio.TimeoutError:
            return await message.edit(embed=cancelled)

        if str(msg.content).lower() in ["1", "knight"]:
            u_class = "knight"
        elif str(msg.content).lower() in ["2", "wizard"]:
            u_class = "wizard"
        elif str(msg.content).lower() in ["3", "archer"]:
            u_class = "archer"
        elif str(msg.content).lower() in ["4", "assassin"]:
            u_class = "assassin"
        elif str(msg.content).lower() in ["5", "giant"]:
            u_class = "giant"
        elif str(msg.content).lower() in ["cancel"]:
            return await message.edit(embed=cancelled)


        subclass_data = subclass[u_class]
        s_check = subclass_data + ["1", "2", "cancel"]
        s_view = ""
        for count, value in enumerate(subclass_data, start=1):
            s_view = f"""{s_view}\n{count}. {value.capitalize()}"""

        embed_2 = discord.Embed(
            title=f"Welcome to Exalia {ctx.author.display_name}",
            description=f"""~~We are now setting up your account...~~
            ~~What class would you like to play as?~~
```diff
+ {u_class.capitalize()}
```
            **What subclass would you like to play as?**
```md
{s_view}
```""",
            timestamp=datetime.datetime.utcnow(),
            color=c_get_color("blue")
        )
        embed_2.set_footer(
            text="If at any time you would like to stop type send \"cancel\""
        )
        await message.edit(embed=embed_2)

        try:
            msg = await self.bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel and str(m.content).lower() in s_check, timeout=60)
        except asyncio.TimeoutError:
            return await message.edit(embed=cancelled)

        if str(msg.content).lower() in ["1", subclass_data[0]]:
            s_class = subclass_data[0]
        elif str(msg.content).lower() in ["2", subclass_data[1]]:
            s_class = subclass_data[1]
        elif str(msg.content).lower() in ["cancel"]:
            return await message.edit(embed=cancelled)

        embed_3 = discord.Embed(
            title=f"Welcome to Exalia {ctx.author.display_name}",
            description=f"""~~We are now setting up your account...~~
            ~~What class would you like to play as?~~
```diff
+ {u_class.capitalize()}
```
            ~~What subclass would you like to play as?~~
```diff
+ {s_class.capitalize()}
```
            **You would like to be a {u_class.capitalize()}, {s_class.capitalize()} correct?**""",
            timestamp=datetime.datetime.utcnow(),
            color=c_get_color("yellow")
        )
        embed_3.set_footer(
            text="If at any time you would like to stop type send \"cancel\""
        )
        await message.edit(embed=embed_3)

        await message.add_reaction("✅")

        try:
            await self.bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and str(reaction.emoji) == "✅", timeout=60)
        except asyncio.TimeoutError:
            return await message.edit(embed=cancelled)

        embed_4 = discord.Embed(
            title=f"Welcome to Exalia {ctx.author.display_name}",
            description=f"""You are now a `{u_class.capitalize()}, {s_class.capitalize()}`!""",
            timestamp=datetime.datetime.utcnow(),
            color=c_get_color("green")
        )
        await message.edit(embed=embed_4)

        # Inserting Bal
        bal_template = {
            "_id": str(ctx.author.id),
            "coins": 1000,
            "gems": 10,
            "level": 1,
            "exp": {
                "current": 0,
                "max": 100
            },
        }
        await bal.insert_one(bal_template)
    
        # Inserting Actual Data
        data_template = {
            "_id": str(ctx.author.id),
            "class": u_class,
            "subclass": s_class,
            "stats": {
                "max": calculate_scores(u_class, s_class, "max"),
                "current": calculate_scores(u_class, s_class, "default")
            }
        }
        await data.insert_one(data_template)

    @commands.command()
    @is_registered()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def profile(self, ctx, user: discord.Member = None):
        """View another user or your own profile"""
        if not user:
            user = ctx.author

        data_d = data.find_one({
            "_id": str(user.id)
        })
        bal_d = await bal.find_one({
            "_id": str(ctx.author.id)
        })

        embed = discord.Embed(
           title=f"{ctx.author.display_name}'s Profile",
           description=f"""""",
           timestamp=datetime.datetime.utcnow(),
           color=c_random_color()
        )
        await ctx.send(embed=embed)


    @commands.command(
        aliases=["bal"]
    )
    @is_registered()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def balance(self, ctx):
        """View your own balance"""
        bal_d = await bal.find_one({
            "_id": str(ctx.author.id)
        })

        embed = discord.Embed(
            title=f"""{ctx.author.display_name}'s Balance""",
            description=f"""{coin} {bal_d["coins"]:,}
            {gem} {bal_d["gems"]:,}""",
            timestamp=datetime.datetime.utcnow(),
            color=c_random_color()
        )
        await ctx.send(embed=embed)

    @commands.command()
    @is_registered()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def work(self, ctx):
        """Work for some coins :L"""
        bal_d = await bal.find_one({
            "_id": str(ctx.author.id)
        })

        amount = multiplier(bal_d["level"], random.randint(1, 10))

        await bal.update_one(
            {"_id": str(ctx.author.id)}, 
            {"$set":{"coins": bal_d["coins"]+amount}}
        )

        embed = discord.Embed(
            title=f"{ctx.author.display_name} is working",
            description=f"""You worked for a total of {coin} {amount:,}!""",
            timestamp=datetime.datetime.utcnow(),
            color=c_get_color("yellow")
        )
        await ctx.send(embed=embed)

    @commands.command()
    @is_registered()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def hunt(self, ctx):
        """Hunt for some coins/animals"""
        pass

    @commands.command()
    @is_registered()
    @commands.cooldown(3, 30, commands.BucketType.user)
    async def shop(self, ctx, search):
        """Check out the shop with a page or item search"""
        if search.is_digit():
            # search was an int, check page
            pass
        else:
            pass

def setup(bot):
    bot.add_cog(Exalia(bot))