from discord.ext.commands import Cog, command
from ..db import db

class Welcome(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @Cog.listener()
    async def on_ready(self):
        self.welcome_channel = self.bot.get_channel(757103651000025180)

    @Cog.listener()
    async def on_member_join(self, member):
        #TODO: set specific messages and channels in DB
        db.execute("INSERT INTO member_exp (guild_id, member_id, username, nickname, discriminator) VALUES (?, ?, ?, ?, ?);", 
            member.guild,  member.id, member.name, member.nick, member.discriminator)
        await self.welcome_channel.send(f"Welcome {member.mention} to **{member.guild.name}**.")
        await member.add_roles(member.guild.get_role(756043010004746290))

    @Cog.listener()
    async def on_member_remove(self, member):
        db.execute("DELETE FROM members WHERE member_id = ? AND guild_id = ?;", member.id, member.guild)   
        await self.welcome_channel.send(f"{member.display_name} has left **{member.guild.name}**.. <:peepoSad:743248118124118056>")

    @Cog.listener()
    async def on_member_update(self, before, member):
        db.execute("UPDATE members SET username = ?, nickname = ?, discriminator = ? WHERE guild_id = ? AND member_id = ?;",
            member.name, member.nick, member.discriminator, member.guild.id, member.id)
        print(f"""Member updated:
Username: {member.name}
Nickname: {member.nick}
Discriminator: {member.discriminator}
""")

def setup(bot):
    bot.add_cog(Welcome(bot))