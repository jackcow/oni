import discord
from discord.ext import commands
from discord import File

import io
import requests
from PIL import Image, ImageEnhance, ImageOps
from typing import Tuple

Colour = Tuple[int, int, int]
ColourTuple = Tuple[Colour, Colour]


class DefaultColours:
    """Default colours provided for deepfrying"""
    red = ((254, 0, 2), (255, 255, 15))
    blue = ((36, 113, 229), (255,) * 3)

def resize_image(image, new_width=100):
    width, height = image.size
    ratio = height / width
    # its very tall so I cut it in half and a little bit
    new_height = int((new_width * ratio)//2.1)
    resized_image = image.resize((new_width, new_height))
    return resized_image

def grayscale(image):
    # luminance mode
    return image.convert("L")

chars = ["███▓▓▒▒░░ ","@$%X*+;,. ","█▓▒░ ","$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft|()1{}[]?-_+~<>i!lI;:,^`. "]

def pixel_ascii(image,version):
    charset = chars[version]
    return "".join([charset[int(pixel//((256)/len(charset)))] for pixel in image.getdata()])


class Images(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["asc","utf","unic","unc"])
    async def ascii(self, ctx, new_width=100, version=0):
        """`ascii <width=100>` converts image attachment to ASCII, max:1000"""
        if new_width > 1000:
            return await ctx.send(f"> {new_width}? I don't think so")
        if version > 3:
            version = 0

        url = ctx.message.attachments[0].url
        img = Image.open(requests.get(url, stream=True).raw)

        data = pixel_ascii(grayscale(resize_image(img, new_width)), version)

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
    async def deepfry(self, ctx, colours: ColourTuple = DefaultColours.red):
        """`deepfry` deepfry image attachment, todo: add flares, position with opencv"""
        url = ctx.message.attachments[0].url
        img = Image.open(requests.get(url, stream=True).raw)
        
        # trip to hell and back
        img = img.convert('RGB')
        width, height = img.width, img.height
        img = img.resize((int(width ** .9), int(height ** .9)), resample=Image.BICUBIC)
        img = img.resize((int(width ** .88), int(height ** .88)), resample=Image.BILINEAR)
        img = img.resize((int(width ** .75), int(height ** .75)), resample=Image.LANCZOS)
        img = img.resize((width, height), resample=Image.BICUBIC)
        img = ImageOps.posterize(img, 4)

        # make color to blend
        r = img.split()[0]
        r = ImageEnhance.Contrast(r).enhance(2.0)
        r = ImageEnhance.Brightness(r).enhance(1.5)

        r = ImageOps.colorize(r, colours[0], colours[1])

        # Overlay red and yellow onto main image and sharpen the hell out of it
        img = Image.blend(img, r, 0.75)
        img = ImageEnhance.Sharpness(img).enhance(100.0)

        with io.BytesIO() as image_binary:
            img.save(image_binary, 'JPEG', quality=-10)
            image_binary.seek(0)
            await ctx.send(file=discord.File(image_binary, filename='deepfried.jpeg'))
 

def setup(client):
    client.add_cog(Images(client))
