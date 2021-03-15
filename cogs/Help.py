from discord.ext import commands
import discord

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.listCogs = ['Audio', #'Code',
                         'Developer Tools', 'Fun',
                         #'Help', #'Images',
                         'Management', 'Message',
                         'Stock',
                         ]

    @commands.command(hidden=True)
    async def help(self, ctx):
        embed = discord.Embed(
                title="Extensions")
        for cogName in self.listCogs:
            cog = self.client.get_cog(cogName)
            commands = cog.get_commands()
            for c in commands:
                embed.add_field(name=c.name,
                                value=c.short_doc)
        await ctx.send(embed=embed)

        
def setup(client):
    client.add_cog(Help(client))
