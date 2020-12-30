import discord

from datetime import datetime
from discord import Embed
from discord.ext.commands import when_mentioned_or, Bot, MissingPermissions, Context
from discord.ext.commands import CommandNotFound, BadArgument, CommandOnCooldown, MissingRequiredArgument
from discord.errors import Forbidden

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from lib.db import db 

OWNER_ID = 91939126634364928
intents = discord.Intents.default()
intents.members = True
intents.reactions = True

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
    "lib.cogs.exp",
    "lib.cogs.emoji",
    "lib.cogs.economy",
    "lib.cogs.gambling",
]

# can mention bot instead of prefix
def get_guild_prefix(bot, message):
    prefix = db.field("SELECT prefix FROM guilds WHERE guild_id = ?;", message.guild.id)
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
                         description="I don't know what I'm doing",
                         intent=intents)
        self.owner_id = OWNER_ID
        self.ready = False
        self.guild = self.get_guild(562178654151507981)
        self.Scheduler = AsyncIOScheduler()
        # self.log_channel = self.get_channel(757112954599768064)

        db.autosave(self.Scheduler)


    # load bot extensions (Cogs)
    def setup(self):
        for extension in EXTENSIONS:
            try:
                self.load_extension(extension)
            except Exception as e:
                print('Failed to load extension {}\n{}: {}'.format(
                    extension, type(e).__name__, e))

        print("setup complete")

    # update the db with guild and member info
    async def update_db(self):
        print("Updating db...")
        
        db.multiexec("INSERT OR IGNORE INTO guilds (guild_id, name) VALUES (?, ?);",
            ((guild.id, guild.name) for guild in self.guilds))

        # had to change the old guild.members to use an async alternative 
        for guild in self.guilds:
            async for member in guild.fetch_members(): 
                if not member.bot:
                    db.execute("""INSERT OR IGNORE INTO members 
                    (guild_id, member_id, username, nickname, discriminator, joined_date) 
                    VALUES (?, ?, ?, ?, ?, ?);""",
                    member.guild.id,  member.id, member.name, member.nick, member.discriminator, 
                    member.joined_at)
                    db.execute("INSERT OR IGNORE INTO member_exp (guild_id, member_id) VALUES (?, ?)", member.guild.id, member.id)
                    db.execute("INSERT OR IGNORE INTO member_points (guild_id, member_id) VALUES (?, ?)", member.guild.id, member.id)
        
        db.commit()
        print("Done.")
        

    async def on_connect(self):
        await self.update_db()
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
        elif isinstance(error, MissingRequiredArgument):
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
            # Now keeping all guild specific configurations in the database.

            # self.guild = self.get_guild(562178654151507981)
            # self.log_channel = self.get_channel(757112954599768064)
            # self.reaction_yoink = 759659429754437663
            self.Scheduler.start()
            await self.update_db()

            print("bot ready")

        else:
            print("bot reconnected")


    # moved most things to Cogs
    async def on_message(self, message):
        if message.author.bot:
            return

        await self.process_commands(message)
        ctx = await self.get_context(message)


    def get_log_channel(self, guild_id: int):
        channel_id = db.field("SELECT log_channel FROM guilds WHERE guild_id = ?;", guild_id)
        return self.get_channel(channel_id)

    def get_welcome_channel(self, guild_id: int):
        channel_id = db.field("SELECT welcome_channel FROM guilds WHERE guild_id = ?;", guild_id)
        return self.get_channel(channel_id)

    def get_guild_lvl_channel(self, guild_id: int):
        channel_id = db.field("SELECT lvl_channel FROM guilds WHERE guild_id = ?;", guild_id)
        return self.get_channel(channel_id)

    def run(self):
        print("running setup...")
        self.setup()

        with open("./lib/token.0", "r", encoding="UTF-8") as t:
            self.token = t.read()

        super().run(self.token, reconnect=True)


if __name__ == "__main__":
    WeiboluBot = WeiboluBot()
    WeiboluBot.run()

