from discord.ext import commands
import discord

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.listCogs = ['Audio', #'Code',
                         'Developer Tools', 'Fun',
                         #'Help', #'Images',
                         'Management', 'Message',
                         'Stock', 'Code',
                         ]

    @commands.command(hidden=True)
    async def help(self, ctx, extension=""):
        if not extension:
            embed = discord.Embed(title="Extensions")
            for name in self.listCogs:
                embed.add_field(name=name,
                                value='\u200b',
                                inline=False)

        else:
            embed = discord.Embed(title=extension)
            cog = self.client.get_cog(extension)

            commands = cog.get_commands()
            for c in commands:
                embed.add_field(name=c.name,
                                value=c.short_doc,
                                inline=False)

        await ctx.send(embed=embed)

        
def setup(client):
    client.add_cog(Help(client))
