"""
Tenshi Discord Bot
Copyright (C) 2021 Ben Z.
This software is licensed under Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)
"""

import discord
from discord.ext import commands, menus
import datetime
import aiohttp
from cogs.colors import *
import asyncio


def format_time(iso: str):
    text = datetime.datetime.fromisoformat(iso).strftime("%c")
    return text

def format_title(eng, jap):
    """Just a quick function to reformat titles"""
    if eng == jap:
        return eng
    else:
        return f"{eng}/{jap}"

async def get_user(username):
    """Get a users profile"""
    async with aiohttp.ClientSession() as cs:
        async with cs.get(f"https://api.jikan.moe/v4/users/{username}") as request:
            if request.status in [200, 404]:
                return await request.json()
            else:
                print(f"[ERROR] [{datetime.datetime.utcnow()}]\nError Code: {request.status}\n{await request.json()}")
                return None

async def get_anime(id):
    """Retrieve an anime by its given ID"""
    async with aiohttp.ClientSession() as cs:
        async with cs.get(f"https://api.jikan.moe/v4/anime/{id}") as request:
            if request.status == 200:
                return await request.json()
            else:
                print(f"[ERROR] [{datetime.datetime.utcnow()}]\nError Code: {request.status}\n{await request.json()}")
                return None

async def get_user_stats(username):
    """Retrieve an anime by its given ID"""
    async with aiohttp.ClientSession() as cs:
        async with cs.get(f"https://api.jikan.moe/v4/users/{username}/statistics") as request:
            if request.status == 200:
                return await request.json()
            else:
                print(f"[ERROR] [{datetime.datetime.utcnow()}]\nError Code: {request.status}\n{await request.json()}")
                return None

async def search_user(user):
    """Just search for a regular anime with a string"""
    async with aiohttp.ClientSession() as cs:
        async with cs.get(f"https://api.jikan.moe/v4/users?q={user}") as request:
            if request.status in [200, 404]:
                return await request.json()
            else:
                print(f"[ERROR] [{datetime.datetime.utcnow()}]\nError Code: {request.status}\n{await request.json()}")
                return None

async def search_anime(anime):
    """Search for a user"""
    async with aiohttp.ClientSession() as cs:
        async with cs.get(f"https://api.jikan.moe/v4/anime?q={anime}") as request:
            if request.status == 200:
                return await request.json()
            else:
                print(f"[ERROR] [{datetime.datetime.utcnow()}]\nError Code: {request.status}\n{await request.json()}")
                return None

async def anime_characters(anime):
    """Not finished"""
    async with aiohttp.ClientSession() as cs:
        async with cs.get(f"https://api.jikan.moe/v4/anime?q={anime}") as request:
            if request.status == 200:
                return await request.json()
            else:
                print(f"[ERROR] [{datetime.datetime.utcnow()}]\nError Code: {request.status}\n{await request.json()}")
                return None

async def get_user_updates(username):
    """Not finished"""
    async with aiohttp.ClientSession() as cs:
        async with cs.get(f"https://api.jikan.moe/v4/users/{username}/userupdates") as request:
            if request.status == 200:
                return await request.json()
            else:
                print(f"[ERROR] [{datetime.datetime.utcnow()}]\nError Code: {request.status}\n{await request.json()}")
                return None

async def get_anime_picture(image_url):
    """Use trace.moe to try and trace the images origins"""
    async with aiohttp.ClientSession() as cs:
        async with cs.get(f"https://trace.moe/api/search?url={image_url}") as request:
            if request.status == 200:
                return await request.json()
            else:
                print(f"[ERROR] [{datetime.datetime.utcnow()}]\nError Code: {request.status}\n{await request.json()}")
                return None

def gen_anime_search(data):
    title = format_title(data["title"], data["title_english"])

    anime_embed = discord.Embed(
        title=f"""{title} - {data["mal_id"]}""",
        url=data["url"],
        color=c_random_color()
    )
    anime_embed.set_thumbnail(
        url=data["images"]["jpg"]["large_image_url"]
    )
    if not data["trailer"]["images"]["maximum_image_url"]:
        pass
    else:
        anime_embed.set_image(
            url=data["trailer"]["images"]["maximum_image_url"]
        )
    anime_embed.add_field(
        name="Info",
        value=f""":tv: {data["type"]} - {data["source"]}
        :star: **Score:** {data["score"]}/10
        :medal: **Rank:** {data["rank"]:,} 
        :trophy: **Popularity:** {data["popularity"]:,}
        :busts_in_silhouette: **Members:** {data["members"]:,}
        :tickets: **Favorites:** {data["favorites"]:,}
        :film_frames: **Trailer Link** {data["trailer"]["url"]}""",
        inline=False
    )
    anime_embed.add_field(
        name="Episode Info",
        value=f"""{data["episodes"]} with {data["duration"]}""",
        inline=False
    )
    if data["airing"]:
        airing_text = "Airing"
    else:
        airing_text = "Aired"
    
    if not data["broadcast"]["string"]:
        airing_text2 = ""
    else:
        airing_text2 = f"""{airing_text} {data["broadcast"]["string"]}"""

    anime_embed.add_field(
        name="Airing Info",
        value=f""":loudspeaker: {data["status"]}
        {airing_text} from {data["aired"]["string"]}
        {airing_text2}""",
        inline=False
    )
    anime_embed.set_footer(
        text=f"""Rated {data["rating"]}""",
    )
    return anime_embed


class AnimeSearchPage(menus.Menu):
    """A search command that bases itself on a list of them, will then allow you to click another button to run another command"""
    def __init__(self, data, ctx, bot):
        super().__init__(timeout=60.0, delete_message_after=True)
        self.data = data
        self.ctx = ctx
        self.bot = bot
        self.page_number = 0
        self.page_cap = len(data) - 1

    async def send_initial_message(self, ctx, channel):
        """The initial message that we send"""
        anime_embed = gen_anime_search(self.data[self.page_number])
        return await channel.send(embed=anime_embed)

    @menus.button(":back_button_triangle:843677189533597749")
    async def on_back(self, payload):
        """When we click to go back a page"""
        if self.page_number > 1:
            self.page_number -= 1
        else:
            self.page_number = self.page_cap
        anime_embed = gen_anime_search(self.data[self.page_number])
        await self.message.edit(embed=anime_embed)
        return await asyncio.sleep(1)
    
    @menus.button(":pause:820003279941271592")
    async def on_stop(self, payload):
        """If users wanna be nice and stop the embed tracking reactions when its done..."""
        self.stop()

    @menus.button(":play_button_triangle:820007884641402920")
    async def on_next(self, payload):
        """When users click next"""
        if self.page_number < self.page_cap:
            self.page_number += 1
        else:
            self.page_number = 0
        anime_embed = gen_anime_search(self.data[self.page_number])
        await self.message.edit(embed=anime_embed)
        return await asyncio.sleep(1)
    
    @menus.button("\U00002705")
    async def on_confirm(self, payload):
        """When users would like to confirm the anime they would like to search"""
        cmd = self.bot.get_command("anime search")
        await cmd(self.ctx, request=str(self.data[self.page_number]["mal_id"]))
        self.stop()

class AnimeSearchID(menus.Menu):
    """Options to display different fields for an embed containing data about an anime..."""
    def __init__(self, data):
        super().__init__(timeout=60.0)
        self.data = data
    
    async def send_initial_message(self, ctx, channel):
        """The initial message that's sent"""
        title = format_title(self.data["title"], self.data["title_english"])

        anime_embed = discord.Embed(
            title=f""":page_facing_up: {title} - {self.data["mal_id"]}""",
            url=self.data["url"],
            color=c_random_color()
        )
        anime_embed.set_thumbnail(
            url=self.data["images"]["jpg"]["large_image_url"]
        )
        if not self.data["trailer"]["images"]["maximum_image_url"]:
            pass
        else:
            anime_embed.set_image(
                url=self.data["trailer"]["images"]["maximum_image_url"]
            )
        anime_embed.add_field(
            name="Info",
            value=f""":tv: {self.data["type"]} - {self.data["source"]}
            :star: **Score:** {self.data["score"]}/10
            :medal: **Rank:** {self.data["rank"]:,} 
            :trophy: **Popularity:** {self.data["popularity"]:,}
            :busts_in_silhouette: **Members:** {self.data["members"]:,}
            :tickets: **Favorites:** {self.data["favorites"]:,}
            :film_frames: **Trailer Link** {self.data["trailer"]["url"]}""",
            inline=False
        )
        anime_embed.add_field(
            name="Episode Info",
            value=f"""{self.data["episodes"]} with {self.data["duration"]}""",
            inline=False
        )
        if self.data["airing"]:
            airing_text = "Airing"
        else:
            airing_text = "Aired"

        if not self.data["broadcast"]["string"]:
            airing_text2 = ""
        else:
            airing_text2 = f"""{airing_text} {self.data["broadcast"]["string"]}"""

        anime_embed.add_field(
            name="Airing Info",
            value=f""":loudspeaker: {self.data["status"]}
            {airing_text} from {self.data["aired"]["string"]}
            {airing_text2}""",
            inline=False
        )
        anime_embed.set_footer(
            text=f"""Rated {self.data["rating"]}""",
        )
        return await channel.send(embed=anime_embed)

    @menus.button("\U0001f4c4") # page_facing_up
    async def on_basic(self, payload):
        """Just the basic embed, shows all the stuff we wanted..."""
        title = format_title(self.data["title"], self.data["title_english"])

        anime_embed = discord.Embed(
            title=f""":page_facing_up: {title} - {self.data["mal_id"]}""",
            url=self.data["url"],
            color=c_random_color()
        )
        anime_embed.set_thumbnail(
            url=self.data["images"]["jpg"]["large_image_url"]
        )
        anime_embed.set_image(
            url=self.data["trailer"]["images"]["maximum_image_url"]
        )
        anime_embed.add_field(
            name="Info",
            value=f""":tv: {self.data["type"]} - {self.data["source"]}
            :star: **Score:** {self.data["score"]}/10
            :medal: **Rank:** {self.data["rank"]:,} 
            :trophy: **Popularity:** {self.data["popularity"]:,}
            :busts_in_silhouette: **Members:** {self.data["members"]:,}
            :tickets: **Favorites:** {self.data["favorites"]:,}
            :film_frames: **Trailer Link** {self.data["trailer"]["url"]}""",
            inline=False
        )
        anime_embed.add_field(
            name="Episode Info",
            value=f"""{self.data["episodes"]} with {self.data["duration"]}""",
            inline=False
        )
        if self.data["airing"]:
            airing_text = "Airing"
        else:
            airing_text = "Aired"
        
        if not self.data["broadcast"]["string"]:
            airing_text2 = ""
        else:
            airing_text2 = f"""{airing_text} {self.data["broadcast"]["string"]}"""

        anime_embed.add_field(
            name="Airing Info",
            value=f""":loudspeaker: {self.data["status"]}
            {airing_text} from {self.data["aired"]["string"]}
            {airing_text2}""",
            inline=False
        )
        anime_embed.set_footer(
            text=f"""Rated {self.data["rating"]}""",
        )
        await self.message.edit(embed=anime_embed)
        return await asyncio.sleep(1)

    @menus.button("\U0001f4dc") # Scroll
    async def on_description(self, payload):
        """Removing original image to save on space and allow the embed to be wider, we then display a description"""
        title = format_title(self.data["title"], self.data["title_english"])
        anime_embed = discord.Embed(
            title=f""":scroll: {title} - {self.data["mal_id"]}""",
            description=self.data["synopsis"],
            url=self.data["url"],
            color=c_random_color()
        )
        anime_embed.set_thumbnail(
            url=self.data["images"]["jpg"]["large_image_url"]
        )
        anime_embed.set_footer(
            text=f"""Rated {self.data["rating"]}""",
        )
        await self.message.edit(embed=anime_embed)
        return await asyncio.sleep(1)

    @menus.button("\U0001f3a5")
    async def on_creation_info(self, payload):
        """Producers, licensors and studios."""
        title = format_title(self.data["title"], self.data["title_english"])
        anime_embed = discord.Embed(
            title=f""":movie_camera: {title} - {self.data["mal_id"]}""",
            url=self.data["url"],
            color=c_random_color()
        )
        anime_embed.set_thumbnail(
            url=self.data["images"]["jpg"]["large_image_url"]
        )
        anime_embed.set_footer(
            text=f"""Rated {self.data["rating"]}""",
        )

        producers = ""
        licensors = ""
        studios = ""

        for producer in self.data["producers"]:
            producers = f"""{producers}\n[{producer["name"]} - {producer["mal_id"]}]({producer["url"]})"""

        for licensor in self.data["licensors"]:
            licensors = f"""{licensors}\n[{licensor["name"]} - {licensor["mal_id"]}]({licensor["url"]})"""

        for studio in self.data["studios"]:
            studios = f"""{studios}\n[{studio["name"]} - {studio["mal_id"]}]({studio["url"]})"""

        if producers == "":
            producers = "None"
        if licensors == "":
            licensors = "None"
        if studios == "":
            studios = "None"

        anime_embed.add_field(
            name="Producers",
            value=producers,
            inline=False
        )

        anime_embed.add_field(
            name="Licensors",
            value=licensors,
            inline=False
        )
        anime_embed.add_field(
            name="Studios",
            value=studios,
            inline=False
        )
        await self.message.edit(embed=anime_embed)
        return await asyncio.sleep(1)

    @menus.button(":pause:820003279941271592")
    async def on_stop(self, payload):
        """If users wanna be nice and stop us processing this"""
        self.stop()

def gen_user_page(data):
    """Generating a user page for ease of access"""
    embed = discord.Embed(
        title=data["username"],
        url=data["url"],
        color=c_random_color()
    )
    embed.set_thumbnail(
        url=data["images"]["jpg"]["image_url"]
    )
    embed.set_footer(
        text=f"""Last Online {format_time(data["last_online"])}"""
    )
    return embed

class UserSearch(menus.Menu):
    """Searches and displays users from given data"""
    def __init__(self, data):
        super().__init__(timeout=60.0, delete_message_after=True)
        self.data = data
        self.page_number = 0
        self.page_cap = len(data) - 1

    async def send_initial_message(self, ctx, channel):
        """Initial message that's sent"""
        user_embed = gen_user_page(self.data[self.page_number])
        return await channel.send(embed=user_embed)

    @menus.button(":back_button_triangle:843677189533597749")
    async def on_back(self, payload):
        """When we click to go back a page"""
        if self.page_number > 1:
            self.page_number -= 1
        else:
            self.page_number = self.page_cap
        anime_embed = gen_user_page(self.data[self.page_number])
        await self.message.edit(embed=anime_embed)
        return await asyncio.sleep(1)
    
    @menus.button(":pause:820003279941271592")
    async def on_stop(self, payload):
        """If users wanna be nice and stop the embed tracking reactions when its done..."""
        self.stop()

    @menus.button(":play_button_triangle:820007884641402920")
    async def on_next(self, payload):
        """When users click next"""
        if self.page_number < self.page_cap:
            self.page_number += 1
        else:
            self.page_number = 0
        anime_embed = gen_user_page(self.data[self.page_number])
        await self.message.edit(embed=anime_embed)
        return await asyncio.sleep(1)
    
    #@menus.button("\U00002705")
    #async def on_confirm(self, payload):
        #"""When users would like to confirm the anime they would like to search"""
        #cmd = self.bot.get_command("anime search")
        #await cmd(self.ctx, request=str(self.data[self.page_number]["mal_id"]))
        # Add the command later
        #self.stop()


class UserPage(menus.Menu):
    """View and display user statistics and pages"""
    def __init__(self, data):
        super().__init__(timeout=60)
        self.data = data
        self.stats = None
        self.user_updates = None

    async def send_initial_message(self, ctx, channel):
        user_embed = discord.Embed(
            title=f""":page_facing_up: {self.data["username"]} - {self.data["mal_id"]}""",
            url=self.data["url"],
            description=f"""Joined {format_time(self.data["joined"])}""",
            color=c_random_color()
        )
        user_embed.set_thumbnail(
            url=self.data["images"]["jpg"]["image_url"]
        )
        user_embed.set_footer(
            text=f"""Last Online {format_time(self.data["last_online"])}"""
        )
        user_embed.add_field(
            name="Gender",
            value=str(self.data["gender"])
        )
        user_embed.add_field(
            name=":map: Location",
            value=str(self.data["location"])
        )
        if self.data["birthday"]:
            bday = format_time(self.data["birthday"])
        else:
            bday = str(self.data["birthday"])
        user_embed.add_field(
            name=":gift: Birthday!",
            value=bday
        )
        return await channel.send(embed=user_embed)

    @menus.button("\U0001f4c4")
    async def on_profile(self, payload):
        user_embed = discord.Embed(
            title=f""":page_facing_up: {self.data["username"]} - {self.data["mal_id"]}""",
            url=self.data["url"],
            description=f"""Joined {format_time(self.data["joined"])}""",
            color=c_random_color()
        )
        user_embed.set_thumbnail(
            url=self.data["images"]["jpg"]["image_url"]
        )
        user_embed.set_footer(
            text=f"""Last Online {format_time(self.data["last_online"])}"""
        )
        user_embed.add_field(
            name="Gender",
            value=str(self.data["gender"])
        )
        user_embed.add_field(
            name=":map: Location",
            value=str(self.data["location"])
        )
        if self.data["birthday"]:
            bday = format_time(self.data["birthday"])
        else:
            bday = str(self.data["birthday"])
        user_embed.add_field(
            name=":gift: Birthday!",
            value=bday
        )
        await self.message.edit(embed=user_embed)
        return await asyncio.sleep(1)

    @menus.button("\U0001f4c8")
    async def on_stat(self, payload):
        if not self.stats:
            self.stats = await get_user_stats(self.data["username"])
            self.stats = self.stats["data"]
        embed = discord.Embed(
            title=f""":chart_with_upwards_trend: {self.data["username"]} - {self.data["mal_id"]}""",
            url=self.data["url"],
            color=c_random_color()
        )
        embed.add_field(
            name=f"""Anime - {self.stats["anime"]["total_entries"]}""",
            value=f""":star: **Average Rating:** {self.stats["anime"]["mean_score"]}
            :film_frames: **Watching:** {self.stats["anime"]["watching"]}
            :white_check_mark: **Completed:** {self.stats["anime"]["completed"]}
            :part_alternation_mark: **On Hold:** {self.stats["anime"]["on_hold"]}
            :no_entry_sign: **Dropped:** {self.stats["anime"]["dropped"]}
            :thought_balloon: **Plan To Watch:** {self.stats["anime"]["plan_to_watch"]}
            :recycle: **ReWatched:** {self.stats["anime"]["rewatched"]}
            :dvd: **Episodes Watched:** {self.stats["anime"]["episodes_watched"]}""",
            inline=True
        )
        embed.add_field(
            name=f"""Manga - {self.stats["manga"]["total_entries"]}""",
            value=f""":star: **Average Rating:** {self.stats["manga"]["mean_score"]}
            :book: **Reading:** {self.stats["manga"]["reading"]}
            :white_check_mark: **Completed:** {self.stats["manga"]["completed"]}
            :part_alternation_mark: **On Hold:** {self.stats["manga"]["on_hold"]}
            :no_entry_sign: **Dropped:** {self.stats["manga"]["dropped"]}
            :thought_balloon: **Plan To Read:** {self.stats["manga"]["plan_to_read"]}
            :recycle: **ReRead:** {self.stats["manga"]["reread"]}
            :books: **Chapters Read:** {self.stats["manga"]["chapters_read"]}""",
            inline=True
        )
        await self.message.edit(embed=embed)
        return await asyncio.sleep(1)

    @menus.button("\U0001f195")
    async def on_user_updates(self, payload):
        if not self.user_updates:
            self.user_updates = await get_user_updates(self.data["username"])
            self.user_updates = self.user_updates["data"]
        embed = discord.Embed(
            title=f""":new: {self.data["username"]} - {self.data["mal_id"]}""",
            url=self.data["url"],
            color=c_random_color()
        )
        for anime in self.user_updates["anime"]:
            date = format_time(anime["date"])
            embed.add_field(
                name=f"""Anime - {anime["entry"]["title"]} - {anime["entry"]["mal_id"]}""",
                value=f"""{anime["entry"][""]}
                [`{date}`]({anime["entry"]["url"]})""",
                inline=True
            )
  
        await self.message.edit(embed=embed)
        return await asyncio.sleep(1)

class Anime(commands.Cog):
    """Anime related commands"""
    def __init__(self, bot):
        self.bot = bot

# Anime things
    @commands.group()
    async def anime(self, ctx):
        """Display options for the anime command"""
        if not ctx.invoked_subcommand:
            await ctx.send_help("anime")
    
    @anime.command(
        name="search", 
        help="Use this command to search for an anime!",
        brief="Anime Search Command", 
        usage="<request = Regular Search, MAL ID, Attachment, Link>",
        description="""Searching using images and links might not always work because of heavy rate limits..."""
    )
    @commands.cooldown(1, 5.0, commands.BucketType.user)
    async def anime_search(self, ctx, *, request=None):
        """Search for an anime, will auto detect numbers for mal_ids or file attachments"""
        if not request:
            # Request needs to have an attachment, if not we tell the user they made a mistake.
            if len(ctx.message.attachments) == 0:
                # No attachments send-help
                return await ctx.send_help("anime search")
            else:
                if "image/" not in ctx.message.attachments[0].content_type:
                    invalid_format = discord.Embed(
                        tite="Error",
                        description=f"""Currently you can only search for images!
                        `{ctx.message.attachments[0].content_type.replace("image/", "")}` is not a supported file type.""",
                        color=self.bot.default_colors["red"],
                        timestamp=datetime.datetime.utcnow()
                    )
                    return await ctx.send(embed=invalid_format)
                else:
                    # We can now check the anime
                    # Not Done
                    pass

        if request.isdigit():
            # Request was a singular number we can just use that
            data = await get_anime(request)
            if not data:
                embed_error = discord.Embed(
                    title="Looks like there aren't any matches...",
                    description=f"""Sorry but we couldn't find any matches for ID: `{request}` make sure this is the correct MYANIMELIST ID""",
                    colors=self.bot.default_colors["red"],
                    timestamp=datetime.datetime.utcnow()
                )
                return await ctx.send(embed=embed_error)

            anime_page = AnimeSearchID(data["data"])
            return await anime_page.start(ctx)

        else:
            # Now we know its just a regular text search result so we use this
            data = await search_anime(request)
            if not data["data"]:
                embed_error2 = discord.Embed(
                    title="Looks like there aren't any matches...",
                    description=f"""Sorry but we couldn't find any matches for `{request}` try being as specific possible and make sure to spell everything correctly!""",
                    colors=self.bot.default_colors["red"],
                    timestamp=datetime.datetime.utcnow()
                )
                return await ctx.send(embed=embed_error2)
            else:
                anime_start = AnimeSearchPage(data["data"], ctx, self.bot)
                await anime_start.start(ctx)

    @anime.group()
    async def user(self, ctx):
        """MyAnimeList User related commands"""
        if not ctx.invoked_subcommand:
            await ctx.send_help("user")
    
    @user.command(
        name="search"
    )
    async def user_search(self, ctx, username: str):
        """Search for a user"""
        data = await get_user(username)
        if "status" in data or not data:
            # We recieved a 404 but we still check anyways just to make sure
            if data["status"] == 404 or not data:
                # We couldn't find them so now we begin a search
                data = await search_user(username)
                user_start = UserSearch(data["data"])
                return await user_start.start(ctx)
        else:
            data = data["data"]
            user_page = UserPage(data)
            await user_page.start(ctx)


def setup(bot):
    bot.add_cog(Anime(bot))