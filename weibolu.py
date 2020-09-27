import discord

from datetime import datetime
from discord import Embed
from discord.ext.commands import when_mentioned_or, Bot, MissingPermissions, Context
from discord.ext.commands import CommandNotFound, BadArgument, CommandOnCooldown
from discord.errors import Forbidden

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from lib.db import db 

OWNER_ID = 91939126634364928

# PREFIX = "!"
EXTENSIONS = [
    "lib.cogs.ping",
    "lib.cogs.utils",
    "lib.cogs.admin",
    "lib.cogs.mal",
    "lib.cogs.fun",
    "lib.cogs.meta",
    "lib.cogs.welcome",
    "lib.cogs.log",
    "lib.cogs.exp"
]

# can mention bot instead of prefix
def get_guild_prefix(bot, message):
    prefix = db.field("SELECT Prefix FROM guilds WHERE GuildID = ?", message.guild.id)
    return when_mentioned_or(prefix)(bot, message)


def create_embed(title, description, color=None, image_url=None, thumbnail_url=None, fields=None):
    if color is not None:
        em = Embed(title=title, description=description, 
        color=color, timestamp=datetime.utcnow())
    else:
        em = Embed(title=title, description=description, timestamp=datetime.utcnow())
    if image_url is not None:
        em.set_image(url=image_url)
    if thumbnail_url is not None:
        em.set_thumbnail(url=thumbnail_url)
    if fields is not None:
        for name, value, inline in fields:
            em.add_field(name=name, value=value, inline=inline)
    return em


class WeiboluBot(Bot):
    def __init__(self):
        super().__init__(command_prefix=get_guild_prefix,
                         description="I don't know what I'm doing")
        self.owner_id = OWNER_ID
        self.ready = False
        self.guild = self.get_guild(562178654151507981)
        self.Scheduler = AsyncIOScheduler()
        self.log_channel = self.get_channel(757112954599768064)

        db.autosave(self.Scheduler)


    def setup(self):
        for extension in EXTENSIONS:
            try:
                self.load_extension(extension)
            except Exception as e:
                print('Failed to load extension {}\n{}: {}'.format(
                    extension, type(e).__name__, e))

        print("setup complete")


    # update the db with guild and member info
    def update_db(self):
        db.multiexec("INSERT OR IGNORE INTO guilds (GuildID) VALUES (?)",
            ((guild.id,) for guild in self.guilds))

        db.multiexec("INSERT OR IGNORE INTO exp (UserID) VALUES (?)",
            ((member.id,) for guild in self.guilds for member in guild.members if not member.bot))

        db.commit()
        

    async def on_connect(self):
        print("we in bois")

    async def on_disconnect(self):
        print("aight ima head out")

    async def on_error(self, error, *args, **kwargs):
        if error == "on command_error":
            await args[0].send("Error: something went wrong.")

        raise

    # main error handling. For command specific errors, we can make those in the Cogs.
    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandNotFound):
           pass
        elif isinstance(error, BadArgument):
            pass
        elif isinstance(error, CommandOnCooldown):
            await ctx.send(f"<@{ctx.message.author.id}>, this command is on cooldown. Please try again in {error.retry_after:,.2f} seconds.")
        elif isinstance(error, MissingPermissions):
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
            self.log_channel = self.get_channel(757112954599768064)
            self.reaction_yoink = "759659429754437663"
            self.Scheduler.start()
            # self.fetch_bot_channels()
            self.update_db()

            print("bot ready")

        else:
            print("bot reconnected")


    # moved most things to Cogs
    async def on_message(self, message):
        if message.author.bot:
            return

        await self.process_commands(message)
        ctx = await self.get_context(message)


    # def fetch_bot_channels(self):
    #     self.reaction_yoink = db.field("SELECT YoinkID FROM guilds WHERE GuildID = ?", self.guild.id)
    #     print("fetched channels")



    def run(self):
        print("running setup...")
        self.setup()

        with open("./lib/token.0", "r", encoding="UTF-8") as t:
            self.token = t.read()

        super().run(self.token, reconnect=True)


if __name__ == "__main__":
    WeiboluBot = WeiboluBot()
    WeiboluBot.run()

