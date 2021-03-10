import discord
from discord.ext import commands


class Management(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=5):
        """clears messages, default=5"""
        await ctx.channel.purge(limit=amount)
        # print(f"cleared {amount} messages")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """kick command"""
        await member.kick(reason=reason)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """ban command"""
        await member.ban(reason=reason)
        await ctx.send(f"{member.mention} has been banned.")

    @commands.command(aliases=["pardon"])
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        """unban command"""
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name,
                                                   member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"unbanned {user.mention}")
                return

    @commands.command()
    async def ping(self, ctx):
        """ping check command"""
        await ctx.send(f"Oni Ping: {round(self.client.latency * 1000)}ms")


def setup(client):
    client.add_cog(Management(client))
