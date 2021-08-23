"""
Tenshi Discord Bot
Copyright (C) 2021 Ben Z.
This software is licensed under Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)
"""

import discord
from discord.ext import commands
from gears.hbot import h_get_time
from gears.cosmetics import *
import unicodedata
import io
from contextlib import redirect_stdout
import textwrap
import traceback
import json


def cleanup_code(content):
    """Automatically removes code blocks from the code"""
    # remove ```py\n```
    if content.startswith("```") and content.endswith("```"):
        return "\n".join(content.split("\n")[1:-1])

class DevOnly(commands.Cog):
    """Commands that are for bot development"""
    def __init__(self, bot):
        self.bot = bot

    @commands.group(hidden=True)
    @commands.is_owner()
    async def dev(self, ctx):
        """Commands thats sole purpose is for me to experiment."""
        if not ctx.invoked_subcommand:
            embed = discord.Embed(
            title=f"{ctx.author.display_name} is the Dev",
            description=f"This message is only displayable by him.",
            timestamp=h_get_time(),
            color=c_get_color("black")
        )
            await ctx.send(embed=embed)

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
                timestamp=h_get_time(),
                color=c_random_color()
            )
            return await ctx.send(embed=embed_fail)
            
        else:
            embed = discord.Embed(
                title=f"__{cog}__ Loaded",
                description=f"""```diff
+ {cog} loaded successfuly
```""",
                timestamp=h_get_time(),
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
                timestamp=h_get_time(),
                color=c_random_color()
            )
            return await ctx.send(embed=embed_fail)

        else:
            embed = discord.Embed(
                title=f"__{cog}__ Unloaded",
                description=f"""```diff
+ {cog} unloaded successfully
```""",
                timestamp=h_get_time(),
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
                timestamp=h_get_time(),
                color=c_random_color()
            )
            return await ctx.send(embed=embed_fail)

        else:
            embed = discord.Embed(
                title=f"__{cog}__ Reloaded",
                description=f"""```diff
+ {cog} reloaded successfully
```""",
                timestamp=h_get_time(),
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
            timestamp=h_get_time(),
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
            timestamp=h_get_time(),
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
            timestamp=h_get_time(),
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
               timestamp=h_get_time(),
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
               timestamp=h_get_time(),
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
               timestamp=h_get_time(),
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
               timestamp=h_get_time(),
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
               timestamp=h_get_time(),
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
               timestamp=h_get_time(),
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
               timestamp=h_get_time(),
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
               timestamp=h_get_time(),
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
               timestamp=h_get_time(),
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
               timestamp=h_get_time(),
               color=c_get_color("red")
            )
            await ctx.send(embed=embed_error)

    @dev.command()
    async def leave(self, ctx, *, guild: discord.Guild):
        """Leave a guild."""
        try:
            await ctx.guild.leave()
            embed = discord.Embed(
               title=f"Left {guild.name}",
               description=f"""```md
- Owned by {guild.owner} - {guild.owner_id}
```""",
               timestamp=h_get_time(),
               color=c_random_color()
            )
            await ctx.send(embed=embed)

        except Exception as e:
            embed_error = discord.Embed(
               title="Error",
               description=f"""```diff
- {e}
```""",
               timestamp=h_get_time(),
               color=c_get_color("red")
            )
            await ctx.send(embed=embed_error)

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
            timestamp=h_get_time(),
            color=c_random_color()
        )
        await ctx.send(embed=embed)

    @commands.command(
        name="eval",
        aliases=["exec"]
    )
    @commands.is_owner()
    async def _eval(self, ctx, *, code: str):
        """Evaluates code given"""

        if "```py" not in code:
            # Didn"t find a code block
            no_cb = discord.Embed(
                title="Error",
                description="Include a code block dumb fuck",
                timestamp=h_get_time(),
                color=c_random_color()
            )
            return await ctx.send(embed=no_cb)

        env = {
            "bot": self.bot,
            "ctx": ctx
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
                timestamp=h_get_time(),
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
                timestamp=h_get_time(),
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
                        timestamp=h_get_time(),
                        color=c_get_color("green")
                    )
                    return await ctx.send(embed=evaluated)

            else:
                embed_e3 = discord.Embed(
                    title="Error",
                    description=f"""```py
{value}{out}
```""",
                    timestamp=h_get_time(),
                    color=c_get_color("red")
                )
                return await ctx.send(embed=embed_e3)

    @commands.command()
    async def botinfo(self, ctx):
        """Will expand as I go but showing some basic bot info"""
        embed = discord.Embed(
           title=f"Bot Info",
           description=f"""```json
{json.dumps(self.bot.file_len_dict, indent=4)}
```""",
           timestamp=h_get_time(),
           color=c_random_color()
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(DevOnly(bot))