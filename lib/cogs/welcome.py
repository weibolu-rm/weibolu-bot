from discord.ext.commands import Cog, command
from ..db import db

WELCOME_CHANNEL = 562190083374055445

class Welcome(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_member_join(self, member):
        #TODO: set specific messages and channels in DB
        db.execute("INSERT INTO exp (UserID) VALUES (?)", member.id)
        await self.bot.get_channel(WELCOME_CHANNEL).send(f"Welcome {member.mention} to **{member.guild.name}**.")
        await member.add_roles(member.guild.get_role(756043010004746290))

    @Cog.listener()
    async def on_member_remove(self, member):
        db.execute("DELETE FROM exp WHERE UserID = ?", member.id)   
        await self.bot.get_channel(WELCOME_CHANNEL).send(f"{member.display_name} has left **{member.guild.name}**.. <:peepoSad:743248118124118056>")

def setup(bot):
    bot.add_cog(Welcome(bot))