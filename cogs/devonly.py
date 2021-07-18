"""
Tenshi Discord Bot
Copyright (C) 2021 Ben Z.
This software is licensed under Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)
"""

import discord
from discord.ext import commands
import datetime
from cogs.colors import *
import unicodedata
import io
from contextlib import redirect_stdout
import textwrap
import traceback

def cleanup_code(content):
    """Automatically removes code blocks from the code"""
    # remove ```py\n```
    if content.startswith("```") and content.endswith("```"):
        return "\n".join(content.split("\n")[1:-1])

class DevOnly(commands.Cog):
    """Commands that are for bot development"""
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @commands.is_owner()
    async def dev(self, ctx):
        """Commands thats sole purpose is for me to experiment."""
        if not ctx.invoked_subcommand:
            embed = discord.Embed(
            title=f"{ctx.author.display_name} is the Dev",
            description=f"This message is only displayable by him.",
            timestamp=datetime.datetime.utcnow(),
            color=c_get_color("black")
        )
            await ctx.send(embed=embed)

    @dev.error
    async def dev_error(self, ctx, error):
        """Will spam my terminal if they keep trying :P"""
        if isinstance(error, commands.CheckFailure):
            print(f"{ctx.author.name} - {ctx.author.id} ran dev command.")
            # add auto blacklist later.
    
    @dev.command(
        help="Load a cog",
        brief="Loading Cogs", 
        usage="<cog = FileName>",
        description="None",
        hidden=True
    )
    async def load(self, ctx, *, cog: str):
        try:
            self.bot.load_extension(cog)
        except Exception as e:
            embed_fail = discord.Embed(
                title=f"__{cog}__ Load Fail",
                description=f"""```diff
- {cog} loading failed
- Reason: {e}
```""",
                timestamp=datetime.datetime.utcnow(),
                color=c_random_color()
            )
            return await ctx.send(embed=embed_fail)
            
        else:
            embed = discord.Embed(
                title=f"__{cog}__ Loaded",
                description=f"""```diff
+ {cog} loaded successfuly
```""",
                timestamp=datetime.datetime.utcnow(),
                color=c_random_color()
            )
            await ctx.send(embed=embed)

    @dev.command(
        help="Unload a cog",
        brief="Unloading Cogs", 
        usage="<cog = FileName>",
        description="None",
        hidden=True
    )
    async def unload(self, ctx, *, cog: str):
        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            embed_fail = discord.Embed(
                title=f"__{cog}__ Unload Fail",
                description=f"""```diff
- {cog} unloading failed
- Reason: {e}
```""",
                timestamp=datetime.datetime.utcnow(),
                color=c_random_color()
            )
            return await ctx.send(embed=embed_fail)

        else:
            embed = discord.Embed(
                title=f"__{cog}__ Unloaded",
                description=f"""```diff
+ {cog} unloaded successfully
```""",
                timestamp=datetime.datetime.utcnow(),
                color=c_random_color()
            )
            await ctx.send(embed=embed)

    @dev.command(
        help="Unload then Load a cog",
        brief="Reloading Cogs", 
        usage="<cog = FileName>",
        description="None",
        hidden=True
    )
    async def reload(self, ctx, *, cog: str):
        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            embed_fail = discord.Embed(
                title=f"__{cog}__ Reload Fail",
                description=f"""```diff
- {cog} reloading failed
- Reason: {e}
```""",
                timestamp=datetime.datetime.utcnow(),
                color=c_random_color()
            )
            return await ctx.send(embed=embed_fail)

        else:
            embed = discord.Embed(
                title=f"__{cog}__ Reloaded",
                description=f"""```diff
+ {cog} reloaded successfully
```""",
                timestamp=datetime.datetime.utcnow(),
                color=c_random_color()
            )
            return await ctx.send(embed=embed)

    @dev.command(
        help="Shows a list of all servers that Tenshi is in.",
        brief="Servers List", 
        usage="",
        description="None",
        hidden=True
    )
    async def servers(self, ctx):
        servers = self.bot.guilds
        servers_var = ""
        for guild in servers:
            servers_var = f"{servers_var}\n{guild.name}"
        embed = discord.Embed(
            title=f"Tenshi Server List ============== {len(self.bot.guilds)}",
            description=f"""```
{servers_var}
```""",
            timestamp=datetime.datetime.utcnow(),
            color=c_random_color()
        )
        await ctx.send(embed=embed)

    @dev.command(
        help="Tries to reload every cog",
        brief="Syncing Cogs", 
        usage="",
        description="None",
        hidden=True
    )
    async def sync(self, ctx):
        cog_statuslist = []
        fails = 0
        success = 0
        for cog in self.bot.cog_list:
            try:
                self.bot.unload_extension(cog)
                self.bot.load_extension(cog)

            except Exception as e:
                cog_statuslist.append(f"- {cog} failed\n- {e}")
                fails += 1
            
            else:
                cog_statuslist.append(f"+ {cog} reloaded")
                success += 1

        if fails > 0:
            embed_color = c_get_color("red")
        else:
            embed_color = c_get_color("green")

        cog_visual = f"\n".join(cog_statuslist)

        embed = discord.Embed(
            title="Tenshi Sync ============================",
            description=f"""```diff
{cog_visual}```
            `{success}` cogs have been reloaded.
            `{fails}` cogs have failed loading.""",
            timestamp=datetime.datetime.utcnow(),
            color=embed_color
        )
        await ctx.send(embed=embed)

    @dev.command(
        help="Clears Terminal by making a massive space",
        brief="Terminal Cleared", 
        usage="",
        description="None",
        hidden=True
    )
    async def ct(self, ctx):
        print("\x1b[2J")
        embed = discord.Embed(
            title="Terminal Cleared",
            timestamp=datetime.datetime.utcnow(),
            color=c_get_color("black")
        )
        await ctx.send(embed=embed)

    @dev.group()
    async def status(self, ctx):
        """Set a status for the bot"""
        if not ctx.invoked_subcommand:
            await ctx.send_help("dev status")

    @status.command()
    async def playing(self, ctx, *, status:str):
        """Set a playing status"""
        try:
            await self.bot.change_presence(activity=discord.Game(name=status))
            embed = discord.Embed(
               title="Status Changed",
               description=f"""Changed successfully.""",
               timestamp=datetime.datetime.utcnow(),
               color=c_get_color("green")
            )
            await ctx.send(embed=embed)
        
        except Exception as e:
            embed_error = discord.Embed(
               title="Status Change Fail",
               description=f"""Failed
```diff
- {e}
```""",
               timestamp=datetime.datetime.utcnow(),
               color=c_get_color("red")
            )
            await ctx.send(embed=embed_error)

    @status.command()
    async def streaming(self, ctx, url: str, *, status: str):
        """Set a streaming status"""
        try:
            await self.bot.change_presence(activity=discord.Streaming(name=status, url=url))
            embed = discord.Embed(
               title="Status Changed",
               description=f"""Changed successfully.""",
               timestamp=datetime.datetime.utcnow(),
               color=c_get_color("green")
            )
            await ctx.send(embed=embed)
        
        except Exception as e:
            embed_error = discord.Embed(
               title="Status Change Fail",
               description=f"""Failed
```diff
- {e}
```""",
               timestamp=datetime.datetime.utcnow(),
               color=c_get_color("red")
            )
            await ctx.send(embed=embed_error)
    
    @status.command()
    async def listening(self, ctx, *, status: str):
        """Set a listening status"""
        try:
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=status))
            embed = discord.Embed(
               title="Status Changed",
               description=f"""Changed successfully.""",
               timestamp=datetime.datetime.utcnow(),
               color=c_get_color("green")
            )
            await ctx.send(embed=embed)
        
        except Exception as e:
            embed_error = discord.Embed(
               title="Status Change Fail",
               description=f"""Failed
```diff
- {e}
```""",
               timestamp=datetime.datetime.utcnow(),
               color=c_get_color("red")
            )
            await ctx.send(embed=embed_error)
    
    @status.command()
    async def competing(self, ctx, *, status: str):
        """Set a competing status"""
        try:
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name=status))
            embed = discord.Embed(
               title="Status Changed",
               description=f"""Changed successfully.""",
               timestamp=datetime.datetime.utcnow(),
               color=c_get_color("green")
            )
            await ctx.send(embed=embed)
        
        except Exception as e:
            embed_error = discord.Embed(
               title="Status Change Fail",
               description=f"""Failed
```diff
- {e}
```""",
               timestamp=datetime.datetime.utcnow(),
               color=c_get_color("red")
            )
            await ctx.send(embed=embed_error)

    @status.command()
    async def watching(self, ctx, *, status: str):
        """Set a watching status"""
        try:
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status))
            embed = discord.Embed(
               title="Status Changed",
               description=f"""Changed successfully.""",
               timestamp=datetime.datetime.utcnow(),
               color=c_get_color("green")
            )
            await ctx.send(embed=embed)
        
        except Exception as e:
            embed_error = discord.Embed(
               title="Status Change Fail",
               description=f"""Failed
```diff
- {e}
```""",
               timestamp=datetime.datetime.utcnow(),
               color=c_get_color("red")
            )
            await ctx.send(embed=embed_error)

    @dev.group()
    async def cache(self, ctx):
        """Recacheing Users, Prefixes, or Guilds"""
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(
                title="Re-Cache",
                description="`user`, `prefixes` or `guild`",
                timestamp=datetime.datetime.utcnow(),
                color=c_random_color()
            )
            await ctx.send(embed=embed)

    # fix once u can get methods up and running again
    @cache.command()
    async def prefix(self, ctx):
        guild_list = []
        for guild in self.bot.guilds:
            guild_list.append(str(guild.id))

        guild_list_len = len(guild_list)
        await ctx.send(f"{len(guild_list)} servers retrieved from discord.")

        """
        for guild_setting in server_settings.find():
            try:
                guild_list.remove(str(guild_setting["_id"]))
            except:
                pass
        """

        if guild_list_len-len(guild_list) != guild_list_len:
            await ctx.send(f"{len(guild_list)} servers not in server_settings, adding them...")
            
            """
            for guild_na in guild_list:
                server_dict = {
                    "_id": str(guild_na),
                    "prefixes": ["t>", ">"],
                    "update_channel": None
                }
                server_settings.insert_one(server_dict)
                self.bot.prefix_dict[str(guild_na)] = server_dict
            print(f"Finished adding server_settings\nProcess Finished.")
            """
        else:
            return await ctx.send(f"No guilds not detected in server_settings\nProcess Finished.")

    # fix this too
    @cache.command()
    async def user(self, ctx):
        await ctx.send(f"Starting Cache User Process.")
        user_dict = {}
        """
        for user in user_settings.find():
            user_dict.update({
                str(user["_id"]): {
                    "supporter": user["supporter"],
                    "accepted_rules": user["accepted_rules"],
                    "dm_updates": user["dm_updates"],
                    "embed_colors": user["embed_colors"]
                    }})
        """

        self.bot.user_dict = user_dict
        return await ctx.send(f"Recached Users.")

    @commands.command()
    async def charinfo(self, ctx, *, characters: str):
        """Gives you the character info"""

        def to_string(c):
            digit = f"{ord(c):x}"
            name = unicodedata.name(c, "Name not found.")
            return f"""```fix
\\U{digit:>08}
```
{c} - [{name}](http://www.fileformat.info/info/unicode/char/{digit})"""

        msg = "\n".join(map(to_string, characters))

        embed = discord.Embed(
            title="Charinfo",
            description=msg,
            timestamp=datetime.datetime.utcnow(),
            color=c_random_color()
        )
        await ctx.send(embed=embed)

    @commands.command(
        name="eval",
        aliases=["exec"]
    )
    async def _eval(self, ctx, *, code: str):
        """Evaluates code given"""

        if "```py" not in code:
            # Didn"t find a code block
            no_cb = discord.Embed(
                title="Error",
                description="Include a code block dumb fuck",
                timestamp=datetime.datetime.utcnow(),
                color=c_random_color()
            )
            return await ctx.send(embed=no_cb)

        env = {
            "bot": self.bot,
            "ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "message": ctx.message,
        }

        env.update(globals())

        code = cleanup_code(code)
        stdout = io.StringIO()

        to_compile = f"""async def func():\n{textwrap.indent(code, "  ")}"""

        try:
            exec(to_compile, env)
        except Exception as e:
            embed_e1 = discord.Embed(
                title="Error",
                description=f"""```py
{e.__class__.__name__}: {e}
```""",
                timestamp=datetime.datetime.utcnow(),
                color=c_get_color("red")
            )
            return await ctx.send(embed=embed_e1)

        func = env["func"]

        try:
            with redirect_stdout(stdout):
                out = await func()

        except Exception as e:
            value = stdout.getvalue()
            embed_e2 = discord.Embed(
                title="Error",
                description=f"""```py
{value}{traceback.format_exc()}
```""",
                timestamp=datetime.datetime.utcnow(),
                color=c_get_color("red")
            )
            return await ctx.send(embed=embed_e2)

        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction("\u2705")
            except:
                pass

            if out is None:
                if value:
                    evaluated = discord.Embed(
                        title="Evaluated",
                        description=f"""```py
{value}
```""",
                        timestamp=datetime.datetime.utcnow(),
                        color=c_get_color("green")
                    )
                    return await ctx.send(embed=evaluated)

            else:
                embed_e3 = discord.Embed(
                    title="Error",
                    description=f"""```py
{value}{out}
```""",
                    timestamp=datetime.datetime.utcnow(),
                    color=c_get_color("red")
                )
                return await ctx.send(embed=embed_e3)


# Adding the Cog
def setup(bot):
    bot.add_cog(DevOnly(bot))