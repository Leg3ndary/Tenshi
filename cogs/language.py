"""
Tenshi Discord Bot
Copyright (C) 2021 Ben Z.
This software is licensed under Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)
"""

import discord
from discord.ext import commands, menus
import datetime
import aiohttp
from gears.cosmetics import *
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

async def cut(text: str, cut_num=300):
    """Cut a paragraph to resize it and fit it correctly currently not used..."""
    list_data = []
    cut_num = int(cut_num)
    for index in range(0, len(text), cut_num):
        list_data.append(text[index : index + cut_num])
    return(list_data)

async def clean(text:str):
    text = text.replace("[", "").replace("]", "").replace("*", "").capitalize()
    return text

async def u_gen_embed(data):
    """Generate an embed with the data needed in it"""
    embed = discord.Embed(
        title=f"""__{data["word"]}__""",
        description=f"""{await clean(data["definition"])}""",
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

async def reformat_list(data):
    """Reformat a list, just a quick function that I have"""
    new_data = []
    for item in data:
        new_data.append(f"`{item}`")
    return new_data


async def d_gen_embed(data, word):
    """Generate an embed with the data given"""
    embed = discord.Embed(
       title=f"""{word.capitalize()} - {data["partOfSpeech"].capitalize()}""",
       description=f"""""",
       timestamp=datetime.datetime.utcnow(),
       color=c_random_color()
    )
    definition_num = 1
    for definition in data["definitions"]:
        if definition.get("synonyms"):
            synonyms = ", ".join(await reformat_list(definition.get("synonyms")))
        
        else:
            synonyms = "`None Given`"
        
        embed.add_field(
            name=f"""Definition {str(definition_num)}""",
            value=f"""{definition.get("definition", "None")}
            > {definition.get("example", "None")}
            {synonyms}""",
            inline=False
        )
        definition_num += 1

    return embed


class UrbanMenu(menus.Menu):
    """Urban Dictionary Menus"""
    def __init__(self, data):
        super().__init__(timeout=60)
        self.data = data
        self.page_cap = len(data) - 1
        self.page_number = 0
        self.on_cooldown = False

    async def send_initial_message(self, ctx, channel):
        """Initial Page thats sent"""
        embed = await u_gen_embed(self.data[self.page_number])
        return await channel.send(embed=embed)

    @menus.button(c_get_emoji("left"))
    async def on_back(self, payload):
        """When we click to go back a page"""
        if self.on_cooldown is True:
            return
        if self.page_number > 1:
            self.page_number -= 1
        else:
            self.page_number = self.page_cap
        embed = await u_gen_embed(self.data[self.page_number])
        await self.message.edit(embed=embed)
        self.on_cooldown = True
        await asyncio.sleep(2)
        self.on_cooldown = False
    
    @menus.button(c_get_emoji("stop"))
    async def on_stop(self, payload):
        """If users wanna be nice and stop the embed tracking reactions when its done..."""
        self.stop()

    @menus.button(c_get_emoji("right"))
    async def on_next(self, payload):
        """When users click next"""
        if self.on_cooldown is True:
            return
        elif self.page_number < self.page_cap:
            self.page_number += 1
        else:
            self.page_number = 0
        embed = await u_gen_embed(self.data[self.page_number])
        await self.message.edit(embed=embed)
        self.on_cooldown = True
        await asyncio.sleep(2)
        self.on_cooldown = False


class Dictionary(menus.Menu):
    """Regular Dictionary Menus"""
    def __init__(self, data):
        super().__init__(timeout=60)
        self.data = data
        self.page_cap = len(data["meanings"]) - 1
        self.page_number = 0
        self.on_cooldown = False

    async def send_initial_message(self, ctx, channel):
        """Initial Page thats sent"""
        embed = await d_gen_embed(self.data["meanings"][self.page_number], self.data["word"])
        return await channel.send(embed=embed)

    @menus.button(c_get_emoji("left"))
    async def on_back(self, payload):
        """When we click to go back a page"""
        if self.on_cooldown is True:
            return
        elif self.page_number > 1:
            self.page_number -= 1
        else:
            self.page_number = self.page_cap
        embed = await d_gen_embed(self.data["meanings"][self.page_number], self.data["word"])
        await self.message.edit(embed=embed)
        self.on_cooldown = True
        await asyncio.sleep(2)
        self.on_cooldown = False
    
    @menus.button(c_get_emoji("stop"))
    async def on_stop(self, payload):
        """If users wanna be nice and stop the embed tracking reactions when its done..."""
        self.stop()

    @menus.button(c_get_emoji("right"))
    async def on_next(self, payload):
        """When users click next"""
        if self.on_cooldown is True:
            return
        elif self.page_number < self.page_cap:
            self.page_number += 1
        else:
            self.page_number = 0
        embed = await d_gen_embed(self.data["meanings"][self.page_number], self.data["word"])
        await self.message.edit(embed=embed)
        self.on_cooldown = True
        await asyncio.sleep(2)
        self.on_cooldown = False


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
        umenu = UrbanMenu(data)
        await umenu.start(ctx)

    @commands.group()
    async def translate(self, ctx):
        """Translating the given text with certain options"""
        if not ctx.invoked_subcommand:
            embed = discord.Embed(
                title="Imagine",
                description=f"""""",
                timestamp=datetime.datetime.utcnow(),
                color=c_random_color()
            )
            return await ctx.send(embed=embed)
    
    @translate.command(
        aliases=["a"],
        help="Auto detect the language and attempt to translate it",
        brief="Auto Translate", 
        usage="<Text>",
        description=""
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
        aliases=["c"],
        help="Run a complex translation using an input and output language",
        brief="Complex Translate", 
        usage="<Input Language> <Output Language> <Text>",
        description="Use the translate list command to view possible translation codes"
    )
    async def complex(self, ctx, inp: str, out: str, *, text: str=None):
        """Define the input and output language"""
        if not text:
            # No message do shit
            pass

        end = self.translator.translate(text=text, dest=out, src=inp)
        #print(end.extra_data) Update later
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
        aliases=["l"],
        help="List all possible translation codes",
        brief="Translation Code List", 
        usage="",
        description="This command is only usable in dms for spam reasons"
    )
    @commands.dm_only()
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

    @commands.command(
        aliases=["dict"],
        help="Search a regular dictionary for the meaning of a word.",
        brief="Dictionary Search", 
        usage="<Word>",
        description=""
    )
    @commands.cooldown(2.0, 6.0, commands.BucketType.user)
    async def dictionary(self, ctx, word: str):
        data = await d_get_word("en_US", word)
        data = data[0]
        dmenu = Dictionary(data)
        await dmenu.start(ctx)


def setup(bot):
    bot.add_cog(Language(bot))