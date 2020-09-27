from discord.ext.commands import Cog, command, has_permissions
from ..db import db 
from discord import Color
from weibolu import create_embed
import re

class Meta(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="prefix")
    @has_permissions(manage_guild=True)
    async def change_prefix(self, ctx, new: str):
        if len(new) > 5:
            await ctx.send("Prefix should be less than 5 characters in lenght.")
        else:
            db.execute("UPDATE guilds SET Prefix = ? WHERE GuildID = ?", new, ctx.guild.id)

        embed = create_embed("New Prefix Set", 
                            f"New Prefix Set to {new} by {ctx.message.author}.", color=Color.green())

        await self.bot.log_channel.send(embed=embed)
        await ctx.send(f"Prefix set to '{new}'.")

    @command(name="yoink", aliases=["steal", "set_yoink", "set_steal"])
    async def set_yoink(self, ctx, message_id: str):
        if message_id == self.bot.reaction_yoink:
            await ctx.send("Yoinker already set to that message.")

        elif not re.match("\d", message_id):
            await ctx.send("Invalid message ID. Enter message ID for reaction emote yoinker.")
        else:
            # db.execute("UPDATE guilds SET YoinkID = ? WHERE GuildID = ?", message_id, ctx.guild.id)
            self.bot.reaction_yoink = message_id
            embed = create_embed("New Yoinker Message Set", 
                                f"Yoinker message set to message with id {self.bot.reaction_yoink}.", color=Color.dark_magenta())

            await self.bot.log_channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Meta(bot))