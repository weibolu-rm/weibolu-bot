from discord.ext.commands import Cog, command, has_permissions
from ..db import db 

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
            await ctx.send(f"Prefix set to '{new}''.")

def setup(bot):
    bot.add_cog(Meta(bot))