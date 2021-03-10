from discord.ext import commands
import discord
import pytz
from datetime import datetime
import yfinance as yf


class Stocks(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['ticker'])
    async def stock(self, ctx, *, ticker):
        """return stock info (WIP)"""

        colors = [
            0x008b00,  #green
            0x8b0000
        ]  #red

        for t in ticker.split():

            stock = yf.Ticker(t)
            lastPrice = stock.history().tail(1)['Close'].iloc[0]
            openPrice = stock.info['open']

            color = colors[0] if lastPrice > openPrice else colors[1]

            embed = discord.Embed(
                title=stock.info['shortName'] + " (" + stock.info['symbol'] +
                ")",
                url="https://finance.yahoo.com/quote/" + stock.info['symbol'],
                description="Currency in " + stock.info['currency'],
                color=color)

            embed.add_field(name="Last Price",
                            value='{0:.2f}'.format(lastPrice),
                            inline=True)
            embed.add_field(name="Day High",
                            value='{0:.2f}'.format(stock.info['dayHigh']),
                            inline=True)
            embed.add_field(name="Ask",
                            value='{0:.2f}'.format(stock.info['ask']),
                            inline=True)

            embed.add_field(name="Open",
                            value='{0:.2f}'.format(openPrice),
                            inline=True)
            embed.add_field(name="Day Low",
                            value='{0:.2f}'.format(stock.info['dayLow']),
                            inline=True)
            embed.add_field(name="Bid",
                            value='{0:.2f}'.format(stock.info['bid']),
                            inline=True)

            embed.set_footer(text=str(
                datetime.now(pytz.timezone('America/New_York')).strftime(
                    "%Y-%m-%d %H:%M:%S EST")))
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Stocks(client))
