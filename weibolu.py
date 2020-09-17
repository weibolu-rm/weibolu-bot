import discord


from datetime import datetime
from discord import Embed
from discord.ext import commands
from discord.errors import Forbidden

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from lib.db import db 

OWNER_ID = 91939126634364928

PREFIX = "!"
EXTENSIONS = [
    "lib.cogs.ping",
    "lib.cogs.utils",
    "lib.cogs.admin",
    "lib.cogs.mal",
    "lib.cogs.fun"
]


class weiboluBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=PREFIX,
                         description="I don't know what I'm doing")
        self.owner_id = OWNER_ID
        self.ready = False
        self.guild = None
        self.Scheduler = AsyncIOScheduler()

        db.autosave(self.Scheduler)


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
        elif isinstance(error, commands.BadArgument):
            pass
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"<@{ctx.message.author.id}>, this command is on cooldown. Please try again in {error.retry_after:,.2f} seconds.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(f"<@{ctx.message.author.id}>, you do not have permission to do that.")
        elif hasattr(error, "original"):

            if isinstance(error.original, Forbidden):
                await ctx.send("I do not have permission to do that <:FeelsBadMan:743242240364773506>")

            else:
                raise error.original
        else:
            raise error

    async def on_ready(self):
        if not self.ready:
            self.ready = True
            self.guild = self.get_guild(562178654151507981)
            self.stdout = self.get_channel(562190083374055445)
            self.Scheduler.start()
            print("bot ready")

        else:
            print("bot reconnected")
        

    async def on_message(self, message):
        if message.author.bot:
            return

        await self.process_commands(message)
        ctx = await self.get_context(message)

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
