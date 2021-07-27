"""
Tenshi Discord Bot
Copyright (C) 2021 Ben Z.
This software is licensed under Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)
"""

import discord
from discord.ext import commands
import datetime
import gears.unsplash


class Photos(commands.Cog):
    """Photo related commands, acts as an ui for our unsplash gear"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command
    async def unsplash(self, ctx):
        pass


def setup(bot):
    bot.add_cog(Photos(bot))