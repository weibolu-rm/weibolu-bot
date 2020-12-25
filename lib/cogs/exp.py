from datetime import datetime, timedelta
from weibolu import create_embed
from discord.ext.commands import Cog, command
from discord import Color, Member
from typing import Optional
from random import randint
from ..db import db


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
        db.execute("UPDATE member_exp SET xp = xp + ?, level = ?, xp_lock = ? WHERE member_id = ?", 
                    xp_to_add, new_lvl, (datetime.utcnow()+timedelta(seconds=60)).isoformat(), message.author.id)

        if new_lvl > lvl:
            embed = create_embed(f"Level Up!", f"Yay! {message.author.mention}, you've reached level {new_lvl:,}.",
            color=Color.magenta(), image_url=message.author.avatar_url)
            #TODO: send in specific level channel
            await message.channel.send(embed=embed)


    @command(name="level", aliases=["lvl"])
    async def display_level(self, ctx, member: Optional[Member]):
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
        ranks = db.records("SELECT * FROM member_exp WHERE guild_id = ? ORDER BY xp DESC;", ctx.message.guild.id)
        fields = []

        for i, rank in enumerate(ranks):
            i+= 1
            if i > 10: 
                break

            if (user := self.bot.get_user(rank[0])) is not None:
                fields.append(("**Rank**", f"{i}" , True))
                fields.append(("**Member**", f"{user}" , True))
                fields.append(("**LVL**", f"{rank[3]} ({rank[2]}XP)" , True))

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
