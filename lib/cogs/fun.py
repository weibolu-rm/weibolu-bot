from discord.ext.commands import Cog, command, has_permissions, cooldown, BucketType
from discord.ext.commands import has_permissions
from ..urbandict import urbandict as ud
from discord import Color, Emoji, HTTPException
from weibolu import create_embed
import requests

class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot


    @cooldown(2, 20, BucketType.user)
    @command(name="define", aliases=["ud"])
    async def define(self, ctx, *, expression: str):
        defs = ud.define(expression)
        if defs:
            await ctx.send(f"{defs[0]}")


    @Cog.listener() 
    async def on_raw_reaction_add(self, payload): 
        if int(payload.message_id) == self.bot.reaction_yoink:

            # need permission to manage server
            if not payload.member.guild_permissions.manage_guild:
                return
                
            emoji = payload.emoji
            if emoji in self.bot.guild.emojis:
                print("emoji already exists")
                return
    
            try:
                response = requests.get(emoji.url)
                await self.bot.guild.create_custom_emoji(name=emoji.name, image=response.content)
            except HTTPException:
                self.bot.log_channel.send(f"Problem adding emoji {emoji.name}.")
    
            embed = create_embed(f"Emoji added to {self.bot.guild.name}!", f"{emoji.name}", 
                                    image_url=emoji.url, color=Color.dark_teal())
    
            await self.bot.log_channel.send(embed=embed)

    
    @Cog.listener() 
    async def on_raw_reaction_remove(self, payload): 
        if int(payload.message_id) == self.bot.reaction_yoink:

            member = self.bot.guild.get_member(payload.user_id)
            # need permission to manage server
            if not member.guild_permissions.manage_guild:
                return
                
            emoji = payload.emoji
            # we need to get the actual Emoji object
            for e in self.bot.guild.emojis:
                if emoji == e:
                    embed = create_embed(f"Emoji removed from {self.bot.guild.name}!", f"{emoji.name}", 
                                        image_url=emoji.url, color=Color.dark_magenta())
                    await e.delete()
                    await self.bot.log_channel.send(embed=embed)



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