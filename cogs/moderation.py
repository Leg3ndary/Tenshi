"""
Tenshi Discord Bot
Copyright (C) 2021 Ben Z.
This software is licensed under Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)
"""

import discord
from discord.ext import commands
from gears.cosmetics import *
import datetime


class Moderation(commands.Cog):
    """Moderation related commands"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        help="Purge messages from the channel that you used this command in.",
        brief="Purge", 
        usage="<Message Amount>",
        description="This command requires the `manage_messages` permission to run."
    )
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(3.0, 15.0, commands.BucketType.user)
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
                color=c_get_color("green")
            )
            await ctx.send(embed=embed, delete_after=5)

        except Exception:
            # Something failed returning
            error = discord.Embed(
                title="Error",
                description=f"""Something went wrong with this command...
                Make sure the messages you are purging aren't over 14 days old, make sure you're also actually purging messsages...""",
                timestamp=datetime.datetime.utcnow(),
                color=c_get_color("red")
            )
            await ctx.send(embed=error)

    @commands.command(
        help="Kicks a member from the server",
        brief="Kick", 
        usage="<User>",
        description="This command requires the `kick_members` permission to run."
    )
    @commands.has_permissions(kick_members=True)
    @commands.cooldown(2.0, 6.0, commands.BucketType.user)
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

    @commands.command(
        help="Bans a member from the server",
        brief="Ban", 
        usage="<User>",
        description="This command requires the `ban_members` permission to run."
    )
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(2.0, 6.0, commands.BucketType.user)
    async def ban(self, ctx, member: discord.Member, *, reason = "None"):
        """Bans a member from the guild"""
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
                color=c_get_color("green")
            )
            return await ctx.send(embed=embed)
        except discord.NotFound:
            embed_fail = discord.Embed(
                title=f"{member} Not Found",
                timestamp=datetime.datetime.utcnow(),
                color=c_get_color("red")
            )
            return await ctx.send(embed=embed_fail)

    @commands.command(
        help="Unbans a member from the server",
        brief="Unban", 
        usage="<User>",
        description="This command requires the `ban_members` permission to run."
    )
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(2.0, 6.0, commands.BucketType.user)
    async def unban(self, ctx, *, member: discord.Member):
        """Unbans an member"""
        try:
            await ctx.guild.unban(member)
            embed = discord.Embed(
                title=f"{member} Unbanned",
                description=f"Responsible Moderator: {ctx.author.mention}",
                timestamp=datetime.datetime.utcnow(),
                color=c_get_color("green")
            )
            await ctx.send(embed=embed)
        except discord.NotFound:
            embed_fail = discord.Embed(
                title=f"{member} not found.",
                timestamp=datetime.datetime.utcnow(),
                color=c_get_color("red")
            )
            await ctx.send(embed=embed_fail)


def setup(bot):
    bot.add_cog(Moderation(bot))