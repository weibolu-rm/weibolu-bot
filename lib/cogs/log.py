from weibolu import create_embed
from discord.ext.commands import Cog, command  
from discord import Color


class Log(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @Cog.listener()
    async def on_ready(self):
        self.log_channel = self.bot.get_channel(757112954599768064)

    @Cog.listener()
    async def on_message_edit(self, original, message):
        if message.author.bot:
            return
        
        if original.content != message.content:

            fields = [("**Original:**", original.content, False), ("**Message:**", message.content, False)]

            embed = create_embed("Message edited", f"Edited by {message.author}.",
            color=Color.gold(), thumbnail_url=message.author.avatar_url, fields=fields)

            await self.log_channel.send(embed=embed)


    @Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return

        fields = [("**Message:**", message.content, False)]

        embed = create_embed("Message deleted", f"Original message by {message.author}.",
        color=Color.gold(), thumbnail_url=message.author.avatar_url, fields=fields)

        await self.log_channel.send(embed=embed)



def setup(bot):
    bot.add_cog(Log(bot))
