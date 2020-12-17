from discord.ext.commands import Cog, command, has_permissions
from ..db import db 
from discord import Color
from weibolu import create_embed, intents

class Meta(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="prefix")
    @has_permissions(manage_guild=True)
    async def change_prefix(self, ctx, new: str):
        if len(new) > 5:
            await ctx.send("Prefix should be less than 5 characters in lenght.")
        else:
            db.execute("UPDATE guilds SET prefix = ? WHERE guild_id = ?", new, ctx.guild.id)

        embed = create_embed("New Prefix Set", 
                            f"New Prefix Set to {new} by {ctx.message.author}.", color=Color.green())

        await self.bot.log_channel.send(embed=embed)
        await ctx.send(f"Prefix set to '{new}'.")

    @command(name="test")
    @has_permissions(manage_guild=True)
    async def test(self, ctx):
        for guild in self.bot.guilds:
            async for member in guild.fetch_members():
                print(member.name)
        await ctx.send("done.")


def setup(bot):
    bot.add_cog(Meta(bot))