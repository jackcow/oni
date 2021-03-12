from discord.ext import commands
import discord
# from deeppyer import deepfry as df
# import requests
from io import BytesIO
from PIL import Image

class Images(commands.Cog):
    def __init__(self, client):
        self.client = client


    # @commands.command(aliases=['df'])
    # async def deepfry(self, ctx):
    #     """not added"""
    #     url = ctx.message.attachments[0].url
    #     img = BytesIO(requests.get(url).content)
    #     img = await df(img)
    #     await ctx.send(file=discord.File(fp=img, filename='image.png'))
        
    

def setup(client):
    client.add_cog(Images(client))
