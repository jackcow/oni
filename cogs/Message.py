from discord.ext import commands
from replit import db


class Message(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.content.startswith('oni.prefix'):
            try:
                await message.channel.send(f"> The prefix for this server is `\'{db[message.guild.id]}\'`")
            except:
                await message.channel.send("> The prefix for this server is `\'.\'`")



def setup(client):
    client.add_cog(Message(client))
