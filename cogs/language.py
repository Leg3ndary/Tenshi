"""
Tenshi Discord Bot
Copyright (C) 2021 Ben Z.
This software is licensed under Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)
"""

import discord
from discord.ext import commands, menus
import datetime
import aiohttp
from cogs.colors import *
import asyncio
import googletrans
from googletrans import Translator

thumbs_up = "<a:thumbs_up:815047014542082059>"
thumbs_down = "<a:thumbs_down:815047039066701894>"

async def ud_get_word(word: str):
    """Request a words data from urbandictionary"""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://api.urbandictionary.com/v0/define?term={word}") as request:
            if request.status == 200:
                return await request.json()
            else:
                print(f"[ERROR] [{datetime.datetime.utcnow()}] {request.status} {await request.json()}")

async def d_get_word(language, word):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.dictionaryapi.dev/api/v2/entries/{language}/{word}") as request:
            return(await request.json())

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


class Language(commands.Cog):
    """Language related commands"""
    def __init__(self, bot):
        self.bot = bot
        self.translator = Translator()
        self.bot.languages = googletrans.LANGUAGES
        self.bot.langcodes = googletrans.LANGCODES

    @commands.Cog.listener()
    async def on_ready(self):
        """When ready create a new cache of current languages available"""
        lang_list= []

        for language in self.bot.languages.keys():
            lang_list.append(f"""<{language:5} = {self.bot.languages[language]}>""")

        self.bot.viewlang = f"\n".join(lang_list)

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
        data = await ud_get_word(word)
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

    @commands.group()
    async def translate(self, ctx):
        """Translating the given text"""
        if not ctx.invoked_subcommand:
            embed = discord.Embed(
                title="Imagine",
                description=f"""""",
                timestamp=datetime.datetime.utcnow(),
                color=c_random_color()
            )
            return await ctx.send(embed=embed)
    
    @translate.command(
        aliases=["a"]
    )
    async def auto(self, ctx, *, text: str = None):
        """Automatically detect the language and output it in english"""
        if not text:
            # No message do shit
            pass

        end = self.translator.translate(text=text, dest="en", src="auto")
        data = end.extra_data
        print(end.extra_data)
        embed = discord.Embed(
            title="Translation",
            description=f"""```
{end.text}
```""",
            timestamp=datetime.datetime.utcnow(),
            color=c_random_color()
        )
        
        await ctx.send(embed=embed)

    @translate.command(
        aliases=["c"]   
    )
    async def complex(self, ctx, inp: str, out: str, *, text: str=None):
        """Define the input and output language"""
        if not text:
            # No message do shit
            pass

        end = self.translator.translate(text=text, dest=out, src=inp)
        data = end.extra_data
        print(end.extra_data)
        embed = discord.Embed(
            title="Translation",
            description=f"""```
{end.text}
```""",
            timestamp=datetime.datetime.utcnow(),
            color=c_random_color()
        )

        await ctx.send(embed=embed)

    @translate.command(
        aliases=["l"]
    )
    async def list(self, ctx):
        """Show the list of languages you can currently use"""
        embed = discord.Embed(
            title="============== Translation Code List ==============",
            description=f"""```md
{self.bot.viewlang}
```""",
            timestamp=datetime.datetime.utcnow(),
            color=c_random_color()
        )
        await ctx.author.send(embed=embed)

    @commands.command()
    async def language(self, ctx):
        """Posts an embed giving reasons as to why we can't translate"""
        pass

    @commands.command(aliases=["dict"])
    @commands.cooldown(2.0, 6.0, commands.BucketType.user)
    async def dictionary(self, ctx, word: str):
        data = await d_get_word('en_US', word)
        data = data[0]

        embed = discord.Embed(
           title=f"__{word.capitalize()}__ Search",
            timestamp=datetime.datetime.utcnow(),
            color=c_random_color(),
            url=data['phonetics'][0]['audio']
        )
        
        for meaning in data['meanings']:
            synonoms = []
            if 'synonyms' in meaning['definitions'][0]:
                for synonom in meaning['definitions'][0]['synonyms']:
                    synonoms.append(synonom.capitalize())
            
            else:
                synonoms = 'None'

            if 'example' in meaning['definitions'][0]:
                example = meaning['definitions'][0]['example'].capitalize()
            else:
                example = 'None'

            embed.add_field(
                name=meaning['partOfSpeech'].capitalize(),
                value=f"""{meaning['definitions'][0]['definition'].capitalize()}
                > *{example}*
                Synonoms: {str(synonoms).replace('[', '').replace(']', '').replace("'", "")}""",
                inline=False
            )
        
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Language(bot))