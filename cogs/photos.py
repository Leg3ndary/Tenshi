"""
Tenshi Discord Bot
Copyright (C) 2021 Ben Z.
This software is licensed under Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)
"""

import discord
from discord.ext import commands
import datetime
import gears.unsplash
from gears.cosmetics import *

unsplash_client = gears.unsplash.Unsplash()

class Photos(commands.Cog):
    """Photo related commands, acts as an ui for our unsplash gear"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def unsplash(self, ctx):
        if not ctx.invoked_subcommand:
            await ctx.send_help("unsplash")

    @unsplash.command()
    async def info(self, ctx):
        """Display some info about our connection with Unsplash"""
        print(await unsplash_client.get_random_photo())
        await ctx.send(await unsplash_client.get_ratelimit_remaining())

def setup(bot):
    bot.add_cog(Photos(bot))