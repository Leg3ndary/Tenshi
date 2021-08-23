"""
Tenshi Discord Bot
Copyright (C) 2021 Ben Z.
This software is licensed under Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)
"""

import discord
import traceback
import sys
from discord.ext import commands
from gears.hbot import h_get_time
from gears.cosmetics import *


def gen_error_embed(error_text):
    """Quickly generate an error embed"""
    embed = discord.Embed(
        title="Error",
        description=f"""```diff
- {error_text}
```""",
        timestamp=h_get_time(),
        color=c_get_color("red")
    )
    return embed


class ErrorHandler(commands.Cog):
    """Our Error Handler"""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """When we recieve an error"""

        # Prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, "on_error"):
            return

        # This prevents any cogs with an overwritten cog_command_error being handled here.
        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, "original", error)

        # Disabled command
        if isinstance(error, commands.DisabledCommand):
            return await ctx.send(embed=gen_error_embed(f"{ctx.command} has been disabled."))

        # Only allowed in direct messages
        elif isinstance(error, commands.NoPrivateMessage):
            return await ctx.send(embed=gen_error_embed(f"{ctx.command} can not be used in direct messages."))

        # Only allowed in direct messages
        elif isinstance(error, commands.PrivateMessageOnly):
            return await ctx.send(embed=gen_error_embed(f"{ctx.command} can only be used in direct messages."))

        # Cooldowns
        elif isinstance(error, commands.CommandOnCooldown):
            cooldown_embed = discord.Embed(
                title=f"{ctx.command} is on Cooldown",
                description=f"""Try again in {error.retry_after:.2f} seconds.""", 
                timestamp = h_get_time(),
                color=c_get_color("red")
            )
            return await ctx.send(embed=cooldown_embed)

        # NSFW
        elif isinstance(error, commands.NSFWChannelRequired):
            return await ctx.send(embed=gen_error_embed(f"{ctx.command} has been marked NSFW channels only."))

        # Check fail
        elif isinstance(error, commands.CheckFailure):
            return await ctx.send(embed=gen_error_embed(f"{ctx.command} has failed because you don't have sufficient permissions"))

        else:
            # All other Errors not returned come here. And we can just print the default TraceBack.
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


def setup(bot):
    bot.add_cog(ErrorHandler(bot))