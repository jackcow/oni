from discord.ext import client
from PIL import Image
import cv2

class Images(client.Cog):
    def __init__(self, client):
        self.client = client


    @client.command()
    async def deepfry(self, ctx):
        """not added"""
        pass


def setup(client):
    client.add_cog(Images(client))
