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

def len_file(file):
    """Return the file length for a given file"""
    try:
        with open(file, encoding="utf8") as f:
            for i, l in enumerate(f):
                pass
        return i + 1
    except Exception as e:
        print(e)
        return 0

def get_files(directory: str=None):
    """Return every file using recursion"""
    files = []
    if directory:
        if directory == "__pycache__":
            pass
        else:
            directories = os.listdir(directory)
            filepath = directory + "/"
    else:
        filepath = ""
        directories = os.listdir()
    for file in directories:
        if file.endswith(".exe") or file.endswith(".png") or file.endswith(".pyc"):
            pass
        elif "." not in file:
            recursion = get_files(f"{filepath}{file}")
            files = files + recursion
        else:
            files.append(f"{filepath}{file}")
    print(files)
    return files


bot = commands.Bot(
    command_prefix=get_prefix,
    intents=discord.Intents.all(),
    activity=discord.Streaming(name="Music - t>help", url="https://www.youtube.com/watch?v=Turf7WDB3iY")
)


cog_list = [
    "cogs.devonly", # Done. May add more stuff idk
    "cogs.help", # Not done, will update formatting last.
    "cogs.anime", # Not Done.
    "cogs.other", # -
    "cogs.music", # Not done.
    "cogs.systeminfo", # Done.
    "cogs.mongodb", # -
    "cogs.settings", # -
    "cogs.colors", # Not Done, 
    "cogs.moderation", # Done.
    "cogs.language", # Done.
    "cogs.redis", # Not Done.
    "cogs.errorhandler", # Done.
    "cogs.exalia.exalia", # Not Done.
    "cogs.photos" # Not Done
]

bot.cog_list = cog_list

file_len_list = {}
total = 0

start = time.monotonic()
for file in get_files():
    file_len = len_file(file)
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
       timestamp=datetime.datetime.utcnow(),
       color=c_get_color("green")
    )
    await bot.update_channel.send(embed=embed)


bot.run(os.getenv("Token"))