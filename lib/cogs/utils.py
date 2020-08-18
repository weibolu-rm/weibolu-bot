from discord.ext.commands import Cog, has_permissions
from discord.ext.commands import command, check

# OWNER_ID = 91939126634364928


# def is_me():
#     def predicate(ctx):
#         return ctx.message.author.id == OWNER_ID
#     return check(predicate)

class Utils(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    
    # @is_me()
    @command(name="kill")
    async def kill(self, ctx):
        if(ctx.message.author.id == self.bot.owner_id):
            await ctx.send("Aight, ima head out <:Tuturu:743261358509785099>")
            await self.bot.logout()
        else:
            await ctx.send(f"<@{ctx.message.author.id}>, you do not have permission to do that.")
            #TODO: manage exception instead. 

    @command(name="github", aliases=["git"])
    async def github(self, ctx):
        await ctx.send("Check out weibolu's GitHub! https://github.com/weibolu-rm")
    
    @command(name="clear", aliases=["clr"])
    @has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=5):
        author = ctx.author
        f_msg = f"""```diff
- {author} deleted {amount} messages.
```
"""
        await ctx.channel.purge(limit=amount+1)
        await ctx.send(f_msg)

    @command(name="echo", aliases=["say"])
    async def echo(self, ctx, *, message: str):
        await ctx.channel.purge(limit=1)
        await ctx.send(message)

        

def setup(bot):
    bot.add_cog(Utils(bot))