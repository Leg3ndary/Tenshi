"""
Tenshi Discord Bot
Copyright (C) 2021 Ben Z.
This software is licensed under Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)
"""

import discord
from discord.ext import commands, menus
import random
import datetime

# Deprecciated for now.
"""
def get_color(bot, ctx=None):
    \"\"\"Gets one of our bots default colors\"\"\"
    if ctx is not None:
        if str(ctx.author.id) in bot.user_dict:
            color_data = bot.user_dict[str(ctx.author.id)]["embed_colors"] # Get Data
            if color_data == "default":
                try:
                    color = bot.color_dict[ctx.command]
                    color = bot.color[color]
                except:
                    print(f"[ERROR] [{datetime.datetime.utcnow()}]: Command {ctx.command} was not found in the color database, please add it.")
                    color = 1 # Black + 1 since disc doesn't like full black
                return color
            elif color_data =="random_default":
                return random.choice(bot.color_list)

    color = random.randint(0,0xffffff)
    return color
"""

def c_random_color():
    return colors[random.choice(color_list)]

def c_get_color(color):
    return colors[color]

colors = {
    "_id": "default",
    "navy": 0x001F3F,
    "blue": 0x0074D9,
    "aqua": 0x7FDBFF,
    "teal": 0x39CCCC,
    "olive": 0x3D9970,
    "green": 0x2ECC40,
    "lime": 0x01FF70,
    "yellow": 0xFFDC00,
    "orange": 0xFF851B,
    "red": 0xFF4136,
    "maroon": 0x85144b,
    "pink": 0xF012BE,
    "purple": 0xB10DC9,
    "black": 0x111111,
    "gray": 0xAAAAAA,
    "silver": 0xDDDDDD,
    "white": 0xFFFFFF
}

color_list = ["navy", "blue", "aqua", "teal", "olive", "green", "lime", "yellow", "orange", "red", "maroon", "pink", "purple", "black", "gray", "silver", "white"]

# Color Dictionary for commands :p
color_dict = {
    "colors": "random_default",
    "colors navy": colors["navy"],
}

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
