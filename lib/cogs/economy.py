from datetime import datetime, timedelta
from discord.ext.commands import Cog, command
from weibolu import create_embed
from discord import Color, Member
from typing import Optional
from random import randint
from ..db import db

class Economy(Cog):
    def __init__(self, bot):
        self.bot = bot

    async def process_points(self, message):
        points, points_lock = db.record("SELECT points, points_lock FROM member_points WHERE member_id = ? AND guild_id = ?;",
                                message.author.id, message.guild.id) 
        # checking if user can receive points
        if  datetime.utcnow() > datetime.fromisoformat(points_lock):
            await self.add_points(message)

    # for member activity
    async def add_points(self, message):
        points_to_add = randint(5,15)
        
        db.execute("UPDATE member_points SET points = points + ?, points_lock = ? WHERE member_id = ? AND guild_id = ?;", 
                    points_to_add, (datetime.utcnow()+timedelta(minutes=5)).isoformat(), message.author.id, message.guild.id)

    # specific for daily check in, has a 24h cooldown
    async def add_daily_points(self, message):
        points_to_add = 200
        
        db.execute("UPDATE member_points SET points = points + ?, daily_cooldown = ? WHERE member_id = ? AND guild_id = ?;", 
                    points_to_add, (datetime.utcnow()+timedelta(days=1)).isoformat(), message.author.id, message.guild.id)
        db.commit() # users are probably immediately going to check for points

    @command(name="daily", aliases=["claim"])
    async def daily_check_in(self, ctx):
        points, daily_cooldown = db.record("SELECT points, daily_cooldown FROM member_points WHERE member_id = ? AND guild_id = ?;",
                                    ctx.author.id, ctx.guild.id) 
        # checking if user can receive points
        if  datetime.utcnow() > datetime.fromisoformat(daily_cooldown):
            await self.add_daily_points(ctx.message)
            await ctx.send(f"200 daily points claimed!")

        else:
            await ctx.send(f"You have already claimed your daily check-in. Next one is in {datetime.fromisoformat(daily_cooldown) - datetime.utcnow()}.")


    @command(name="points", aliases=["pts", "economy"])
    async def display_points(self, ctx, member: Optional[Member]):
        member = member or ctx.author

        points = db.field("SELECT points FROM member_points WHERE member_id = ? AND guild_id = ?;",
        member.id, member.guild.id);

        if points is not None:
            embed = create_embed("Points", f"{member.display_name} has {points} points.",
            color=Color.blue()    , thumbnail_url=member.avatar_url)

            await ctx.send(embed=embed)
        else:
            await ctx.send("That member does not have any point data.")

    @Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        await self.process_points(message)

def setup(bot):
    bot.add_cog(Economy(bot))
