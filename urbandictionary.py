"""
Tenshi Discord Bot
Copyright (C) 2021 Ben Z.
This software is licensed under Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)
"""

import discord
from discord.ext import commands, menus
import datetime
import aiohttp
from colors import *
import asyncio

thumbs_up = "<a:thumbs_up:815047014542082059>"
thumbs_down = "<a:thumbs_down:815047039066701894>"

async def get_word(word: str):
    """Request a words data from urbandictionary"""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://api.urbandictionary.com/v0/define?term={word}") as request:
            if request.status == 200:
                return await request.json()
            else:
                print(f"[ERROR] [{datetime.datetime.utcnow()}] {request.status} {await request.json()}")

def cut(text: str, cut_num=300):
    """Cut a paragraph to resize it and fit it correctly"""
    list_data = []
    cut_num = int(cut_num)
    for index in range(0, len(text), cut_num):
        list_data.append(text[index : index + cut_num])
    return(list_data)

def clean(text:str):
    text = text.replace("[", "").replace("]", "").replace("*", "").capitalize()
    return text

def gen_embed(data):
    """Generate an embed with the data needed in it"""
    embed = discord.Embed(
        title=f"""__{data["word"]}__""",
        description=f"""{clean(data["definition"])}""",
        url=data["permalink"],
        timestamp=datetime.datetime.utcnow(),
        color=c_random_color()
    )
    embed.set_author(
        name=f"""Author: {data["author"]}"""
    )
    embed.add_field(
        name=f"""Votes""",
        value=f"""{thumbs_up} {data["thumbs_up"]:,}
        {thumbs_down} {data["thumbs_down"]:,}""",
        inline=False
    )
    return embed

class UrbanMenu(menus.Menu):
    """Urban Dictionary Menus"""
    def __init__(self, data):
        super().__init__(timeout=60)
        self.data = data
        self.page_cap = len(data) - 1
        self.page_number = 0

    async def send_initial_message(self, ctx, channel):
        """Initial Page thats sent"""
        embed = gen_embed(self.data[self.page_number])
        return await channel.send(embed=embed)

    @menus.button(":back_button_triangle:843677189533597749")
    async def on_back(self, payload):
        """When we click to go back a page"""
        if self.page_number > 1:
            self.page_number -= 1
        else:
            self.page_number = self.page_cap
        embed = gen_embed(self.data[self.page_number])
        await self.message.edit(embed=embed)
        return await asyncio.sleep(1)
    
    @menus.button(":pause:820003279941271592")
    async def on_stop(self, payload):
        """If users wanna be nice and stop the embed tracking reactions when its done..."""
        self.stop()

    @menus.button(":play_button_triangle:820007884641402920")
    async def on_next(self, payload):
        """When users click next"""
        if self.page_number < self.page_cap:
            self.page_number += 1
        else:
            self.page_number = 0
        embed = gen_embed(self.data[self.page_number])
        await self.message.edit(embed=embed)
        return await asyncio.sleep(1)


class UrbanDictionary(commands.Cog):
    """The urban dictionary!"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        aliases=["ud"],
        help="Search the urban dictionary for words that you may not know!",
        brief="Urban Dictionary", 
        usage="<Word>",
        description="Command requires an NSFW channel as it may contain NSFW posts/definitions."
    )
    @commands.cooldown(1.0, 7.0, commands.BucketType.user)
    @commands.is_nsfw()
    async def urban(self, ctx, word):
        """Search the urban dictionary for words"""
        data = await get_word(word)
        data = data['list']
        if len(data) == 0:
            embed_failure = discord.Embed(
                title='Search Failure',
                description="Seems like your search didn't turn up any matches...",
                timstamp=datetime.datetime.utcnow(),
                color=c_random_color()
            )
            return await ctx.send(embed=embed_failure)
        dmenu = UrbanMenu(data)
        await dmenu.start(ctx)

    @urban.error
    async def urban_error(self, ctx, error):
        """If we encounter some error of some kind"""
        if isinstance(error, commands.CommandOnCooldown):
            cooldown_embed = discord.Embed(
                title=f"Urbandictionary is on Cooldown",
                description=f"""Try again in {error.retry_after:.2f} seconds.""", 
                timestamp = datetime.datetime.utcnow(),
                color=c_get_color("red")
            )
            return await ctx.send(embed=cooldown_embed)
        elif isinstance(error, commands.errors.NSFWChannelRequired):
            embed_nsfw = discord.Embed(
                title='Nsfw',
                description='Urban Dictionary can contain NSFW posts so this command may only be run in NSFW channels.',
                timstamp=datetime.datetime.utcnow(),
                color=c_get_color("red")
                )
            return await ctx.send(embed=embed_nsfw)


def setup(bot):
    bot.add_cog(UrbanDictionary(bot))