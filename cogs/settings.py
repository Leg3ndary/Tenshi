"""
Tenshi Discord Bot
Copyright (C) 2021 Ben Z.
This software is licensed under Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)
"""

import discord
from discord.ext import commands
from gears.hbot import h_get_time
import asyncio
import motor.motor_asyncio
import os
from gears.cosmetics import *


motor_client = motor.motor_asyncio.AsyncIOMotorClient(f"""mongodb+srv://{os.getenv("MongoUser")}:{os.getenv("MongoPass")}@tenshi-cluster.bvwvs.mongodb.net/database?retryWrites=true&w=majority""")

database = motor_client["database"]
server_db = motor_client["server"]
user_db = motor_client["user"]

prefixes = server_db["prefixes"]
user_settings = user_db["users"]


class Settings(commands.Cog):
    """Anything related to server settings"""
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @commands.cooldown(2.0, 6.0, commands.BucketType.user)
    async def prefix(self, ctx):
        """Return a list of the servers current prefixes..."""
        if ctx.invoked_subcommand is None:
            data = self.bot.prefix_cache[str(ctx.guild.id)]

            prefixes_list = ""
            for prefix in data:
                prefixes_list = f"{prefixes_list}\n{prefix}"

            embed = discord.Embed(
                title="Server Prefixes",
                description=f"""{ctx.guild.name} has `{len(data)}` prefixes
```fix
{prefixes_list}
```""",
                timestamp=h_get_time(),
                color=c_random_color()
            )
            await ctx.send(embed=embed)

    @prefix.command()
    @commands.has_permissions(manage_guild=True)
    async def add(self, ctx, prefix: str):
        """Add a prefix to the bot"""
        if len(prefix) > 10:
            embed_se = discord.Embed(
                title="Error",
                description=f"""{prefix} must be less then `10` characters
                Not sure why you need more then that... 
                Already a pain typing it out""",
                timestamp=h_get_time(),
                color=c_get_color("red")
            )
            return await ctx.send(embed=embed_se)
        
        data = self.bot.prefix_cache[str(ctx.guild.id)]

        if len(data) >= 5:
            embed_ne = discord.Embed(
                title="Prefix Error",
                description=f"""Your server has too many prefixes!
                You may have a max of 5 prefixes!""",
                timestamp=h_get_time(),
                color=c_get_color("red")
            )
            return await ctx.send(embed=embed_ne)

        elif prefix in data:
            embed_paf = discord.Embed(
                title="Error",
                description=f"""Prefix {prefix} has already been added to your server!""",
                timestamp=h_get_time(),
                color=c_get_color("red")
            )
            return await ctx.send(embed=embed_paf)

        data.append(prefix)

        await prefixes.update_one({"_id": str(ctx.guild.id)}, {"$set":{"prefixes":data}})
        self.bot.prefix_cache[str(ctx.guild.id)] = data

        prefixes_format = ""
        for prefix in data:
            prefixes_format = f"{prefixes_format}\n{prefix}"

        embed = discord.Embed(
            title="Server Prefix Added",
            description=f"""{ctx.guild.name} now has `{len(data)}` prefixes
```fix
{prefixes_format}
```""",
            timestamp=h_get_time(),
            color=c_get_color("green")
        )
        return await ctx.send(embed=embed)

    @prefix.command()
    @commands.has_permissions(manage_guild=True)
    async def remove(self, ctx, prefix: str):
        """Remove a prefix from a server"""
        data = self.bot.prefix_cache[str(ctx.guild.id)]

        if prefix not in data:
            embed_nf = discord.Embed(
                title="Error",
                description=f"""Sorry but that prefix wasn't found!
                Make sure you're removing existing prefixes!""",
                timestamp=h_get_time(),
                color=c_get_color("red")
            )
            return await ctx.send(embed=embed_nf)

        if len(data) == 1:
            embed_tl = discord.Embed(
                title="Error",
                description="""You need at least one prefix!""",
                timestamp=h_get_time(),
                color=c_get_color("red")
            )
            return await ctx.send(embed=embed_tl)

        data.remove(prefix)

        await prefixes.update_one({"_id": str(ctx.guild.id)}, {"$set":{"prefixes":data}})
        self.bot.prefix_dict[str(ctx.guild.id)] = data

        prefixes_format = ""
        for prefix in data:
            prefixes_format = f"{prefixes_format}\n{prefix}"

        embed = discord.Embed(
            title="Server Prefix Removed",
            description=f"""{ctx.guild.name} now has `{len(data)}`` prefixes
```fix
{prefixes_format}
```""",
            timestamp=h_get_time(),
            color=c_get_color("green")
        )
        return await ctx.send(embed=embed)

    @prefix.command()
    @commands.has_permissions(manage_guild=True)
    async def reset(self, ctx):
        """Reset all prefixes"""
        embed_rusure = discord.Embed(
            title="Are you sure?",
            description=f"""This change will remove all current prefixes and replace them with 
```fix
t>
```
            This change is irreversable.""",
            timestamp=h_get_time(),
            color=c_get_color("yellow")
        )
        embed_msg = await ctx.send(embed=embed_rusure)

        await embed_msg.add_reaction("✅")
        await embed_msg.add_reaction("❌")

        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=lambda r, u: str(r.emoji) in ["✅", "❌"] and u == ctx.author, timeout=30)

        except asyncio.TimeoutError:
            embed_timeout = discord.Embed(
                title="Canceled",
                description="You didn't react within 30 seconds",
                timestamp=h_get_time(),
                color=c_get_color("red")
            )
            return await ctx.send(embed=embed_timeout)

        if str(reaction.emoji) == "✅":
            await prefixes.update_one({"_id": str(ctx.guild.id)}, {"$set":{"prefixes":["t>"]}})

            self.bot.prefix_cache[str(ctx.guild.id)] = ["t>"]

            embed_reset = discord.Embed(
                title="Server Prefixes Reset",
                description=f"""The servers prefixes have been reset to
```fix
t>
```""",
                timestamp=h_get_time(),
                color=c_get_color("green")
            )
            return await ctx.send(embed=embed_reset)

        elif str(reaction.emoji) == "❌":
            embed_cancel = discord.Embed(
                title="Canceled",
                description="Cancelled Reset",
                timestamp=h_get_time(),
                color=c_get_color("red")
            )
            return await ctx.send(embed=embed_cancel)


def setup(bot):
    bot.add_cog(Settings(bot))