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
import os


# Latest Save Data Class
class UnsplashSaveData:
    def __init__(self, savedata):
        self.savedata = savedata

    def retrieve(self):
        return(self.savedata)

# Functions
async def unsplash_random():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.unsplash.com/photos/random/?client_id={os.getenv('UnsplashToken')}") as request:
            bot.unsplash_sd = UnsplashSaveData(request.headers)
            return(json.loads(await request.text()))
    
async def unsplash_photo(type, data):
    if str.lower(type) in ["id"]:
        url_string = f"/photos/?{data}&"

    if str.lower(type) in ["search"]:
        url_string = "/search/photos/?"
        for item in data:
            parameter = item.split("=", 1)
            if str.lower(parameter[0]) in ["search", "s", "query"]:
                url_string = url_string+f"query={parameter[1]}&"
            elif str.lower(parameter[0]) in ["order", "orderby", "ob"]:
                url_string = url_string+f"order_by={parameter[1]}&"
            elif str.lower(parameter[0]) in ["orentation", "o"]:
                url_string = url_string+f"orientation={parameter[1]}&"
            elif str.lower(parameter[0]) in ["color", "c"]:
                url_string = url_string+f"color={parameter[1]}&"

    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.unsplash.com{url_string}client_id={os.getenv('UnsplashToken')}") as request:
            global save_data
            save_data = UnsplashSaveData(request.headers)
            return(json.loads(await request.text()))

def random_hex():
    random_number = rnd.randint(0,0xffffff)
    return(random_number)

# Cog Setup
class Unsplash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['randompfp'])
    @commands.cooldown(1.0, 5.0, commands.BucketType.user)
    async def rpfp(self, ctx):
        pfp_data = await unsplash_random()
        pfp_cut = pfp_data['urls']['raw']

        # Forcing cloudinary to cache
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://res.cloudinary.com/demo/image/fetch/f_png,w_516,h_516,c_fill,r_max/{pfp_cut}") as request:
                pass

        pfp_cut = f"https://res.cloudinary.com/demo/image/fetch/f_png,w_516,h_516,c_fill,r_max/{pfp_cut}"

        embed = discord.Embed(
            title=f"{pfp_data['alt_description'].capitalize()}",
            description=f"""Photo by [{pfp_data['user']['username']}]({pfp_data['links']['html']}?utm_source=Tenshi&utm_medium=referral) on [Unsplash](https://unsplash.com/?utm_source=Tenshi&utm_medium=referral)
            :eyes: {pfp_data['views']:,}
            <:join_tenshi:820026603563122708> {pfp_data['downloads']:,}""",
            color=int(f"0x{pfp_data['color'].replace('#', '')}", 16),
            url=pfp_data['urls']['full']
        )
        embed.set_image(
            url=pfp_cut
        )
        embed.set_footer(
            text=f"Requested by {ctx.author.name} - Photo ID: {pfp_data['id']}",
            icon_url=ctx.author.avatar_url
        )
        return await ctx.send(embed=embed)
        
    @rpfp.error
    async def rpfp_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cooldown_embed = discord.Embed(
                title=f"RPFP is on Cooldown",
                description=f"""Try again in {error.retry_after:.2f} seconds.
                This command requires multiple requests to be made hence the long cooldown. 
                Please be patient""", 
                timestamp = dt.datetime.utcnow(),
                color=random_hex()
            )
            return await ctx.send(embed=cooldown_embed)

    @commands.command()
    @commands.cooldown(1.0, 5.0, commands.BucketType.user)
    async def unsplash(self, ctx, parameter=None):
        if not parameter:
            return

        if str.lower(parameter) in ['status']:
            data = ctx.bot.unspalsh_sd.retrieve()
            status_embed = discord.Embed(
                title="Latest Unsplash Request Status",
                description=f"""```diff
! Connection Type - {data['Connection']} !
*** Server - {data['Server']} ***
+ Requests - {data['X-Ratelimit-Remaining']}/{data['X-Ratelimit-Limit']} +
! Request Time - {data['Date']} !
```
                Please note this request limit is applied to every server and is updated after every unsplash related request.""",
                timestamp=dt.datetime.utcnow(),
                color=random_hex()
            )
            return await ctx.send(embed=status_embed)

    @commands.group()
    @commands.cooldown(1.0, 7.0, commands.BucketType.user)
    async def photo(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(
                title="Unsplash Photos",
                description=f"""Search for photos by using the following subcommands""",
                timestamp=dt.datetime.utcnow(),
                color=random_hex()
            )
            return await ctx.send(embed=embed)

    @photo.error
    async def photo_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cooldown_embed = discord.Embed(
                title=f"Photo is on Cooldown",
                description=f"""Try again in {error.retry_after:.2f} seconds.""", 
                timestamp = dt.datetime.utcnow(),
                color=random_hex()
            )
            return await ctx.send(embed=cooldown_embed)

    @photo.command()
    async def id(self, ctx, id: str):
        data = await unsplash_photo("id", id)
        embed = discord.Embed(
            title=f"{data['alt_description'].capitalize()}",
            description=f"""Photo by [{data['user']['username']}]({data['links']['html']}?utm_source=Tenshi&utm_medium=referral) on [Unsplash](https://unsplash.com/?utm_source=Tenshi&utm_medium=referral)
            :eyes: {data['views']:,}
            <:join_tenshi:820026603563122708> {data['downloads']:,}""",
            timestamp=dt.datetime.utcnow(),
            color=int(f"0x{data['color'].replace('#', '')}", 16),
            url=data['urls']['full']
        )
        embed.set_image(url=data['urls']['regular'])
        return await ctx.send(embed=embed)
    
    @photo.command()
    async def search(self, ctx, *, data):
        if data is None:
            embed = discord.Embed(
                title="Unsplash Photos",
                description=f"""With this command you can search for photo's with a few different options.
```asciidoc
= Search for something related to what you described = 
[search=] [s=] [query=]
[search=Cherry Blossoms]
= Order the results with either relevant (r) or latest (l) =
[orderby=] [order=] [ob=]
[orderby=r]
= Orientation of the photo, use landscape (l), portrait=(p) and squarish(s) =
[orientation=] [o=]
[orientation=s]
= General color of the photo, valid options are black_and_white (baw), black, white, yellow, orange, red, purple, magenta, green, teal, and blue =
[color=] [c=]
[color=teal]
```
                You can include all 4 or just 1 though at least one of them is needed, **make sure to separate them with a comma.**
                **Do not use a comma other then separating multiple queries :p In addition don't include the []**
                Example: `t>photo search s=Cherry Blossoms, o=l`""",
                timestamp=dt.datetime.utcnow(),
                color=random_hex()
            )
            return await ctx.send(embed=embed)
        
        search_data = data

        if "," in search_data:
            search_data = search_data.split(",")
        else:
            search_data = [f"{search_data}"]
        
        unsplash_data = await unsplash_photo("search", search_data)
        unsplash_data = unsplash_data['results'][0]

        unsplash_embed = discord.Embed(
            title=f"{unsplash_data['alt_description'].capitalize()}",
            description=f"""Photo by [{unsplash_data['user']['username']}]({unsplash_data['links']['html']}?utm_source=Tenshi&utm_medium=referral) on [Unsplash](https://unsplash.com/?utm_source=Tenshi&utm_medium=referral)""",
            timestamp=dt.datetime.utcnow(),
            color=int(f"0x{unsplash_data['color'].replace('#', '')}", 16),
            url=unsplash_data['urls']['full']
        )
        unsplash_embed.set_image(url=unsplash_data['urls']['regular'])
        return await ctx.send(embed=unsplash_embed)     

# Adding the Cog
def setup(bot):
    bot.add_cog(Unsplash(bot))