from discord.ext.commands import Cog, has_permissions
from discord.ext.commands import command, check

OWNER_ID = 562175478824304661


def is_me():
    def predicate(ctx):
        return ctx.message.author.id == OWNER_ID
    return check(predicate)

class Utils(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    
    @command(name="kill")
    @is_me()
    async def kill(self, ctx):
        await ctx.send("Aight, ima head out <:Tuturu:743261358509785099>")
        await self.bot.logout()
    
    @command(name="github", aliases=["git"])
    async def github(self, ctx):
        await ctx.send("Check out weibolu's GitHub! https://github.com/weibolu-rm")
    
    @command(name="clear", aliases=["clr"])
    @has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=5):
        author = ctx.author
        await ctx.channel.purge(limit=amount)
        await ctx.send(f"{author} deleted {amount} messages." )

    @command(name="echo", aliases=["say"])
    async def echo(self, ctx, *, message: str):
        await ctx.channel.purge(limit=1)
        await ctx.send(message)

        

def setup(bot):
    bot.add_cog(Utils(bot))