import os
from discord.ext import commands
from replit import db


def get_prefix(client, message):
  try: 
    return db[str(message.guild.id)]
  except:
    db[str(message.guild.id)] = '.'

  return db[str(message.guild.id)]

client = commands.Bot(command_prefix=get_prefix)


@client.event
async def on_guild_join(guild):
  db[str(guild.id)] = '.'


@client.event
async def on_guild_remove(guild):
  del db[str(guild.id)]


@client.command()
async def changeprefix(ctx, prefix):
  db[str(ctx.guild.id)] = prefix


@client.event
async def on_message(message):
  if message.author == client.user:
    return
  if message.content.startswith('oni.prefix'):
    await message.





@client.event
async def on_command_error(ctx, error):
  await ctx.send(f"wtf bro: {error}")


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


client.run(os.getenv('TOKEN'))