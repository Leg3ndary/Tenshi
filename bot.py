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

def get_prefix(bot, message):
    """Gets the prefix from built cache, if a guild isn"t found (Direct Messages) assumes prefix is the below"""
    if message.guild is None:
        return "t>"
    return bot.prefix_cache[str(message.guild.id)]


bot = commands.Bot(
    command_prefix=get_prefix,
    intents=discord.Intents.all(),
    activity=discord.Streaming(name="Music - t>help", url="https://www.youtube.com/watch?v=Turf7WDB3iY")
)


cog_list = [
    "cogs.devonly",
    "cogs.help",
    "cogs.anime",
    "cogs.other",
    "cogs.music",
    "cogs.unsplash",
    "cogs.systeminfo", # Done
    "cogs.mongodb",
    "cogs.data",
    "cogs.colors",
    "cogs.moderation",
    "cogs.language",
    "cogs.redis",
    "cogs.errorhandler",
    "cogs.exalia.exalia"
]

bot.cog_list = cog_list

start = time.monotonic()
for cog in cog_list:
    bot.load_extension(cog)
end = time.monotonic()

print(f"{len(cog_list)} cogs loaded in {(round((end - start) * 1000, 2))/1000} seconds.")


@bot.event
async def on_ready():
    """On ready show the bot logging in."""
    print(f"Bot Login Success.\n{bot.user}")

@bot.event
async def on_command(ctx):
    """For detecting new users that are using our bot and quickly adding them to our database."""


bot.run(os.getenv("Token"))