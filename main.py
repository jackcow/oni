import os
import json
from discord.ext import commands


def get_prefix(client, message):
    with open('prefixes.json', 'r') as file:
        prefixes = json.load(file)

    return prefixes[str(message.guild.id)]


client = commands.Bot(command_prefix=get_prefix)


@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as file:
        prefixes = json.load(file)

    prefixes[str(guild.id)] = '.'

    with open('prefixes.json', 'w') as file:
        json.dump(prefixes, file, indent=4)


@client.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as file:
        prefixes = json.load(file)

    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as file:
        json.dump(prefixes, file, indent=4)


@client.command()
async def changeprefix(ctx, prefix):
    """change the prefix"""
    with open('prefixes.json', 'r') as file:
        prefixes = json.load(file)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as file:
        json.dump(prefixes, file, indent=4)








@client.event
async def on_command_error(ctx, error):
  await ctx.send(f"wtf bro: {error}")


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


client.run(os.getenv('TOKEN'))