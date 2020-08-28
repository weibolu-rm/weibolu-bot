import asyncio
from discord.ext.commands import Cog, command
from discord import Embed
from datetime import datetime
from jikanpy import AioJikan
from jikanpy.exceptions import APIException
import json

class mal(Cog):
    def __init__(self, bot):
        self.bot = bot
        
        
    @command(name="anime", aliases=["mal"])
    async def mal(self, ctx, *, query):
        jikan = AioJikan()

        try:
            result = await jikan.search("anime",query)
        except APIException:
            await ctx.send("Problem connecting to the API. Please try again.")
            await jikan.close()
            return

        #taking first result for now
        if len(result["results"]) > 0:
            result = result["results"][0]
        else:
            await ctx.send(f"No results for <{query}>.")
            await jikan.close()
            return

        try:
            anime = await jikan.anime(result.get("mal_id"))
        except APIException:
            await ctx.send("Problem connecting to the API. Please try again.")
            await jikan.close()
            return

        # with open("anime.json", "w") as f:
        #     json.dump(anime,f,indent=2)

        title = anime.get("title")
        title_japanese = anime.get("title_japanese")
        anime_type = anime.get("type")
        url = anime.get("url")
        image = anime.get("image_url")
        airing = anime.get("airing")
        aired = anime["aired"].get("string")
        synopsis = anime.get("synopsis")
        score = anime.get("score")
        broadcast = "N/A"
        if airing:
            broadcast = anime.get("broadcast")
        if (episodes := anime.get("episodes")) is None:
            episodes = "N/A"

    #     print("""
    # title = {}
    # title_japanese {} 
    # url = {}
    # image = {} 
    # aired = {}
    # synopsis = {}
    # airing = {}
    # score = {}
    # broadcast = {}
    # episodes = {}
    #     """.format(title,title_japanese,url,image,aired,synopsis,airing,score,broadcast,episodes))

        embed = Embed(title=u"{}【{}】".format(title, title_japanese),
                        description=f"\"{synopsis}\"",
                        color=0x003F87, timestamp=datetime.utcnow())
        fields = [
                    ("**Type**:", anime_type, False),
                    ("**URL**:", url, False),
                    ("**Aired :**", aired, True),
                    ("**Broadcast :**", broadcast, True),
                    # ("**Synopsis:**",f"\"{synopsis}\"", False),
                    ("**Score:**",score, True),
                    ("**Episodes:**",episodes, True)]
                   
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        embed.set_image(url=image)
        await ctx.send(embed=embed)
        await jikan.close()



    @command(name="manga")
    async def manga(self, ctx, *, query):
        jikan = AioJikan()

        try:
            result = await jikan.search("manga",query)
        except APIException:
            await ctx.send("Problem connecting to the API. Please try again.")
            await jikan.close()
            return

        #taking first result for now
        if len(result["results"]) > 0:
            result = result["results"][0]
        else:
            await ctx.send(f"No results for <{query}>.")
            await jikan.close()
            return

        try:
            manga = await jikan.manga(result.get("mal_id"))
        except APIException:
            await ctx.send("Problem connecting to the API. Please try again.")
            await jikan.close()
            return

        # with open("manga.json", "w") as f:
        #     json.dump(manga,f,indent=2)

        title = manga.get("title")
        title_japanese = manga.get("title_japanese")
        url = manga.get("url")
        image = manga.get("image_url")
        # aired = manga["aired"].get("string")
        synopsis = manga.get("synopsis")
        # status = manga.get("status")
        published = manga["published"].get("string")
        score = manga.get("score")
        broadcast = "N/A"
        # if airing:
        #     broadcast = manga.get("broadcast")
        if (chapters := manga.get("chapters")) is None:
            chapters = "N/A"

        embed = Embed(title=u"{}【{}】".format(title, title_japanese),
                        description=f"\"{synopsis}\"",
                        color=0x003F87, timestamp=datetime.utcnow())
        fields = [
                    ("**URL**:", url, False),
                    ("**Published :**", published, True),
                    # ("**Broadcast :**", broadcast, True),
                    # ("**Synopsis:**",f"\"{synopsis}\"", False),
                    ("**Score:**",score, True),
                    ("**Chapters:**",chapters, True)]
                   
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        embed.set_image(url=image)
        await ctx.send(embed=embed)
        await jikan.close()

# asyncio.run(jikan())
def setup(bot):
    bot.add_cog(mal(bot))