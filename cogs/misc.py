"""
Tenshi Discord Bot
Copyright (C) 2021 Ben Z.
This software is licensed under Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)
"""

import discord
from discord.ext import commands, tasks
from gears.hbot import h_get_time
import matplotlib.pyplot as plt
import numpy as np
from gears.cosmetics import *
import time
import asyncio


async def bot_latency(latency):
    """Return the bots latency through some math because why not"""
    ping = round(latency * 1000, 2)
    return ping


class Misc(commands.Cog):
    """Commands with no real category that I just have here"""
    def __init__(self, bot):
        self.bot = bot
        self.ping_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.ping_loop.start()

    def cog_unload(self):
        """On cog unload stop the ping loop."""
        self.ping_loop.cancel()

    @tasks.loop(minutes=1)
    async def ping_loop(self):
        if len(self.ping_data) > 19:
            del self.ping_data[0]
        self.ping_data.append(await bot_latency(self.bot.latency))

    @ping_loop.before_loop
    async def before_ping(self):
        print(f"Awaiting first ping loop.")
        await self.bot.wait_until_ready()
    
    @commands.command(aliases=['pong'])
    async def ping(self, ctx):
        """Checkout the bots ping..."""
        image = discord.File("C:/Users/benzh/OneDrive/Documents/Tenshi/ping.png", filename="ping.png")

        x_axis = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
        y_axis = np.array(self.ping_data)

        plt.title("Tenshi Ping Over The Last 20 Minutes")
        plt.xlabel("Time In Minutes")
        plt.ylabel("Average Ping")
        plt.grid()

        plt.plot(x_axis, y_axis)
        
        plt.savefig("ping.png")
        plt.close()
    
        embed = discord.Embed(
            title="Tenshi Ping", 
            description=f"""```md
Pong! 
<Tenshi Latency='{str(await bot_latency(self.bot.latency))}'>
```""", 
            timestamp=h_get_time(), 
            color=c_random_color()
            )
        embed.set_image(url="attachment://ping.png")
        return await ctx.send(file=image, embed=embed)

    @commands.command()
    async def ping(self, ctx):
        """Return the bots current ping..."""
        start = time.monotonic()
        message = await ctx.send("Pinging...")
        end = time.monotonic()
        totalPing = round((end - start) * 1000, 2)
        e = discord.Embed(title="Pinging..", description=f"Overall Latency: {totalPing}ms")
        await asyncio.sleep(0.25)
        try:
            await message.edit(content=None, embed=e)
        except discord.NotFound:
            return

        botPing = round(self.bot.latency * 1000, 2)
        e.description = e.description + f"\nDiscord WebSocket Latency: {botPing}ms"
        await asyncio.sleep(0.25)

        averagePing = (botPing + totalPing) / 2
        if averagePing >= 1000:
            color = c_get_color("red")
        elif averagePing >= 200:
            color = c_get_color("orange")
        else:
            color = c_get_color("green")


        e.color = color
        try:
            await message.edit(embed=e)
        except discord.NotFound:
            return

        e.title = "Pong!"

        await asyncio.sleep(0.25)
        try:
            await message.edit(embed=e)
        except discord.NotFound:
            return
    
    @commands.command(aliases=['pfp'])
    async def avatar(self, ctx, *, member: discord.Member=None):
        """Display a users avatar"""
        if not member:
            member = ctx.author

        embed = discord.Embed(
            title=f"{member.display_name}'s Avatar", 
            timestamp=h_get_time(), 
            color=c_random_color()
        )
        embed.set_image(
            url=member.avatar_url
        )
        return await ctx.send(embed=embed)
    
    @commands.command()
    async def about(self, ctx):
        embed = discord.Embed(
            title="About Tenshi",
            description="""Tenshi is a bot made by the user _Leg3ndary#0001, the bot was made in the midst of Covid 19 and is based off a fictional anime character known as Tenshi or Tachibana Kanade from Angel Beats
            The bot itself has a range of features most of which aren't useful however are fun and interesting!
            Hope you'll continue to support it! 
            -Ben""",
            timestamp=h_get_time(), 
            color=c_random_color()
        )
        embed.set_thumbnail(
            url=self.bot.user.avatar_url
        )
        try:
            ben = await self.bot.get_user(360061101477724170)
        except:
            ben = await self.bot.fetch_user(360061101477724170)
        embed.set_footer(
            text=ben.name,
            icon_url=ben.avatar_url
        )
        return await ctx.send(embed=embed)
        
    @commands.command()
    async def credits_(self, ctx):
        """Credits for commands, art, etc"""
        

def setup(bot):
    bot.add_cog(Misc(bot))
    print("Misc Loaded.")