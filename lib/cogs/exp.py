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
        xp, lvl, xplock = db.record("SELECT XP, Level, XPLock FROM exp WHERE UserID = ?", message.author.id) 
        # checking if user can receive exp
        if  datetime.utcnow() > datetime.fromisoformat(xplock):
            await self.add_xp(message, xp, lvl)


    async def add_xp(self, message, xp, lvl):
        xp_to_add = randint(5,15)
        new_lvl = int(((xp+xp_to_add)//42) ** 0.55)
        
        # exp lock set to 1 min for now
        db.execute("UPDATE exp SET XP = XP + ?, Level = ?, XPLock = ? WHERE UserID = ?", 
                    xp_to_add, new_lvl, (datetime.utcnow()+timedelta(seconds=60)).isoformat(), message.author.id)

        if new_lvl > lvl:
            embed = create_embed(f"Level Up!", f"Yay! {message.author.mention}, you've reached level {new_lvl:,}.",
            color=Color.magenta(), image_url=message.author.avatar_url)
            await message.channel.send(embed=embed)


    @command(name="level", aliases=["lvl"])
    async def display_level(self, ctx, member: Optional[Member]):
        member = member or ctx.author

        xp, lvl = db.record("SELECT XP, Level FROM exp WHERE UserID = ?", member.id) or (None, None)

        if lvl is not None:
            embed = create_embed("Level", f"{member.display_name} is level {lvl:,} with {xp:,} XP.",
            color=Color.teal(), thumbnail_url=member.avatar_url)

            await ctx.send(embed=embed)
        else:
            await ctx.send("That member does not have any exp data.")

    @Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        await self.process_xp(message)

def setup(bot):
    bot.add_cog(Exp(bot))
