import discord
from discord.ext import commands
import os

class Dev(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['rld','rl'])
    @commands.is_owner()
    async def reload(self, ctx, extension):
        """`reload <extension>` reloads a loaded extension"""
        try:
            self.client.reload_extension(f"cogs.{extension}")
            await ctx.send(f"> `{extension} was reloaded`")
        except Exception as e:
            await ctx.send(f"> `{extension} cannot be reloaded`")
            raise e

    @commands.command(aliases=['uld','unld','ul'])
    @commands.is_owner()
    async def unload(self, ctx, extension):
        """`unload <extension>` unloads named extension"""
        try:
            self.client.unload_extension(f"cogs.{extension}")
            await ctx.send(f"> `{extension} was unloaded`")
        except Exception as e:
            await ctx.send(f"> `{extension} cannot be unloaded`")
            raise e

    @commands.command(aliases=['ld'])
    @commands.is_owner()
    async def load(self, ctx, extension):
        """`load <extension>` loads named extension"""
        try:
            self.client.load_extension(f"cogs.{extension}")
            await ctx.send(f"> `{extension} was loaded`")
        except Exception as e:
            await ctx.send(f"> `{extension} cannot be loaded`")
            raise e

    @commands.command(aliases=['rlall','rldall'])
    @commands.is_owner()
    async def reloadall(self, ctx):
        """`reloadall` reloads all loaded extensions"""
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                extension = filename[:-3]
                try:
                    self.client.reload_extension(f'cogs.{extension}')
                    await ctx.send(f"> `{extension} was reloaded`")
                except Exception as e:
                    await ctx.send(f"> `{extension} cannot be reloaded`")
                    raise e


def setup(client):
    client.add_cog(Dev(client))
