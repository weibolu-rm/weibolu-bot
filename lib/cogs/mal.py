import asyncio
from discord.ext.commands import Cog, command
from discord import Embed
from datetime import datetime
from jikanpy import AioJikan
from jikanpy.exceptions import APIException
import json

# import difflib
# I should parse the titles and find the closest match using diflib.get_close_matches


async def jikan(*, query="naruto"):
    async with AioJikan() as aio_jikan:

        results = await aio_jikan.search("anime", query)

        with open ("anime.json", "w") as f:
            json.dump(results, f, indent=2)

        return results


class mal(Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @command(name="mal")
    async def mal(self, ctx, *, query):

        try:
            result = await jikan(query=query)
        except APIException:
            await ctx.send("Problem connecting to the API. Please try again.")
            return
        except Exception:
            await ctx.send(f"Problem finding {query}. Please try a different query.")
            


        #taking first result for now
        if len(result["results"]) >= 1:
            anime = result["results"][0]
        else:
            await ctx.send(f"Problem finding {query}. Please try a different query.")
            return

        if end := anime["end_date"] is None:
            end = "N/A"
        else:
            end = anime["end_date"][:10]

        if (episodes := anime["episodes"]) == 0:
            episodes = "N/A"

        embed = Embed(title=anime["title"], color=0x003F87, timestamp=datetime.utcnow())
        fields = [("**URL**:", anime["url"], False),
                   ("**Start date:**", anime["start_date"][:10], False),
                   ("**End date:**", end, True),
                   ("**Synopsis:**",f"\"{anime['synopsis']}\"", False),
                   ("**Score:**",anime["score"], True),
                   ("**Episodes:**",episodes, True)]
                   
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
            embed.set_image(url=anime["image_url"])
        await ctx.send(embed=embed)

# asyncio.run(jikan())
def setup(bot):
    bot.add_cog(mal(bot))