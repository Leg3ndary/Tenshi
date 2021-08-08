"""
Tenshi Discord Bot
Copyright (C) 2021 Ben Z.
This software is licensed under Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)
"""

import discord
from discord.ext import commands, menus
import datetime
from gears.cosmetics import *
import asyncio


async def gen_color_embed(color):
    """Generate a color embed based on the color given"""
    embed = discord.Embed(
       title=f"{reversed_colors[color]}",
       description=f"""""",
       timestamp=datetime.datetime.utcnow(),
       color=c_random_color()
    )
    embed.set_thumbnail(url=f"""https://res.cloudinary.com/demo/image/upload/w_100,h_100,e_colorize,co_rgb:{hex(color).replace("0x", "")}/one_pixel.png""")
    return embed


class Colors(menus.Menu):
    """Color menu too view our colors"""
    def __init__(self, color):
        super().__init__(timeout=60)
        self.color = color
        self.page_cap = len(colors)
        self.page_number = 0
        self.on_cooldown = False

    async def send_initial_message(self, ctx, channel):
        """Initial Page thats sent"""
        embed = await gen_color_embed()
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
        embed = await gen_color_embed()
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
        embed = await gen_color_embed()
        await self.message.edit(embed=embed)
        self.on_cooldown = True
        await asyncio.sleep(2)
        self.on_cooldown = False


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
