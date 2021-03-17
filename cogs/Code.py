from discord.ext import commands


class Code(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command(aliases=["py", "py3"])
    # @commands.cooldown(1, 10, commands.BucketType.server)
    async def python3(self, ctx, *, content: commands.clean_content):
        """`python3 [code]` executes your python3 code"""
        content = (
            content.replace("```python", "").replace("```py", "").replace("```", "")
        )
        await self.run_code(ctx, "python3", content)

def setup(client):
    client.add_cog(Code(client))
