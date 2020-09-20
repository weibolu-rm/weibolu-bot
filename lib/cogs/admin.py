import discord
from datetime import datetime
from weibolu import create_embed
from discord.ext.commands import Cog, has_permissions
from discord.ext.commands import command, check

class Admin(Cog):
    def __init__(self, bot):
        self.bot = bot

    @has_permissions(kick_members=True)
    @command(name="kick")
    async def kick(self, ctx, member: discord.Member, *, reason="None"):
        await member.kick(reason=reason)

        fields = [("**User**:", f"{member} <@{member.id}>", False),
                   ("**Reason**:",reason, False),
                   ("**Kicked by**:",ctx.message.author, False)]

        embed = create_embed(title="Kicked", description="", color=0xFF0000, fields=fields)
        
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Admin(bot))