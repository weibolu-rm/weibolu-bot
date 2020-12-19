from discord import Member, Color
from weibolu import create_embed
from discord.ext.commands import Cog, has_permissions, bot_has_permissions
from discord.ext.commands import command, Greedy


class Admin(Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @has_permissions(kick_members=True)
    @bot_has_permissions(kick_members=True)
    @command(name="kick")
    async def kick(self, ctx, members: Greedy[Member], *, reason="None"):
        if not len(members):
            await ctx.send("Please sepcify a user to be kicked.") 
        for member in members:
            await member.kick(reason=reason)

            fields = [("**User**:", f"{member} <@{member.id}>", False),
                    ("**Reason**:",reason, False),
                    ("**Kicked by**:",ctx.message.author, False)]

            embed = create_embed("Kicked", "", color=0xFF0000, thumbnail_url=member.avatar_url, fields=fields)
        
            log_channel = self.bot.get_log_channel(ctx.guild.id)
            if log_channel is not None:
                await log_channel.send(embed=embed)


    @has_permissions(ban_members=True)
    @bot_has_permissions(ban_members=True)
    @command(name="ban")
    async def ban(self, ctx, members: Greedy[Member], *, reason="None"):
        if not len(members): 
            await ctx.send("Please specify a user to be banned.")
        for member in members:
            await member.ban(reason=reason)

            fields = [("**User**:", f"{member} <@{member.id}>", False),
                    ("**Reason**:",reason, False),
                    ("**Banned by**:",ctx.message.author, False)]

            embed = create_embed("Banned", "", color=0xFF0000, thumbnail_url=member.avatar_url, fields=fields)
        
            log_channel = self.bot.get_log_channel(ctx.guild.id)
            if log_channel is not None:
                await log_channel.send(embed=embed)

    # TODO: add ability to delete messages from specific user(s) 
    @has_permissions(manage_messages=True)
    @bot_has_permissions(manage_messages=True)
    @command(name="clear", aliases=["clr"])
    async def clear(self, ctx, amount=5):
        author = ctx.author
        f_msg = f"""```diff
- {author} deleted {amount} messages.
```
"""
        field = [("**Deleted by:**", ctx.message.author, False)]

        embed = create_embed("Message deleted", f"{amount} deleted in <#{ctx.channel.id}>.", 
        color=Color.gold(), thumbnail_url=ctx.author.avatar_url, fields=field)

        await ctx.channel.purge(limit=amount+1)
        await ctx.send(f_msg, delete_after=5)
        
        log_channel = self.bot.get_log_channel(ctx.guild.id)
        if log_channel is not None:
            await log_channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Admin(bot))