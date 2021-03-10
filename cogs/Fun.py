import random
import discord
from discord.ext import commands


class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['dice'])
    async def roll(self, ctx, *, integer=6):
        """roll the dice, default=6"""
        try:
            await ctx.send(
                f"{ctx.message.author.mention} rolled a {random.randrange(int(integer))+1}."
            )
        except:
            await ctx.send("Please enter an integer")

    @commands.command(aliases=['yn', 'yesno'])
    async def yesorno(self, ctx, *, question):
        """yes or no"""
        responses = ['yes', 'no']
        await ctx.send(
            f"Question: {question}\nAnswer: {random.choice(responses)}")

    @commands.command(aliases=['pfp'])
    async def profilepicture(self, ctx):
        """sends mentioned profile file picture"""
        for member in ctx.message.mentions:
            await ctx.send(embed=discord.Embed().set_image(
                url=member.avatar_url))


def setup(client):
    client.add_cog(Fun(client))
