import discord
from discord import Embed
from datetime import datetime

from discord.ext.commands import Cog, has_permissions
from discord.ext.commands import command, check

class admin(Cog):
    def __init__(self, bot):
        self.bot = bot

    @has_permissions(kick_members=True)
    @command(name="kick")
    async def kick(self, ctx, member: discord.Member, *, reason="None"):
        await member.kick(reason=reason)

        embed = Embed(title="Kicked", color=0xFF0000, timestamp=datetime.utcnow())
        fields = [("**User**:", f"{member} <@{member.id}>", False),
                   ("**Reason**:",reason, False),
                   ("**Kicked by**:",ctx.message.author, False)]
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(admin(bot))