from discord.ext.commands import Cog, command, has_permissions, cooldown, BucketType
from discord.ext.commands import has_permissions
from ..urbandict import urbandict as ud
from discord import Color, Emoji
from weibolu import create_embed
import requests

class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        self.log_channel = self.bot.get_channel(757112954599768064)

    @cooldown(2, 20, BucketType.user)
    @command(name="define", aliases=["ud"])
    async def define(self, ctx, *, expression: str):
        defs = ud.define(expression)
        if defs:
            await ctx.send(f"{defs[0]}")


    @Cog.listener()
    async def on_raw_reaction_add(self, payload):
        emoji = payload.emoji
        response = requests.get(emoji.url)

        if str(payload.message_id) == "759625578847666206":
            await self.bot.guild.create_custom_emoji(name=emoji.name, image=response.content)
        embed = create_embed(f"Emoji added to {self.bot.guild.name}!", f"{emoji.name}", 
                                image_url=emoji.url, color=Color.dark_magenta())
        await self.log_channel.send(embed=embed)

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