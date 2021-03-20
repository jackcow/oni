import discord
from discord.ext import commands


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

    @commands.command()
    async def ping(self, ctx):
        """`ping` checks Oni ping"""
        await ctx.send(f"> Oni Ping: `{round(self.client.latency * 1000)}ms`")


def setup(client):
    client.add_cog(Management(client))
