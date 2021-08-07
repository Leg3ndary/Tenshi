"""
Tenshi Discord Bot
Copyright (C) 2021 Ben Z.
This software is licensed under Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)
"""

import discord
from discord.ext import commands, menus
import random
import datetime
from gears.cosmetics import *

class ColorMenu(menus.Menu):
    def __init__(self):
        super().__init__(timeout=60, delete_message_after=True)

# Cog Setup
class Colors(commands.Cog):
    """Everything related to Tenshi's colors"""
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def colors(self, ctx):
        """All of Tenshis colors!"""
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(
                title="Tenshi's Colors",
                description="""The following are all of Tenshi's default colors""",
                timestamp=datetime.datetime.utcnow(),
                color=c_random_color()
            )
            return await ctx.send(embed=embed)

    @colors.command(help="Display the Navy Color")
    async def navy(self, ctx):
        embed = discord.Embed(
            title="Navy",
            description="Navy",
            color=self.bot.default_colors["navy"],
            timestamp=datetime.datetime.utcnow()
        )
        await ctx.send(embed=embed)

    @colors.command(
        help="Display the Blue Color"
    )
    async def blue(self, ctx):
        embed = discord.Embed(
            title="Blue",
            description="Blue",
            color=self.bot.default_colors["Blue"],
            timestamp=datetime.datetime.utcnow()
        )
        await ctx.send(embed=embed)

# Adding the Cog
def setup(bot):
    bot.add_cog(Colors(bot))
