"""
Tenshi Discord Bot
Copyright (C) 2021 Ben Z.
This software is licensed under Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)
"""

import discord
from discord.ext import commands
import datetime as dt
import random as rnd
import aiohttp
import json

# Functions
async def word_request(language, word):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.dictionaryapi.dev/api/v2/entries/{language}/{word}") as request:
            return(json.loads(await request.text()))

def random_hex():
    random_number = rnd.randint(0,0xffffff)
    return(random_number)

# Cog Setup
class Dictionary(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['dictionary', 'dictionarysearch'])
    @commands.cooldown(2.0, 6.0, commands.BucketType.user)
    async def ds(self, ctx, word: str):
        data = await word_request('en_US', word)
        data = data[0]

        embed = discord.Embed(
           title=f"__{word.capitalize()}__ Search",
            timestamp=dt.datetime.utcnow(),
            color=random_hex(),
            url=data['phonetics'][0]['audio']
        )
        
        for meaning in data['meanings']:
            synonoms = []
            if 'synonyms' in meaning['definitions'][0]:
                for synonom in meaning['definitions'][0]['synonyms']:
                    synonoms.append(synonom.capitalize())
            
            else:
                synonoms = 'None'

            if 'example' in meaning['definitions'][0]:
                example = meaning['definitions'][0]['example'].capitalize()
            else:
                example = 'None'

            embed.add_field(
                name=meaning['partOfSpeech'].capitalize(),
                value=f"""{meaning['definitions'][0]['definition'].capitalize()}
                > *{example}*
                Synonoms: {str(synonoms).replace('[', '').replace(']', '').replace("'", "")}""",
                inline=False
            )
        
        return await ctx.send(embed=embed)

    @ds.error
    async def ds_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cooldown_embed = discord.Embed(
                title=f"Dictionary Search is on Cooldown",
                description=f"Try again in {error.retry_after:.2f} seconds.", 
                timestamp = dt.datetime.utcnow(),
                color=random_hex()
            )
            return await ctx.send(embed=cooldown_embed)

# Adding the Cog
def setup(bot):
    bot.add_cog(Dictionary(bot))