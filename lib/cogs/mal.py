import asyncio
from discord.ext.commands import Cog, command, cooldown, BucketType
from datetime import datetime
from jikanpy import AioJikan
from jikanpy.exceptions import APIException
from weibolu import create_embed
import json

class Mal(Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @cooldown(2, 20, BucketType.user)
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

        fields = [
                    ("**Type**:", anime_type, False),
                    ("**URL**:", url, False),
                    ("**Aired :**", aired, True),
                    ("**Broadcast :**", broadcast, True),
                    ("**Score:**",score, True),
                    ("**Episodes:**",episodes, True)]

        embed = create_embed(title=u"{}【{}】".format(title, title_japanese),
                       description=f"\"{synopsis}\"", color=0x003F87, 
                       image_url=image, fields=fields)
        
        await ctx.send(embed=embed)
        await jikan.close()



    @cooldown(2, 20, BucketType.user)
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


        title = manga.get("title")
        title_japanese = manga.get("title_japanese")
        url = manga.get("url")
        image = manga.get("image_url")
        synopsis = manga.get("synopsis")
        published = manga["published"].get("string")
        score = manga.get("score")
        broadcast = "N/A"
        if (chapters := manga.get("chapters")) is None:
            chapters = "N/A"

        fields = [
                    ("**URL**:", url, False),
                    ("**Published :**", published, True),
                    ("**Score:**",score, True),
                    ("**Chapters:**",chapters, True)]
         

        embed = create_embed(title=u"{}【{}】".format(title, title_japanese),
                        description=f"\"{synopsis}\"",
                        color=0x003F87, image_url=image, fields=fields) 
                   
        await ctx.send(embed=embed)
        await jikan.close()

# asyncio.run(jikan())
def setup(bot):
    bot.add_cog(Mal(bot))