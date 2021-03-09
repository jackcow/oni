from discord.ext import commands

class Code(commands.Cog):

  def __init__(self, client):
    self.client = client

#WIP
#integrate aiohttp
#use piston api



def setup(client):
    client.add_cog(Code(client))
  