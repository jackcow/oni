import aiohttp
import discord
from discord.ext import commands
import os
import json


class Code(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def run(self, ctx, language, content):

        async with self.client.aioSession.post(
            "https://emkc.org/api/v1/piston/execute", 
            data={"language": language,
                  "source": content}
        ) as response:
            r = await response.json()

        output = "Ok And? (No Output)" if not r["output"] else r["output"]
        await ctx.send(f"```{output}```")

    @commands.command(aliases=["py", "py3"])
    # @commands.cooldown(1, 10, commands.BucketType.server)
    async def python3(self, ctx, *, content: commands.clean_content):
        """`python3 [code]` run python3 code"""
        content = content.replace("```", "")
        await self.run(ctx, "python3", content)

    @commands.command(aliases=["j"])
    # @commands.cooldown(1, 10, commands.BucketType.server)
    async def java(self, ctx, *, content: commands.clean_content):
        """`java [code]` run java code"""
        content = content.replace("```", "")
        await self.run(ctx, "java", content)

    @commands.command()
    # @commands.cooldown(1, 10, commands.BucketType.server)
    async def c(self, ctx, *, content: commands.clean_content):
        """`c [code]` run c code"""
        content = content.replace("```", "")
        await self.run(ctx, "c", content)

    @commands.command(aliases=["c++"])
    # @commands.cooldown(1, 10, commands.BucketType.server)
    async def cpp(self, ctx, *, content: commands.clean_content):
        """`cpp [code]` run cpp code"""
        content = content.replace("```", "")
        await self.run(ctx, "cpp", content)

def setup(client):
    client.add_cog(Code(client))
