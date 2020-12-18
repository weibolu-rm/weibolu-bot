from discord.ext.commands import Cog, command, has_permissions
from ..db import db 
from discord import Color, TextChannel
from weibolu import create_embed, intents
from typing import Optional

class Meta(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="prefix")
    @has_permissions(manage_guild=True)
    async def change_prefix(self, ctx, new: str):
        if len(new) > 5:
            await ctx.send("Prefix should be less than 5 characters in lenght.")
        else:
            db.execute("UPDATE guilds SET prefix = ? WHERE guild_id = ?;", new, ctx.guild.id)
            db.commit()

        embed = create_embed("New Prefix Set", 
                            f"New Prefix Set to {new} by {ctx.message.author}.", color=Color.green())

        log_channel = self.bot.get_log_channel(ctx.guild.id)
        if log_channel is not None:
            await log_channel.send(embed=embed)
        await ctx.send(f"Prefix set to '{new}'.")

    @command(name="log")
    @has_permissions(manage_guild=True)
    async def set_log_channel(self, ctx, arg, channel: TextChannel):
        if arg != "channel":
            await ctx.send("Invalid argument. !log channel #log-channel")
        elif self.bot.get_channel(channel.id) is None:
            await ctx.send("Invalid channel.")
        else:
            db.execute("UPDATE guilds SET log_channel = ? WHERE guild_id = ?;", channel.id, ctx.guild.id)
            db.commit()
            await ctx.send(f"Log channel set to <#{channel.id}>.")

        embed = create_embed("Log Channel Set",
                            f"New Log Channel Set to <#{channel.id}>.", color=Color.gold())

        log_channel = self.bot.get_log_channel(ctx.guild.id)
        if log_channel is not None:
            await log_channel.send(embed=embed)

    @command(name="welcome")
    @has_permissions(manage_guild=True)
    async def set_welcome_channel(self, ctx, arg, channel: TextChannel):
        if arg != "channel":
            await ctx.send("Invalid argument. !welcome channel #welcome-channel")
        elif self.bot.get_channel(channel.id) is None:
            await ctx.send("Invalid channel.")
        else:
            db.execute("UPDATE guilds SET welcome_channel = ? WHERE guild_id = ?;", channel.id, ctx.guild.id)
            db.commit()
            await ctx.send(f"Welcome channel set to <#{channel.id}>.")
        
        embed = create_embed("Welcome Channel Set",
                            f"New Welcome Channel Set to <#{channel.id}>.", color=Color.gold())

        log_channel = self.bot.get_log_channel(ctx.guild.id)
        if log_channel is not None:
            await log_channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Meta(bot))