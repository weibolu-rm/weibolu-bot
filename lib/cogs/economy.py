from datetime import datetime, timedelta
from discord.ext.commands import Cog, command, group
from weibolu import create_embed, strfdelta
from discord import Color, Member
from typing import Optional
from random import randint
from ..db import db

class Economy(Cog):
    def __init__(self, bot):
        self.bot = bot

    async def purchase_item(self, ctx, cost, item, i_amount):
        # potentially unsafe
        db.execute(f"UPDATE member_points SET points = points - ?, {item} = {item} + ?  WHERE member_id = ? AND guild_id = ?;", 
                    cost, i_amount, ctx.author.id, ctx.guild.id)

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

    # specific for daily check in, has a 12h cooldown
    async def add_daily_points(self, message, points_to_add):
        
        db.execute("UPDATE member_points SET points = points + ?, daily_cooldown = ? WHERE member_id = ? AND guild_id = ?;", 
                    points_to_add, (datetime.utcnow()+timedelta(hours=12)).isoformat(), message.author.id, message.guild.id)
        db.commit() # users are probably immediately going to check for points



    @group()
    async def buy(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid buy command passed.")
    
    @buy.command()
    async def guildhouse(self, ctx):
        price = 5000
        points, guild_house = db.record("SELECT points, guild_house FROM member_points WHERE member_id = ? AND guild_id = ?;",
                                    ctx.author.id, ctx.guild.id) 
        if int(guild_house) == 1:
            await ctx.send("You already own a Guild House!")
            return
        
        if int(points) < price:
            await ctx.send(f"A Guild House is {price} :coin:. You don't have enough funds!")
            return

        # purchase guild house
        await self.purchase_item(ctx, price, "guild_house", 1)
        await ctx.send(f"Congratulations! You purchased a Guild House for {price} :coin:.")

        db.commit()


    @buy.command(aliases=["workers", "w"])
    async def worker(self, ctx, amount=1):
        if amount <= 0:
            await ctx.send("Invalid amount passed.")
            return

        price = 3000
        points, guild_house, workers = db.record("SELECT points, guild_house, workers FROM member_points WHERE member_id = ? AND guild_id = ?;",
                                    ctx.author.id, ctx.guild.id) 
        if int(guild_house) == 0:
            await ctx.send("You need to purchase a Guild House to have workers!")
            return
        
        msg_prefix = "1 worker"
        if amount > 1:
            price = amount * price
            msg_prefix = f"{amount} workers"

        if int(points) < price:
            await ctx.send(f"{msg_prefix} is {price} :coin:. You don't have enough funds!")
            return

        # purchase worker(s)
        await self.purchase_item(ctx, price, "workers", amount)
        new_amount = int(amount + workers)
        await ctx.send(f"Congratulations! You purchased {msg_prefix} for {price} :coin:.\nYou now own {new_amount} workers.")

        db.commit()

    @command(name="daily", aliases=["claim"])
    async def daily_check_in(self, ctx):
        points, daily_cooldown, guild_house, workers = db.record("SELECT points, daily_cooldown, guild_house, workers FROM member_points WHERE member_id = ? AND guild_id = ?;",
                                    ctx.author.id, ctx.guild.id) 
        # checking if user can receive points
        cooldown_datetime = datetime.fromisoformat(daily_cooldown)
        cooldown = strfdelta(cooldown_datetime - datetime.utcnow(), "{hours} hours and {minutes} minutes")

        if  datetime.utcnow() > cooldown_datetime:

            # Member owns guild house and potentially workers
            if int(guild_house) == 1:
                points_to_add = 500
                worker_bonus = 0
                if int(workers) > 0:
                    worker_bonus = int(workers) * 200
                    points_to_add = points_to_add + worker_bonus

                await ctx.send(f"""200 daily :coin:
300 :coin: from guild house
{worker_bonus} :coin: from {workers} workers
{points_to_add} :coin: claimed!""")

            # Member has no guild house, default points
            else:
                points_to_add = 200
                await ctx.send(f"200 daily :coin: claimed!")

            await self.add_daily_points(ctx.message, points_to_add)

        else:
            await ctx.send(f"You can claim your daily points **{cooldown}** from now.", delete_after=10)
            


    @command(name="points", aliases=["pts", "economy", "balance", "bal"])
    async def display_points(self, ctx, member: Optional[Member]):
        member = member or ctx.author

        points = db.field("SELECT points FROM member_points WHERE member_id = ? AND guild_id = ?;",
        member.id, member.guild.id);

        if points is not None:
            embed = create_embed("Points :purse:", f"{member.display_name} has {points} :coin:.",
            color=Color.blue(), thumbnail_url=member.avatar_url)

            await ctx.send(embed=embed)
        else:
            await ctx.send("That member does not have any point data.")

    @command(name="asset", aliases=["assets"])
    async def display_assets(self, ctx, member: Optional[Member]):
        member = member or ctx.author

        guild_house, workers, points = db.record("SELECT guild_house, workers, points FROM member_points WHERE member_id = ? AND guild_id = ?;",
        member.id, member.guild.id);

        result = ""
        net_worth = points
        if int(guild_house) == 1:
            net_worth += 5000
            result += ":house: Owns a guild house\n"
            
            if int(workers) > 0:
                net_worth += int(workers) * 3000
                result += f":tools: {workers} workers\n"

        if points is not None:
            result += f":purse: {points}\n"

        elif points is None and int(guild_house) == 0:
            await ctx.send("That member does not have any asset data.")
            return

        embed = create_embed(f":bank: {member.display_name}'s Assets", f"{result}\n**net worth**: {net_worth} :coin:",
        color=Color.blue(), thumbnail_url=member.avatar_url)
        await ctx.send(embed=embed)

    @Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        await self.process_points(message)

def setup(bot):
    bot.add_cog(Economy(bot))
