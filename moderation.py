"""
Tenshi Discord Bot
Copyright (C) 2021 Ben Z.
This software is licensed under Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)
"""

import discord
from discord.ext import commands
from colors import *
import asyncio


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        help="Purge messages from the channel that you used this command in.",
        brief="Purge", 
        usage="<Message Amount>",
        description="This command requires the `manage_messages` permission to run."
    )
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(3.0, 10.0, commands.BucketType.user)
    async def purge(self, ctx, amount: int):
        """Purge messages from a channel"""
        channel = ctx.message.channel
        messages = []
        if amount > 99:
            amount = 99
        async for message in channel.history(limit=amount + 1):
            messages.append(message)
        
        try:
            await channel.delete_messages(messages)

            if amount == 1:
                word_thing = "has"
            else:
                word_thing = "have"

            embed = discord.Embed(
            title="Message Purge", 
            description=f'{amount} messages {word_thing} been purged by {ctx.message.author.mention}', 
            timestamp=datetime.datetime.utcnow(), 
            color=c_random_color()
            )
            return await ctx.send(embed=embed, delete_after=5)

        except Exception as e:
            # Something failed returning
            error = discord.Embed(
                title="Error",
                description=f"""Something went wrong with this command...
                Make sure the messages you are purging aren't over 14 days old, make sure you're also actually purging messsages...""",
                timestamp=datetime.datetime.utcnow(),
                color=c_random_color()
            )
            return await ctx.send(embed=error)
        
    @purge.error
    async def purge_error(self, ctx, error):
        """Errors that may arise"""
        if isinstance(error, commands.CheckFailure):
            embed = discord.Embed(
                title='Purge Error', 
                description='Insufficient Permissions, you need the `manage_messages` permission to use purge', 
                timestamp=datetime.datetime.utcnow(), 
                color=c_get_color("red")
            )
            return await ctx.send(embed=embed, delete_after=5)

        elif isinstance(error, commands.CommandOnCooldown):
            cooldown_embed = discord.Embed(
                title=f"AMS is on Cooldown",
                description=f"Try again in {error.retry_after:.2f} seconds.", 
                timestamp = datetime.datetime.utcnow(),
                color=c_get_color("red")
            )
            return await ctx.send(embed=cooldown_embed, delete_after=5)
    
    @commands.command(
        help="Kicks a member from the server",
        brief="Kick", 
        usage="<User>",
        description="This command requires the `kick_members` permission to run."
    )
    @commands.has_permissions(kick_members=True)
    @commands.cooldown(1.0, 1.0, commands.BucketType.user)
    async def kick(self, ctx, member: discord.Member=None):
        """Kick a member from the guild"""
        if not member or member == ctx.author:
            member = ctx.author
            embed = discord.Embed(
                title='Kick Error', 
                description="You cannot kick yourself!", 
                timestamp=datetime.datetime.utcnow(), 
                color=c_get_color("red")
                )
            return await ctx.send(embed=embed, delete_after=5)
        else: 
            await member.kick()
            embed = discord.Embed(
                title='Member Kicked', 
                description=f'Member `{member.display_name}{member.discriminator}` ID: `{member.id}` was kicked.', 
                timestamp=datetime.datetime.utcnow(), 
                color=c_get_color("green")
                )
            return await ctx.send(embed=embed)

    @kick.error
    async def kick_error(self, ctx, error):
        """Kicking errors that we may recieve"""
        if isinstance(error, commands.CheckFailure):
            embed = discord.Embed(
                title='Kick Error', 
                description='Insufficient Permissions, you need the `kick_members` permission to run this command.', 
                timestamp=datetime.datetime.utcnow(), 
                color=c_get_color("red")
                )
            return await ctx.send(embed=embed, delete_after=5)
        elif isinstance(error, commands.CommandOnCooldown):
            cooldown_embed = discord.Embed(
                title=f"AMS is on Cooldown",
                description=f"Try again in {error.retry_after:.2f} seconds.", 
                timestamp = datetime.datetime.utcnow(),
                color=c_get_color("red")
            )
            return await ctx.send(embed=cooldown_embed, delete_after=5)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1.0, 1.0, commands.BucketType.user)
    async def ban(self, ctx, member : discord.Member, *, reason = "None"):
        try:
            await member.ban(reason=reason)
            embed = discord.Embed(
                title=f"{member} Banned",
                description=f"""Responsible Moderator: {ctx.author.mention}
                Reason:
```diff
- {reason}
```""",
                timestamp=datetime.datetime.utcnow(),
                color=c_random_color()
            )
            return await ctx.send(embed=embed)
        except discord.NotFound:
            embed_fail = discord.Embed(
                title=f"{member} Not Found",
                timestamp=datetime.datetime.utcnow(),
                color=c_random_color()
            )
            return await ctx.send(embed=embed_fail)

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            embed = discord.Embed(
                title='Ban Error', 
                description='Insufficient Permissions', 
                timestamp=datetime.datetime.utcnow(), 
                color=c_random_color()
                )
            return await ctx.send(embed=embed, delete_after=5)
        elif isinstance(error, commands.CommandOnCooldown):
            cooldown_embed = discord.Embed(
                title=f"AMS is on Cooldown",
                description=f"Try again in {error.retry_after:.2f} seconds.", 
                timestamp = datetime.datetime.utcnow(),
                color=c_get_color("red")
            )
            return await ctx.send(embed=cooldown_embed, delete_after=5)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        member = discord.Object(id=int(member))
        try:
            await ctx.guild.unban(member)
            embed = discord.Embed(
                title=f"{member} Unbanned",
                description=f"Responsible Moderator: {ctx.author.mention}",
                timestamp=datetime.datetime.utcnow(),
                color=c_random_color()
            )
            await ctx.send(embed=embed)
            return
        except discord.NotFound:
            embed_fail = discord.Embed(
                title=f"{member} Not Found",
                timestamp=datetime.datetime.utcnow(),
                color=c_random_color()
            )
            await ctx.send(embed=embed_fail)
            return
    
    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            embed = discord.Embed(
                title='Unban Error', 
                description='Insufficient Permissions', 
                timestamp=datetime.datetime.utcnow(), 
                color=c_random_color()
                )
            msg = await ctx.send(embed=embed)
            await asyncio.sleep(5)
            await msg.delete()
            return


def setup(bot):
    bot.add_cog(Moderation(bot))