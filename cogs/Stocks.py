import discord
from discord.ext import commands

import time
import yfinance as yf


def inInfo(item,info,alt='None'):
    """
        Checks if item is in given list.
        return item if true, else return alt
        Args:
            item: the item to be compared
            info: the list to be checked
            alt: alternative output
    """
    if item in info:
        return info[item]
    return alt if alt=='None' else info[alt]

class Stocks(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['ticker', 'st', 'stocks', 'stonk', 'stonks'])
    async def stock(self, ctx, *, ticker):
        """`stock [tickers]` lists stock tickers seperated by spaces"""

        colors = [
            0x00873c,  #green
            0xeb0f29,  #red
        ]  

        for t in ticker.split():

            stock = yf.Ticker(t)
            name = inInfo('longName', stock.info, 'shortName')
            sector = stock.info['sector']
            industry = stock.info['industry']
            lastPrice = stock.info['currentPrice']
            openPrice = stock.info['open']

            form = '{0:.2f}' if lastPrice > 5 else '{0:.4f}'
            color = colors[0] if lastPrice > openPrice else colors[1]

            embed = discord.Embed(
                title=f"{name} ({stock.info['symbol']})" ,
                url=f"https://finance.yahoo.com/quote/{stock.info['symbol']}",
                description=f"Sector: {sector}\nIndustry: {industry}\n<t:{int(time.time())}:f>",
                color=color)

            embed.add_field(name="Last Price",
                            value=form.format(lastPrice),
                            inline=True)
            embed.add_field(name="Day High",
                            value=form.format(stock.info['dayHigh']),
                            inline=True)
            embed.add_field(name="52w High",
                            value=form.format(stock.info['fiftyTwoWeekHigh']),
                            inline=True)

            embed.add_field(name="Open",
                            value=form.format(openPrice),
                            inline=True)
            embed.add_field(name="Day Low",
                            value=form.format(stock.info['dayLow']),
                            inline=True)
            embed.add_field(name="52w Low",
                            value=form.format(stock.info['fiftyTwoWeekLow']),
                            inline=True)

            embed.set_footer(text=f"Currency in {stock.info['currency']}")
            await ctx.send(embed=embed)

    @stock.error
    async def stock_error(self, ctx, error):
        await ctx.send("> wtf bro? `Ticker Not Found`")
        print(error)


def setup(client):
    client.add_cog(Stocks(client))
