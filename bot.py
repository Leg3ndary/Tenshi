"""
Tenshi Discord Bot
Copyright (C) 2021 Ben Z.
This software is licensed under Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)
"""

import discord
import datetime
from discord.ext import commands
from dotenv import load_dotenv
import os
import time
from gears.cosmetics import *
from gears.hbot import h_get_prefix, h_get_files, h_len_file, h_get_time

load_dotenv()

bot = commands.Bot(
    command_prefix=h_get_prefix,
    intents=discord.Intents.all(),
    activity=discord.Streaming(name="Music - t>help", url="https://www.youtube.com/watch?v=Turf7WDB3iY")
)

cog_list = [
    "cogs.devonly", # Done. May add more stuff idk
    "cogs.help", # Not done, will update formatting last.   
    "cogs.anime", # Not Done.
    "cogs.misc", # -
    "cogs.music", # Not done.
    "cogs.systeminfo", # Done.
    "cogs.mongodb", # -
    "cogs.settings", # -
    "cogs.customs", # Not Done, 
    "cogs.moderation", # Done.
    "cogs.language", # Done.
    "cogs.redis", # Not Done.
    "cogs.errorhandler", # Done.
    "cogs.exalia.exalia", # Not Done.
    "cogs.photos", # Not Done
    "cogs.supercell"
]

bot.cog_list = cog_list

file_len_list = {}
total = 0

start = time.monotonic()
for file in h_get_files():
    file_len = h_len_file(file)
    file_len_list[file] = file_len
    total += file_len
file_len_list["total"] = total 
end = time.monotonic()

print(f"{len(file_len_list)} files length loaded in {(round((end - start) * 1000, 2))/1000} seconds.")

bot.file_len_dict = file_len_list

start = time.monotonic()
for cog in cog_list:
    bot.load_extension(cog)
end = time.monotonic()

print(f"{len(cog_list)} cogs loaded in {(round((end - start) * 1000, 2))/1000} seconds.")

@bot.event
async def on_ready():
    """On ready do stuff"""
    # Remove on actual bot, only used for testing purposes
    bot.update_channel = await bot.fetch_channel(866868897398259732)
    embed = discord.Embed(
        title="Cogs",
        description=f"""```diff
+ {len(cog_list)} cogs loaded in {(round((end - start) * 1000, 2))/1000} seconds.
```""",
        timestamp=h_get_time(),
        color=c_get_color("green")
    )
    await bot.update_channel.send(embed=embed)

bot.run(os.getenv("Token"))