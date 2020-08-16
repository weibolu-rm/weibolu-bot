from discord.ext.commands import Cog
from discord.ext.commands import command

class Utils(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="kill")
    async def kill(self, ctx):
        await ctx.send("Aight, ima head out <:Tuturu:743261358509785099>")
        await self.bot.logout()
    
    @command(name="github", aliases=["git"])
    async def github(self, ctx):
        await ctx.send("Check out weibolu's GitHub! https://github.com/weibolu-rm")


def setup(bot):
    bot.add_cog(Utils(bot))