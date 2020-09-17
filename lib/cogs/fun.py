from discord.ext.commands import Cog, command, has_permissions, cooldown, BucketType
from ..urbandict import urbandict as ud

class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @cooldown(2, 20, BucketType.user)
    @command(name="define", aliases=["ud"])
    async def define(self, ctx, *, expression: str):
        defs = ud.define(expression)
        if defs:
            await ctx.send(f"{defs[0]}")

    # TODO: make a seperate reaction Cog
    @Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if "???" in message.content:
            await message.channel.send("<:KannaWhat:743663211584159835>")

        if message.content.lower().startswith("hey kids"):
            await message.channel.send("<:KannaPolice:743272223414026332>")   

            
def setup(bot):
    bot.add_cog(Fun(bot))