from discord.ext.commands import Cog, command, has_permissions
from ..db import db 
from discord import Color, NotFound, HTTPException
from weibolu import create_embed

class Emoji(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="yoink", aliases=["steal", "set_yoink", "set_steal"])
    @has_permissions(manage_guild = True)
    async def set_yoink(self, ctx, message_id: int):
        
        message = await ctx.fetch_message(message_id)


        if message_id == self.bot.reaction_yoink:
            await ctx.send("Yoinker already set to that message.")

        # elif not re.match("\d", message_id):
        #     await ctx.send("Invalid message ID. Enter message ID for reaction emote yoinker.")
        else:
            # db.execute("UPDATE guilds SET YoinkID = ? WHERE GuildID = ?", message_id, ctx.guild.id)
            self.bot.reaction_yoink = message_id
            embed = create_embed("New Yoinker Message Set", 
                                f"Yoinker message set to message with id {self.bot.reaction_yoink}. {message.jump_url}", color=Color.dark_magenta())

            log_channel = self.bot.get_log_channel(ctx.guild.id)
            if log_channel is not None:
                await log_channel.send(embed=embed)

    # not wroking for some reason
    @set_yoink.error
    async def set_yoink_error(self, ctx, error):
        print("test")
        if isinstance(error, NotFound): 
            await ctx.send("Wrong argument. Message id could not be found.")



def setup(bot):
    bot.add_cog(Emoji(bot))