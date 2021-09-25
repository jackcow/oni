import discord
from discord.ext import commands

import time


class Management(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['clr', 'cl'])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=5):
        """`clear <int>` clears [int] messages"""
        try:
            await ctx.channel.purge(limit=amount+1)
        # print(f"cleared {amount} messages")
        except:
            await ctx.send("> Please enter an integer")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """`kick <member> [reason]` kicks mentioned member"""
        await member.kick(reason=reason)
        await ctx.send(f"> {member.mention} was kicked for `{reason}`.")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """`ban <member> [reason]` kicks mentioned member"""
        await member.ban(reason=reason)
        await ctx.send(f"> {member.mention} was banned for `{reason}`.")

    @commands.command(aliases=["pardon"])
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        """`unban <user#tag>` unbans usertag member"""
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name,
                                                   member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"> unbanned {user.mention}")
                return

    @commands.command(aliases=['t'])
    async def time(self, ctx, modifier="F", unix='None'):
        """`time [mod] [unix]` display the time depending on viewer's timezone"""
        if unix.isnumeric():
            unix = int(unix)
            if (-8640000000000 <= unix <= 8640000000000): timestamp = unix
        else: 
            timestamp = int(time.time())
        if modifier in "dDtTfFR":
            await ctx.send(f"> <t:{timestamp}:{modifier}>")
        elif modifier in "aA":
            for chr in "dDtTfFR":
                await ctx.send(f"> <t:{timestamp}:{chr}>")
        else: await ctx.send(f"> modcheck?")

    @commands.command(aliases=['tmstmp'])
    async def timestamp(self, ctx, sec=0, min=0, hr=0, d=0, yr=0):
        """`timestamp [sec] [min] [hr] [d] [yr]` set"""

        timestamp = int(time.time()) + sec + min*60 + hr*3600 + d*86400 + yr*31536000
        await ctx.send(f"> {timestamp}\n <t:{timestamp}:R>")
        

    @commands.command()
    async def ping(self, ctx):
        """`ping` checks Oni ping"""
        await ctx.send(f"> Oni Ping: `{round(self.client.latency * 1000)}ms`")


def setup(client):
    client.add_cog(Management(client))
