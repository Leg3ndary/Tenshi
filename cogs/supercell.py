"""
Tenshi Discord Bot
Copyright (C) 2021 Ben Z.
This software is licensed under Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)
"""

import discord
from discord.ext import commands, menus
from gears.coc import CocClient, coc_emojis
from gears.cosmetics import *
import urllib.parse
import asyncio
from gears.hbot import h_get_time


coc_colors = {
    "unranked": 0xb3b4b3,
    "bronze": 0xb77f53,
    "silver": 0x83838a,
    "gold": 0xf0b747,
    "crystal": 0x8544c1,
    "master": 0x1c1317,
    "champion": 0xa42a17,
    "titan": 0xf8df48,
    "legend": 0x8f5afd
}


async def gen_coc_user_page(data):
    """Generate the basic user page with most of the data"""
    
    embed = discord.Embed(
       title=f"""{data["name"]} - TH {data["townHallLevel"]}""",
       description=f"""{coc_emojis["exp"]} **Level:** {data["expLevel"]}
       {coc_emojis["trophym"]} **Trophies:** {data["trophies"]} (**Personal Best** {data["bestTrophies"]})
       {coc_emojis["star"]} **War Stars:** {data["warStars"]}
       """,
       timestamp=h_get_time(),
       color=c_random_color()
    )
    embed.add_field(
        name=f"Season Stats",
        value=f"""{coc_emojis["sword"]} **Attacks Won:** {data["attackWins"]}
        {coc_emojis["shield"]} **Defenses Won:** {data["defenseWins"]}""",
        inline=False
    )
    embed.add_field(
        name="s",
        value="s",
        inline=False
    )
    embed.set_thumbnail(
        url=data["league"]["iconUrls"]["medium"]
    )
    embed.set_author(
        name=f"""{data["clan"]["name"]} - Level {data["clan"]["clanLevel"]} - {data["role"].title()}""",
        url=f"""https://link.clashofclans.com/en?action=OpenClanProfile&tag={urllib.parse.quote(data["clan"]["tag"])}""",
        icon_url=data["clan"]["badgeUrls"]["large"]
    )
    return embed


class CocUserPage(menus.Menu):
    """The clash of clans user page"""
    def __init__(self, data):
        super().__init__(timeout=60.0, delete_message_after=False)
        self.data = data
        self.page_number = 0
        self.page_cap = len(data) - 1
        self.cooldown = 3

    async def send_initial_message(self, ctx, channel):
        """The initial message that we send"""
        anime_embed = await gen_coc_user_page(self.data)
        return await channel.send(embed=anime_embed)

    """
    @menus.button(c_get_emoji("left"))
    async def on_back(self, payload):
        "\""When we click to go back a page"\""
        if self.page_number > 1:
            self.page_number -= 1
        else:
            self.page_number = self.page_cap
        anime_embed = gen_anime_search(self.data[self.page_number])
        await self.message.edit(embed=anime_embed)
        return await asyncio.sleep(self.cooldown
    """


class Supercell(commands.Cog):
    """Supercell related commands, eg clash of clans (coc), clash royale"""
    def __init__(self, bot):
        self.bot = bot
        self.coc = CocClient()

    @commands.group()
    async def coc(self, ctx):
        """Clash of clans related commands"""
        if not ctx.invoked_subcommand:
            await ctx.send_help("coc")

    @coc.command()
    @commands.dm_only()
    async def verify(self, token: str):
        """Command to verify self"""
        

    @coc.command()
    async def player(self, ctx, tag: str):
        """Find a player by their tag"""
        if "#" not in tag:
            tag = "#" + tag
        data = await self.coc.get_player(urllib.parse.quote(tag))

        if data["/request-status"] == 404:
            embed_nf = discord.Embed(
               title=f"Not Found",
               description=f"""```fix
{data["message"]}
```""",
               timestamp=h_get_time(),
               color=c_get_color("yellow")
            )
            return await ctx.send(embed=embed_nf)
        
        else:
            coc_page = CocUserPage(data)
            return await coc_page.start(ctx)

def setup(bot):
    bot.add_cog(Supercell(bot))