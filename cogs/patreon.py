"""
Tenshi Discord Bot
Copyright (C) 2021 Ben Z.
This software is licensed under Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)
"""

import discord
from discord.ext import commands
from gears.hbot import h_get_time
import patreon
from gears.cosmetics import *


class Patreon(commands.Cog):
    """Payment related commands"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["donate"])
    async def patreon(self, ctx):
        """Patreon info"""
        

def setup(bot):
    bot.add_cog(Patreon(bot))