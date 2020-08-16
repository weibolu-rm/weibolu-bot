import discord


from datetime import datetime
from discord import Embed
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler

OWNER_ID = 562175478824304661

PREFIX = "!"
EXTENSIONS = [
    "lib.cogs.ping",
    "lib.cogs.utils"
]


class weiboluBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=PREFIX,
                         description="I don't know what I'm doing")
        self.owner_id = OWNER_ID
        self.ready = False
        self.guild = None
        self.Scheduler = AsyncIOScheduler()


    def setup(self):
        for extension in EXTENSIONS:
            try:
                self.load_extension(extension)
            except Exception as e:
                print('Failed to load extension {}\n{}: {}'.format(
                    extension, type(e).__name__, e))

        print("setup complete")

    async def on_connect(self):
        print("we in bois")

    async def on_disconnect(self):
        print("aight ima head out")

    async def on_error(self, error, *args, **kwargs):
        if error == "on command_error":
            await args[0].send("Error: something went wrong.")

        raise

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
           pass
        elif hasattr(error, "original"):
            raise error.original
        else:
            raise error

    async def on_ready(self):
        if not self.ready:
            self.ready = True
            self.guild = self.get_guild(562178654151507981)
            self.stdout = self.get_channel(562190083374055445)
            print("bot ready")

            #await self.stdout.send("we in bois")

            # embed = Embed(title="Begin hacking sequence", description="You're getting hacked.", 
            #             color=0xFF0000, timestamp=datetime.utcnow())
            # fields = [("Name","Value", True),
            #            ("Test","Testing", True),
            #            ("non inline","tester", False)]
            # for name, value, inline in fields:
            #     embed.add_field(name=name, value=value, inline=inline)
            # embed.set_author(name="Weibolu-bot", icon_url=self.guild.icon_url)
            # embed.set_thumbnail(url=self.guild.icon_url)
            # embed.set_image(url=self.guild.icon_url)
            # await self.stdout.send(embed=embed)

        else:
            print("bot reconnected")
        

    async def on_message(self, message):
        if message.author.bot:
            return

        await self.process_commands(message)
        ctx = await self.get_context(message)

        # if message.content == "!kill": 
        #     await self.logout()

        if "???" in message.content:
            await message.channel.send("<:KannaWhat:743663211584159835>")

        if message.content.lower().startswith("hey kids"):
            await message.channel.send("<:KannaPolice:743272223414026332>")

    def run(self):
        print("running setup...")
        self.setup()

        with open("./lib/token.0", "r", encoding="UTF-8") as t:
            self.token = t.read()

        super().run(self.token, reconnect=True)


if __name__ == "__main__":
    weiboluBot = weiboluBot()
    weiboluBot.run()
"""
open cv for image zooming,
gif speed?

Osu

MAL
"""