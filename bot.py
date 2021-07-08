"""
Tenshi Discord Bot
Copyright (C) 2021 Ben Z.
This software is licensed under Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)
"""

import discord
from discord.ext import commands
import datetime as dt
from dotenv import load_dotenv
import os   
import urllib
import time
import asyncio
import colors
#import keep_alive
load_dotenv()

def get_prefix(bot, message):
    """Gets the prefix from built cache, if a guild isn"t found (Direct Messages) assumes prefix is the below"""
    if message.guild is None:
        return ["t>", ">"]
    return bot.prefix_dict[str(message.guild.id)]

# Bot instance
bot = commands.Bot(
    command_prefix=get_prefix,
    intents=discord.Intents.all(),
    activity=discord.Streaming(name="Music - t>help", url="https://www.youtube.com/watch?v=Turf7WDB3iY")
)

# Cog list which we then add to bot instance
cog_list = [
    "devonly",
    "help",
    "anime",
    "urbandictionary", # Done
    "other",
    "music",
    "unsplash",
    "dictionary",
    "systeminfo", # Done
    "mongodb",
    "data",
    "colors",
    "moderation",
    "translate"
]

bot.cog_list = cog_list

# Just showing how long it takes the cog to load
start = time.monotonic()
for cog in cog_list:
    bot.load_extension(cog)
end = time.monotonic()
print(f"{len(cog_list)} Cogs Loaded in {(round((end - start) * 1000, 2))/1000} seconds.")

@bot.event
async def on_ready():
    """On ready show the bot logging in."""
    print(f"Bot Login Success.\n{bot.user}")
    #while 1:
        #urllib.request.urlopen("https://Tenshi.benzhou.repl.co")
        #await asyncio.sleep(200)

@bot.event
async def on_command(ctx):
    """For detecting new users that are using our bot and welcoming them/adding to db"""
    try:
        test_var = bot.user_dict[str(ctx.author.id)]
        return

    except:
        embed = discord.Embed(
            title=f"Hi {ctx.author.name}!",
            description="""Thanks for using Tenshi!
            We are adding you to our database, however please make sure you review our rules with the rules command.""",
            timestamp=dt.datetime.utcnow(),
            color=colors.get_color(bot)
        )
        await ctx.send(embed=embed)
        settings_format = {
            "_id": str(ctx.author.id),
            "supporter": False,
            "accepted_rules": True,
            "dm_updates": True,
            "embed_colors": "random"
        }
        #user_settings.insert_one(settings_format) Update in mongodb
        bot.user_dict[str(ctx.author.id)] = settings_format
        await ctx.send("Finished")

# Keep Alive Function
# keep_alive.keep_alive()

bot.run(os.getenv("Token"))