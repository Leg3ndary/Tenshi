"""
Tenshi Discord Bot
Copyright (C) 2021 Ben Z.
This software is licensed under Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)
"""

import discord
from discord.ext import commands
import datetime

# Cog Setup
class Insults(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command
    async def insult_check(self, ctx):
        pass

# Adding the Cog
def setup(bot):
    bot.add_cog(Insults(bot))