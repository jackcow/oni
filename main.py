import os
from discord.ext import commands
from replit import db
from web_server import online


def get_prefix(client, message):
  try: 
    db[message.guild.id]
  except:
    db[message.guild.id] = '.'

  return db[message.guild.id]


client = commands.Bot(command_prefix=get_prefix)


@client.event
async def on_guild_join(guild):
  db[guild.id] = '.'


@client.event
async def on_guild_remove(guild):
  del db[guild.id]


@client.command()
async def changeprefix(ctx, prefix):
  """Changes Oni's prefix for this server"""
  db[ctx.guild.id] = prefix


@client.event
async def on_command_error(ctx, error):
  await ctx.send(f"wtf bro?\n {error}")


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))



for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

online()
client.run(os.getenv('TOKEN'))