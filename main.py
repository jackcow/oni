import os
import discord
from discord.ext import commands
from asyncio import sleep
from replit import db
from web_server import online

'''TODO:
custom error messages
image manipulation
social media posts
math engine
execution engine
'''


def get_prefix(client, message):
    try:
        return db[message.guild.id]
    except:
        return '.'


def get_num_members():
    total = 0
    for guild in client.guilds:
        total += len(guild.members)

    return total


intents = discord.Intents.default()
client = commands.AutoShardedBot(command_prefix=get_prefix,
                                 intents=intents,
                                 help_command=None,
                                #  case_insensitive=True,
                      )


# @client.event
# async def on_guild_join(guild):
#     db[guild.id] = '.'


@client.event
async def on_guild_remove(guild):
    del db[guild.id]


@client.command(aliases=['prefix'])
async def changeprefix(ctx, prefix):
    """``prefix [cog name]`` changes server's prefix"""
    if prefix == '.':
        del db[ctx.guild.id]
    else:
        db[ctx.guild.id] = prefix
    await ctx.send(f"> `server prefix was changed to: {prefix} `")


@client.event
async def on_command_error(ctx, error):
    await ctx.send(f"wtf bro?\n {error}")


async def status_task():
    while True:
        await client.change_presence(activity=discord.Activity(
            type=0, name=f"in {len(client.guilds)} Servers"))
        await sleep(30)
        await client.change_presence(activity=discord.Activity(
            type=0, name=f"with {len(set(client.get_all_members()))} Users"))
        await sleep(30)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    client.loop.create_task(status_task())


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

if __name__ == "__main__":
    online()
    client.run(os.getenv('TOKEN'))
