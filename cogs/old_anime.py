# Discord Imports
import discord
from discord.ext import commands

# Other
import math
import datetime as dt
import random as rnd
import asyncio
import requests
import validators as vtr
import urllib.parse as url
import json

# Functions
def random_hex():
    random_number = rnd.randint(0,0xffffff)
    return(random_number)

def mal_request(id):
    id = str(id)
    response = requests.get("https://api.jikan.moe/v3/anime/"+id)
    data = json.loads(response.text)
    return(data)

def mal_search(name):
    name = str(name)
    response = requests.get("https://api.jikan.moe/v3/search/anime?q="+name+"&page=1")
    data = json.loads(response.text)
    return(data)

def mal_charactersearch(name):
    name = str(name)
    response = requests.get("https://api.jikan.moe/v3/search/character?q="+name)
    data = json.loads(response.text)
    return(data)

# Cog Setup
class Anime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['animepicturesearch'])
    async def aps(self, ctx, imageurl: str):
        await ctx.message.delete()
        valid = vtr.url(imageurl)

        if 'gif' in imageurl:
            embed_gif = discord.Embed(
                title='Link Error',
                description='It seems like your link is a GIF which is currently not allowed!',
                timstamp=dt.datetime.utcnow(),
                color=random_hex()
                )
            msg = await ctx.send(embed=embed_gif)
            await asyncio.sleep(5)
            await msg.delete()
            return

        if 'vid' in imageurl or 'video' in imageurl:
            embed_vid = discord.Embed(
                title='Link Error',
                description="It seems like your link is a VIDEO which won't work with this, please change it to an image format",
                timstamp=dt.datetime.utcnow(),
                color=random_hex()
                )
            msg = await ctx.send(embed=embed_vid)
            await asyncio.sleep(5)
            await msg.delete()
            return
        
        if valid:
            anime = requests.get("https://trace.moe/api/search?url="+imageurl)
            anime = json.loads(anime.text)

            if 'Invalid Image' in anime:
                embed_search_404 = discord.Embed(
                    title='Search Failure',
                    description="Nothing Found",
                    timestamp=dt.datetime.utcnow(),
                    color=random_hex()
                )
                await ctx.send(embed=embed_search_404)
                return

            anime_info = anime['docs']
            anime_info = anime_info[0]

            if not ctx.channel.is_nsfw() and anime_info['is_adult']:
                embed_nsfw = discord.Embed(
                    title='Nsfw',
                    description='It seems like your anime contains NSFW! Please run this in an NSFW channel',
                    timstamp=dt.datetime.utcnow(),
                    color=random_hex()
                    )
                msg = await ctx.send(embed=embed_nsfw)
                await asyncio.sleep(5)
                await msg.delete()
                return
            
            image_searched = anime['RawDocsCount'] 
            image_search_time = anime['RawDocsSearchTime'] 
            image_compare_time = anime['ReRankSearchTime']
            
            if image_search_time == 0:
                image_search_time = 'less then 1 second'
            if image_compare_time == 0:
                image_compare_time = 'less then 1 second'

            embed = discord.Embed(
                title='Anime Picture Search',
                url=imageurl,
                color=random_hex()
                )
            embed.set_footer(
                text=f'{image_searched} images searched in {image_search_time}, compared results in {image_compare_time}'
                )
            embed.add_field(
                name=f"**{anime_info['title_romaji']}/{anime_info['title_english']} - Episode {anime_info['episode']}**",
                value=f"""Video Time: `{math.trunc(anime_info['at'])}` seconds (`{anime_info['from']}-{anime_info['to']}`) 
                Similarity Rate: `{math.trunc(anime_info['similarity']*10000)/100}%`
                [`Video Clip`](https://media.trace.moe/video/{anime_info['anilist_id']}/{url.quote(anime_info['filename'])}?t={anime_info['at']}&token={anime_info['tokenthumb']}&size=l)""",
                inline=False
                )
            embed.add_field(
                name='Other Websites:',
                value=f"""[`AniList`](https://anilist.co/anime/{anime_info['anilist_id']})
                [`MyAnimeList`](https://myanimelist.net/anime/{anime_info['mal_id']})
                Run `>anime info {anime_info['mal_id']}` for more info!""",
                inline=False
                )
            embed.set_image(
                url=f"https://media.trace.moe/image/{anime_info['anilist_id']}/{url.quote(anime_info['filename'])}?t={anime_info['at']}&token={anime_info['tokenthumb']}&size=l"
                )
            embed.set_thumbnail(
                url=imageurl
                )
            await ctx.send(embed=embed)
            return
        else: 
            embed_error = discord.Embed(
                title='Link Error',
                description='It seems like your link is invalid! Please make sure its an actual image link please!',
                timstamp=dt.datetime.utcnow(),
                color=random_hex()
                )
            msg = await ctx.send(embed=embed_error)
            await asyncio.sleep(5)
            await msg.delete()
            return

    @commands.command(aliases=['mal'])
    async def anime(self, ctx, parameter='None', p1='None', p2='None', p3='None'):
        if str.lower(parameter) == 'info':
            data = mal_request(p1)
            aired_data = data['aired']
            embed = discord.Embed(
                title=f"{data['title']}/{data['title_english']}",
                description=f"{data['synopsis']}",  
                url=data['url'],
                timestamp=dt.datetime.utcnow(),
                color=random_hex()
                )
            if data['trailer_url']:
                trailer=f"[`Trailer`]({data['trailer_url']})"
            else:
                trailer=''
            if data['title_english']:
                clip_link=f"[`Click Me!`](https://kissanimefree.to/{data['title_english'].replace(' ', '-')})"
            elif data['title']:
                clip_link=f"[`Click Me!`](https://kissanimefree.to/{data['title'].replace(' ', '-')})"
            else: 
                clip_link=f"This anime doesn't have a watchable link!"
            embed.add_field(
                name="Info",
                value=f"""Type: {data['type']} - {data['source']}
                Status: {data['status']} ({aired_data['string']})
                Episodes: {data['episodes']} ({data['duration']})
                Age Rating: {data['rating']}
                
                Score: {data['score']} (Scored by {data['scored_by']} Users)
                Ranked: {data['rank']}
                Popularity: {data['popularity']}
                Members: {data['members']}
                Favorites: {data['favorites']}
                {trailer}
                Watch It: {clip_link}
                """,
                inline=False
                )
            embed.set_thumbnail(
                url=data['image_url']
                )
            await ctx.send(embed=embed)
            return

        if str.lower(parameter) == 'search':
            data = mal_search(p1)

            if 'status' in data and data['status'] == 404:
                embed_search_404 = discord.Embed(
                    title='Search Failure - 404',
                    description="Nothing Found",
                    timestamp=dt.datetime.utcnow(),
                    color=random_hex()
                )
                await ctx.send(embed=embed_search_404)
                return

            data = data['results']

            if p1:
                embed_search = discord.Embed(
                    title=f"Anime Search - {p1}",
                    timestamp=dt.datetime.utcnow(),
                    color=random_hex()
                )

                data_0 = data[0]
                data_1 = data[1]
                data_2 = data[2]

                embed_search.add_field(
                    name=f"{data_0['title']} - {data_0['mal_id']} - Rated: {data_0['rated']}",
                    value=f"""**Synopsis**: {data_0['synopsis']}
                    Type: {data_0['type']}
                    Airing: {data_0['airing']}
                    Episodes: {data_0['episodes']}
                    Score: {data_0['score']}
                    [MyAnimeList]({data_0['url']})
                    Run `>anime info {data_0['mal_id']}` for more info!""",
                    inline=False
                )
                embed_search.add_field(
                    name=f"{data_1['title']} - {data_1['mal_id']} - Rated: {data_1['rated']}",
                    value=f"""**Synopsis**: {data_1['synopsis']}
                    Type: {data_1['type']}
                    Airing: {data_1['airing']}
                    Episodes: {data_1['episodes']}
                    Score: {data_1['score']}
                    [MyAnimeList]({data_1['url']})
                    Run `>anime info {data_1['mal_id']}` for more info!""",
                    inline=False
                )
                embed_search.add_field(
                    name=f"{data_2['title']} - {data_2['mal_id']} - Rated: {data_2['rated']}",
                    value=f"""**Synopsis**: {data_2['synopsis']}
                    Type: {data_2['type']}
                    Airing: {data_2['airing']}
                    Episodes: {data_2['episodes']}
                    Score: {data_2['score']}
                    [MyAnimeList]({data_2['url']})
                    Run `>anime info {data_0['mal_id']}` for more info!""",
                    inline=False
                )
                embed_search.set_thumbnail(
                    url=f"{data_2['image_url']}"
                )
                await ctx.send(embed=embed_search)
                return

        if str.lower(parameter) == 'debug':
            if ctx.author.id == 360061101477724170:
                embed_debug = discord.Embed(
                    title=f"Debug",
                    description=f"""```
    Request Hash: {data['request_hash']}
    Request Cached? {data['request_cached']}
    Request Cached Time: {data['request_cache_expiry']}
    ```""",
                    timestamp=dt.datetime.utcnow(),
                    color=random_hex()
                )
                await ctx.send(embed=embed_debug)
                return
            else:
                embed_devonly = discord.Embed(
                    title="Dev Only",
                    description="Sorry but this command is for _Leg3ndary#3109 only.",
                    timestamp=dt.datetime.utcnow(),
                    color=random_hex()
                )
                await ctx.send(embed=embed_devonly)
                return
    
    @commands.command(aliases=['charactersearch', 'cs'])
    async def im(self, ctx, *, character):
        data = mal_charactersearch(character)
        page_number = character[-1]

        if page_number.isnumeric():
            page_number = int(page_number)
            page_number = page_number-1

        elif not page_number.isnumeric():
            page_number = '0'

        page_number = int(page_number)
        
        if 'status' in data and data['status'] == 404:
            embed_search_404 = discord.Embed(
                title='Search Failure - 404',
                description="Nothing Found",
                timestamp=dt.datetime.utcnow(),
                color=random_hex()
                )
            await ctx.send(embed=embed_search_404)
            return
        
        if 'status' in data and data['status'] == 500:
            embed_search_404 = discord.Embed(
            title='Search Failure - 500',
            description="Your request seems to be less then 3 characters long",
            timestamp=dt.datetime.utcnow(),
            color=random_hex()
            )
            await ctx.send(embed=embed_search_404)
            return
        
        data_results = data['results']
        name = str(data_results[page_number]['alternative_names'])
        name = name.replace("'", "")
        name = name.replace("[", "")
        name = name.replace("]", "")
        embed = discord.Embed(
            title=f"{data_results[page_number]['name']}",
            description=f"""{name}""",
            url=f"{data_results[page_number]['url']}",
            timestamp=dt.datetime.utcnow(),
            color=random_hex()
        )
        embed.set_image(
            url=f"{data_results[page_number]['image_url']}"
        )
        await ctx.send(embed=embed)
        return

# Adding the Cog
def setup(bot):
    bot.add_cog(Anime(bot))
