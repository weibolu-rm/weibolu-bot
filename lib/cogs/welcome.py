from discord.ext.commands import Cog, command

class Welcome(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_member_join(self, member):
        pass

    @Cog.listener()
    async def on_member_remove(self, member):
        pass   

def setup(bot):
    bot.add_cog(Welcome(bot))