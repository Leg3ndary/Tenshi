"""
Tenshi Discord Bot
Copyright (C) 2021 Ben Z.
This software is licensed under Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)
"""

import discord
from discord.ext import commands
import datetime
from cogs.colors import *
import googletrans
from googletrans import Translator


class Translation(commands.Cog):
    """Translating Input"""
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

def setup(bot):
    bot.add_cog(Translation(bot))