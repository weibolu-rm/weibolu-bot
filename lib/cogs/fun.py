from discord.ext.commands import Cog, command, has_permissions, cooldown, BucketType, group
from discord.ext.commands import has_permissions
from ..urbandict import urbandict as ud
from ..osu import osu as osu
from discord import Color, Emoji, HTTPException
from weibolu import create_embed
from ..db import db


class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot


    @cooldown(2, 20, BucketType.user)
    @command(name="define", aliases=["ud"])
    async def define(self, ctx, *, expression: str):
        defs = ud.define(expression)
        if defs:
            await ctx.send(f"{defs[0]}")


    @cooldown(2, 20, BucketType.user)
    @group()
    async def osu(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid osu command passed.")


    #TODO: register user


    @osu.command(aliases=["u"])
    async def update(self, ctx, uid : int):
        response = osu.updateUser(uid)
        if not response:
            await ctx.send("Problem updating user.")
            return
        if not response['exists']:
            await ctx.send("User does not exist.")
            return

        print(response)

        # user gets updated
        await ctx.send(f"User **{response['username']}** updated.")
        user_url = f"https://ameobea.me/osutrack/user/{response['username']}"
        highscores = response['newhs']
        rank_gained = str(response['pp_rank'])
        acc_gained = str(response['accuracy'])

        # rank gained +-
        if int(response['pp_rank']) >= 0:
            rank_gained = "+" + str(response['pp_rank'])

        # acc gain
        if float(response['accuracy']) >= 0:
            acc_gained = "+" + str(response['accuracy'])

        # there is a change
        if int(response['pp_rank']) != 0 or float(response['pp_raw']) != 0.0:
            await ctx.send(f"Rank: {rank_gained} ({response['pp_raw']}pp in {response['playcount']} plays).")
            await ctx.send(f"Accuracy: {acc_gained}")
        else:
            await ctx.send(f"No changes.")
            return

        # if there's only 1 new hs, display info
        if len(highscores) == 1:
            highscore = highscores[0]
            hs_max_combo = highscore['maxcombo']
            hs_pp = highscore['pp']
            hs_fc = highscore['perfect'] # 0 or 1
            hs_rank = highscore['rank'] # letter rank
            hs_ranking = highscore['ranking'] # ranking in top 100
            hs_miss = highscore['countmiss']
            is_fc = f"{hs_miss}x miss"
            if int(hs_fc) == 1:
                is_fc = "FC"
                
            await ctx.send(f"New highscore (#{hs_ranking + 1})! [{hs_pp}pp] '{hs_rank}' {hs_max_combo}x max combo {is_fc}." )
            await ctx.send(f"More info on {user_url}.")

        elif len(highscores) > 1 :
            await ctx.send(f"{len(highscores)} new highscore(s)! View them on {user_url}")


    @osu.command()
    async def peak(self, ctx, uid : int):
        response = osu.getUserPeak(uid)
        if response:
            if not response['best_global_rank']:
                await ctx.send("Could not find user.")
                return

            user = osu.updateUser(uid)
            await ctx.send(f"""
User **{user['username']}**:
Peak rank: {response['best_global_rank']}
Peak Acc: {round(response['best_accuracy'], 3)}%""")




    # TODO: make a seperate reaction Cog
    @Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if "???" in message.content:
            await message.channel.send("<:KannaWhat:743663211584159835>")

        if message.content.lower().startswith("hey kids"):
            await message.channel.send("<:KannaPolice:743272223414026332>")   

            
def setup(bot):
    bot.add_cog(Fun(bot))
