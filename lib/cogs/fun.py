from discord.ext.commands import Cog, command, has_permissions
from ..urbandict import urbandict as ud

class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # @command(name="hack")
    # @has_permissions(administrator=True)
    # async def hack(self, ctx, *, message: str):
    #     await ctx.channel.purge(limit=1)
    #     await ctx.send(message, tts=True)

    @command(name="define", aliases=["ud"])
    async def define(self, ctx, *, expression: str):
        defs = ud.define(expression)
        if defs:
            await ctx.send(f"{defs[0]}")


    async def on_message(self, ctx, message: str):
        if ctx.message.author.bot:
            return

            
def setup(bot):
    bot.add_cog(Fun(bot))