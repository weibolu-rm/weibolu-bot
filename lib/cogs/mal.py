import asyncio
from discord.ext.commands import Cog, command
from discord import Embed
from datetime import datetime
from jikanpy import AioJikan

async def jikan(*, query="naruto"):
    async with AioJikan() as aio_jikan:
        results = await aio_jikan.search(search_type="anime", query=query, parameters={})
        return results

        # with open ("anime.json", "w") as f:
        #     json.dump(naruto, f, indent=2)

#         for result in naruto["results"]:
#             f_result = f"""
# Title = {result["title"]}
# Url = {result["url"]}
# Synopsis = \"{result['synopsis']}\"
# """

class mal(Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @command(name="mal")
    async def mal(self, ctx, *, query):
        result = await jikan(query=query)
        print(query)
#         for item in result["results"]:
#             f_result = f"""
# Title = {item["title"]}
# Url = {item["url"]}
# Synopsis = \"{item['synopsis']}\"
# """
#             print(f_result)

        anime = result["results"][0]

        if end :=anime["end_date"] is None:
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