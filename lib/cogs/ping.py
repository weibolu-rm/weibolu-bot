from discord.ext.commands import Cog
from discord.ext.commands import command

class Ping(Cog):
    def __init__(self, bot):
        self.bot = bot
        
    # ctx is a context ctx.send == ctx.channel.send
    @command(name="ping")
    async def ping(self, ctx):
        await ctx.send("pong! {0:.2f}ms".format(self.bot.latency * 1000))
    
def setup(bot):
    bot.add_cog(Ping(bot))