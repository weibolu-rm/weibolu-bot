from datetime import datetime, timedelta
from weibolu import create_embed
from discord.ext.commands import Cog, command, has_permissions
from discord import Color, Member, NotFound, TextChannel
from typing import Optional
from random import randint
from ..db import db

def get_guild_lvl_channel(guild_id: int):
    lvl_channel = db.field("SELECT lvl_channel FROM guilds WHERE guild_id = ?;", guild_id)
    return lvl_channel

def guild_lvl_enabled(guild_id: int):
    lvl_enabled = db.field("SELECT lvl_toggle FROM guilds WHERE guild_id = ?;", guild_id)
    if lvl_enabled == 1:
        return True
    return False

class Exp(Cog):
    def __init__(self, bot):
        self.bot = bot

    async def process_xp(self, message):
        xp, lvl, xp_lock = db.record("SELECT xp, level, xp_lock FROM member_exp WHERE member_id = ?", message.author.id) 
        # checking if user can receive exp
        if  datetime.utcnow() > datetime.fromisoformat(xp_lock):
            await self.add_xp(message, xp, lvl)


    async def add_xp(self, message, xp, lvl):
        xp_to_add = randint(5,15)
        new_lvl = int(((xp+xp_to_add)//42) ** 0.55)
        
        # exp lock set to 1 min for now
        db.execute("UPDATE member_exp SET xp = xp + ?, level = ?, xp_lock = ? WHERE member_id = ? AND guild_id = ?", 
                    xp_to_add, new_lvl, (datetime.utcnow()+timedelta(seconds=60)).isoformat(), message.author.id, message.guild.id)

        if new_lvl > lvl and guild_lvl_enabled(message.guild.id):

            embed = create_embed(f"Level Up!", f"Yay! {message.author.mention}, you've reached level {new_lvl:,}.",
            color=Color.magenta(), image_url=message.author.avatar_url)

            # if notifications are toggled, will send to specific channel if exists, otherwise the channel
            # with the message that leveled the user
            lvl_channel = self.bot.get_channel(get_guild_lvl_channel(message.guild.id))
            if lvl_channel is not None:
                await lvl_channel.send(embed=embed)
            else:
                await message.channel.send(embed=embed)

    @command(name="level", aliases=["lvl"])
    @has_permissions(manage_guild = True)
    async def level(self, ctx, arg, channel: TextChannel = None):
        if arg == "toggle" or arg == "t":
            guild_toggle = db.field("SELECT lvl_toggle FROM guilds WHERE guild_id = ?;", ctx.guild.id)
            on_off = ""


            if guild_toggle == 1:
                on_off = "Off"
                db.execute("UPDATE guilds SET lvl_toggle = 0 WHERE guild_id = ?;", ctx.guild.id)
                db.commit()
                await ctx.send("Level notificationgs disabled.")
            else:
                on_off = "On"
                db.execute("UPDATE guilds SET lvl_toggle = 1 WHERE guild_id = ?;", ctx.guild.id)
                db.commit()
                await ctx.send("Level notificationgs enabled.")

            embed = create_embed(f"Level Notification Toggled {on_off}",
                    f"Level notifications toggled by {ctx.message.author}.", color=Color.gold())

            log_channel = self.bot.get_log_channel(ctx.guild.id)
            if log_channel is not None:
                await log_channel.send(embed=embed)


            return
        
        if arg == "clear" or arg == "clr":
            db.execute("UPDATE guilds SET lvl_channel = ? WHERE guild_id = ?;", None, ctx.guild.id)
            db.commit()
            embed = create_embed("Level Channel Cleared", 
                                f"Level channel was cleared by {ctx.message.author}.", color=Color.red())

            log_channel = self.bot.get_log_channel(ctx.guild.id)
            if log_channel is not None:
                await log_channel.send(embed=embed)
            await ctx.send(f"Successfully cleared level channel.")

            return


        if arg != "channel":
            await ctx.send("Invalid argument. !level channel #lvl-channel")
        elif self.bot.get_channel(channel.id) is None:
            await ctx.send("Invalid channel.")
        else:
            db.execute("UPDATE guilds SET lvl_channel = ? WHERE guild_id = ?;", channel.id, ctx.guild.id)
            db.commit()
            await ctx.send(f"Level channel set to <#{channel.id}>.")

        embed = create_embed("Level Channel Set",
                            f"New Level Channel Set to <#{channel.id}> by {ctx.message.author}.", color=Color.gold())

        log_channel = self.bot.get_log_channel(ctx.guild.id)
        if log_channel is not None:
            await log_channel.send(embed=embed)


    @command(name="exp", aliases=["xp"])
    async def display_exp(self, ctx, member: Optional[Member]):
        member = member or ctx.author

        xp, lvl = db.record("SELECT xp, level FROM member_exp WHERE member_id = ? AND guild_id = ?;",
        member.id, member.guild.id) or (None, None)

        if lvl is not None:
            embed = create_embed("Level", f"{member.display_name} is level {lvl:,} with {xp:,} XP.",
            color=Color.teal(), thumbnail_url=member.avatar_url)

            await ctx.send(embed=embed)
        else:
            await ctx.send("That member does not have any exp data.")


    @command(name="rank")
    async def display_rank(self, ctx):
        ranks = db.records("SELECT * FROM member_exp WHERE guild_id = ? ORDER BY xp DESC;", ctx.guild.id)
        fields = []

        for i, rank in enumerate(ranks):
            if i > 9: 
                break

            try:
                user = await self.bot.fetch_user(rank[0])
            except NotFound as e:
                i -= 1
                continue

            fields.append(("**Rank**", f"{i+1}" , True))
            fields.append(("**Member**", f"{user}" , True))
            fields.append(("**LVL (XP)**", f"{rank[3]} ({rank[2]}XP)" , True))

        embed = create_embed("Level Ranking", f"Member level rankings for {ctx.guild.name}.",
            fields=fields, color=Color.magenta())
            
        await ctx.send(embed=embed)



    @Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        await self.process_xp(message)

def setup(bot):
    bot.add_cog(Exp(bot))
