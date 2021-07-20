"""
Tenshi Discord Bot
Copyright (C) 2021 Ben Z.
This software is licensed under Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)
"""

import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import time
from cogs.colors import *

load_dotenv()

async def get_prefix(bot, message):
    """Gets the prefix from built cache, if a guild isn't found (Direct Messages) assumes prefix is the below"""
    if message.guild is None:
        return "t>"
    return bot.prefix_cache[str(message.guild.id)]


bot = commands.Bot(
    command_prefix=get_prefix,
    intents=discord.Intents.all(),
    activity=discord.Streaming(name="Music - t>help", url="https://www.youtube.com/watch?v=Turf7WDB3iY")
)


cog_list = [
    "cogs.devonly", # basically done
    "cogs.help", # also basically done for now
    "cogs.anime", # need to add all the other methods sighs
    "cogs.other", # basically done
    "cogs.music", # not done
    "cogs.unsplash", # not done
    "cogs.systeminfo", # Done.
    "cogs.mongodb", # will update as I need too
    "cogs.settings", # will update as I need too
    "cogs.colors", # add menu pages
    "cogs.moderation", # Done.
    "cogs.language", # Done. Maybe update dictionary and add a menu.
    "cogs.redis", # Not Done.
    "cogs.errorhandler", # Done.
    "cogs.exalia.exalia" # Not Done.
]

bot.cog_list = cog_list


start = time.monotonic()
for cog in cog_list:
    bot.load_extension(cog)
end = time.monotonic()

print(f"{len(cog_list)} cogs loaded in {(round((end - start) * 1000, 2))/1000} seconds.")

@bot.event
async def on_ready():
    """On ready do stuff"""
    bot.update_channel = await bot.fetch_channel(866868897398259732)
    embed = discord.Embed(
       title="Cogs",
       description=f"""```diff
+ {len(cog_list)} cogs loaded in {(round((end - start) * 1000, 2))/1000} seconds.
```""",
       timestamp=datetime.datetime.utcnow(),
       color=c_get_color("green")
    )
    await bot.update_channel.send(embed=embed)


bot.run(os.getenv("Token"))