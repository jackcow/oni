import discord
from discord.ext import commands
from discord import File


import io
import requests
from PIL import Image, ImageEnhance

chars = "@#$%X*+;,. "

def resize_image(image, new_width=100):
    width, height = image.size
    ratio = height / width
    # its very tall so I cut it in half and a little bit
    new_height = int((new_width * ratio)//2.3)
    resized_image = image.resize((new_width, new_height))
    return resized_image

def grayscale(image):
    # luminance mode
    return image.convert("L")

def pixel_ascii(image):
    return "".join([chars[pixel//25] for pixel in image.getdata()])


class Images(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["asc"])
    async def ascii(self, ctx, new_width=100):
        """`ascii <width>` converts image attachment to ASCII, optional width"""
        url = ctx.message.attachments[0].url
        img = Image.open(requests.get(url, stream=True).raw)

        data = pixel_ascii(grayscale(resize_image(img, new_width)))

        img = "\n".join(data[i:(i+new_width)] for i in range(0, len(data), new_width))

        try:
            await ctx.send(f"```{img}```")
        except:
            buf = io.BytesIO(img.encode('utf-8'))
            await ctx.send(file=File(buf, filename=f"{ctx.author}_ascii.txt"))

    @commands.command(aliases=["gsc", "gscale"])
    async def grayscale(self, ctx):
        """`grayscale` converts image attachment to grayscale"""
        url = ctx.message.attachments[0].url
        img = Image.open(requests.get(url, stream=True).raw)
        img = grayscale(img)
        with io.BytesIO() as image_binary:
            img.save(image_binary, 'PNG')
            image_binary.seek(0)
            await ctx.send(file=discord.File(image_binary, filename='grayscale.png'))

    @commands.command(aliases=["destroy","df"])
    async def deepfry(self, ctx):
        """`df` deepfry image attachment, values wip`"""
        url = ctx.message.attachments[0].url
        img = Image.open(requests.get(url, stream=True).raw)

        sharpness = ImageEnhance.Sharpness(img)
        img = sharpness.enhance(100)

        contrast = ImageEnhance.Contrast(img)
        img = contrast.enhance(10)

        saturation = ImageEnhance.Color(img)
        img = saturation.enhance(5)

        with io.BytesIO() as image_binary:
            img.save(image_binary, 'PNG')
            image_binary.seek(0)
            await ctx.send(file=discord.File(image_binary, filename='grayscale.png'))

    

def setup(client):
    client.add_cog(Images(client))
