"""
Tenshi Discord Bot
Copyright (C) 2021 Ben Z.
This software is licensed under Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)
"""

import discord
from discord.ext import commands
import datetime
from colors import *
from googletrans import Translator


class Translation(commands.Cog):
    """Anything to do with translating"""
    def __init__(self, bot):
        self.bot = bot
        self.translator = Translator()

    @commands.group()
    async def translate(self, ctx):
        """Translating the given text"""
        if not ctx.invoked_subcommand:
            pass
    
    @translate.command(
        aliases=["a"]
    )
    async def auto(self, ctx, *, text: str = None):
        """Automatically detect the language and output it in english"""
        if not text:
            # No message do shit
            pass

        end = self.translator.translate(text=text, dest="en", src="auto")

        print(end.extra_data)
        embed = discord.Embed(
            title=None
        )
        await ctx.send(end.text)

    @translate.command()
    async def complex(self, ctx, inp: str, out: str, text: str):
        """Define the input and output language"""
        pass

    @commands.command()
    async def language(self, ctx):
        """Posts an embed giving reasons as to why we can't translate"""
        pass

def setup(bot):
    bot.add_cog(Translation(bot))
