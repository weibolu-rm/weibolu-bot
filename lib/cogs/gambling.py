from datetime import datetime, timedelta
from discord.ext.commands import Cog, command
from weibolu import create_embed
from discord import Color, Member
from random import randint, choice
from ..db import db

# TODO: option to limit certain commands (like gambling) to a specific channel?
class Gambling(Cog):
    def __init__(self, bot):
        self.bot = bot

    async def reward_points(self, ctx, amount):
        db.execute("UPDATE member_points SET points = points + ? WHERE member_id = ? AND guild_id = ?;", 
                    amount, ctx.author.id, ctx.guild.id)

    async def remove_points(self, ctx, amount):
        db.execute("UPDATE member_points SET points = points - ? WHERE member_id = ? AND guild_id = ?;", 
                    amount, ctx.author.id, ctx.guild.id)

    @command(name="coin", aliases=["c", "flip"])
    async def coin_flip(self, ctx, choice, amount: int):
        won = False
        points = db.field("SELECT points FROM member_points WHERE member_id = ? AND guild_id = ?;",
                    ctx.author.id, ctx.guild.id);

        if amount > points:
            await ctx.send("You don't have enough :coin: !")
            return
        if amount < 10:
            await ctx.send("Minimum bet of 10 :coin:.")
            return

        # for some reason choice() not working so using randint
        flip = randint(0, 1)
        if flip == 0:
            flip = "tails"
        else:
            flip = "heads"
            
        await ctx.send(f"**{flip}**!")


        if flip not in ["tail", "tails", "t", "head", "heads", "h"]:
            await ctx.send("Wrong argument. Try 'heads' or 'tails'.")
        elif flip == "tails" and choice.lower() in ["tail", "tails", "t"]: 
            won = True
        elif flip == "heads" and choice.lower() in ["head", "heads", "h"]:
            won = True
        else:
            won = False

        if won:
            await self.reward_points(ctx, amount)  
            await ctx.send(f"You win {amount * 2} :coin:!")

        else:
            await self.remove_points(ctx, amount)
            await ctx.send(f"You lost {amount} :coin:...")

        db.commit()

def setup(bot):
    bot.add_cog(Gambling(bot))