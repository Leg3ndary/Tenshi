"""
Tenshi Discord Bot
Copyright (C) 2021 Ben Z.
This software is licensed under Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)
"""

import discord
from discord.ext import commands, tasks
import datetime as dt
import random as rnd
import asyncio
import matplotlib.pyplot as plt
import numpy as np

# Functions
def random_hex():
    random_number = rnd.randint(0,0xffffff)
    return(random_number)
    
def bot_latency(latency):
    ping = latency * 1000
    ping = round(ping, 2)
    return(ping)

# Cog Setup
class Other(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ping_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.ping_loop.start()

    # Tracking MS Data
    @tasks.loop(minutes=1)
    async def ping_loop(self):
        if len(self.ping_data) > 19:
            del self.ping_data[0]
        
        self.ping_data.append(bot_latency(self.bot.latency))

    @ping_loop.before_loop
    async def before_ping(self):
        print(f"Pending Finish = Loop ID 01 /// Ping Loop")
        await self.bot.wait_until_ready()
    
    @commands.command(aliases=['pong'])
    async def ping(self, ctx):
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
<Tenshi Latency='{str(bot_latency(self.bot.latency))}'>
```""", 
            timestamp=dt.datetime.utcnow(), 
            color=random_hex()
            )
        embed.set_image(url="attachment://ping.png")
        return await ctx.send(file=image, embed=embed)
    
    @commands.command(aliases=['pfp','icon', 'av'])
    async def avatar(self, ctx, *,  avatarmember : discord.Member=None):
        if not avatarmember:
            avatarmember = ctx.author

        embed = discord.Embed(
            title=f"{avatarmember.display_name}'s Avatar", 
            timestamp=dt.datetime.utcnow(), 
            color=random_hex()
            ) 
        embed.set_image(url=avatarmember.avatar_url)
        return await ctx.send(embed=embed)
    
    @commands.command(aliases=['ab'])
    async def about(self, ctx):
        embed = discord.Embed(
            title="About Tenshi",
            description="""Tenshi is a bot made by the user _Leg3ndary#0001, the bot was made in the midst of Covid 19 and is based off a fictional anime character known as Tenshi or Tachibana Kanade from Angel Beats
            The bot itself has a range of features most of which aren't useful however are fun and interesting!
            Hope you'll continue to support it! 
            -Ben""",
            timestamp=dt.datetime.utcnow(), 
            color=random_hex()
        )
        embed.add_field(
            name="Thank You!",
            value="""Special Thanks too [Icons8](https://icons8.com) for letting Tenshi use its amazing and free icons!""",
        )
        embed.set_thumbnail(
            url=self.bot.user.avatar_url
        )
        return await ctx.send(embed=embed)
        


# Adding the Cog
def setup(bot):
    bot.add_cog(Other(bot))