import random
import discord
from discord.ext import commands


class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['dice'])
    async def roll(self, ctx, *, integer=6):
        """``roll [int]`` rolls random value starting from 1 to [int]"""
        try:
            await ctx.send(
                f"> {ctx.message.author.mention} rolled a {random.randrange(int(integer))+1}."
            )
        except:
            await ctx.send("Please enter an integer")

    @commands.command(aliases=['yn', 'yesno'])
    async def yesorno(self, ctx, *, question):
        """``yn [question]`` gives yes or no answer to question"""
        responses = ['Yes', 'No']
        await ctx.send(
            f"```Question: {question}\nAnswer: {random.choice(responses)}```")

    @commands.command(aliases=['pfp'])
    async def profilepicture(self, ctx):
        """``pfp [mentions]`` sends mentioned profile picture"""
        for member in ctx.message.mentions:
            await ctx.send(embed=discord.Embed().set_image(
                url=member.avatar_url))


def setup(client):
    client.add_cog(Fun(client))
