from discord.ext.commands import Cog, command, has_permissions
from ..db import db 
from discord import Color, NotFound, HTTPException, version_info
from weibolu import create_embed
import requests
from typing import Optional

def get_guild_yoinker(guild_id: int):
    yoinker = db.field("SELECT yoinker_id FROM guilds WHERE guild_id = ?;", guild_id)
    return yoinker

class Emoji(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="yoink", aliases=["steal", "set_yoink", "set_steal"])
    @has_permissions(manage_guild = True)
    async def set_yoink(self, ctx, arg, message_id: Optional[int]):
        message_id = message_id or None
        if arg == "clear" or arg == "clr":
            db.execute("UPDATE guilds SET yoinker_id = ? WHERE guild_id = ?;", None, ctx.guild.id)
            db.commit()
            embed = create_embed("Yoinker Message Cleared", 
                                f"Yoinker message was cleared by {ctx.message.author}", color=Color.red())

            log_channel = self.bot.get_log_channel(ctx.guild.id)
            if log_channel is not None:
                await log_channel.send(embed=embed)
            await ctx.send(f"Successfully cleared yoinker.")
            return

        elif arg == "set":
            if message_id is None:
                await ctx.send("Please enter a valid message ID.")
                return

        else:
            print("returning")
            return

        message = await ctx.fetch_message(message_id)

        if message_id == get_guild_yoinker(ctx.guild.id):
            await ctx.send("Yoinker already set to that message.")

        # elif not re.match("\d", message_id):
        #     await ctx.send("Invalid message ID. Enter message ID for reaction emote yoinker.")
        else:
            db.execute("UPDATE guilds SET yoinker_id = ? WHERE guild_id = ?;", message_id, ctx.guild.id)
            db.commit()
            self.bot.reaction_yoink = message_id
            embed = create_embed("New Yoinker Message Set", 
                                f"Yoinker message set to message with id {message_id}. {message.jump_url} by {ctx.message.author}.", color=Color.dark_magenta())

            log_channel = self.bot.get_log_channel(ctx.guild.id)
            if log_channel is not None:
                await log_channel.send(embed=embed)
            await ctx.send(f"Successfully set yoinker to message with id {message_id}.")

    # not wroking for some reason
    @set_yoink.error
    async def set_yoink_error(self, ctx, error):
        print("test")
        if isinstance(error, NotFound): 
            await ctx.send("Wrong argument. Message id could not be found.")

    @Cog.listener() 
    async def on_raw_reaction_add(self, payload): 
        guild = self.bot.get_guild(payload.guild_id)
        log_channel = self.bot.get_log_channel(payload.guild_id)
        if int(payload.message_id) == get_guild_yoinker(payload.guild_id):

            # need permission to manage server
            if not payload.member.guild_permissions.manage_guild:
                return
                
            emoji = payload.emoji
            if emoji in guild.emojis:
                print("emoji already exists")
                return
    
            try:
                response = requests.get(emoji.url)
                await guild.create_custom_emoji(name=emoji.name, image=response.content)
            except HTTPException:
                if log_channel is not None:
                    await log_channel.send(f"Problem adding emoji {emoji.name}.")
                    return
    
            embed = create_embed(f"Emoji added to {guild.name}!", f"{emoji.name}", 
                                    image_url=emoji.url, color=Color.dark_teal())
    
            if log_channel is not None:
                await log_channel.send(embed=embed)

    
    # as of discord.py 1.5.1, I can't seem to get the info on the user removing reactions

    # @Cog.listener() 
    # async def on_raw_reaction_remove(self, payload): 
    #     print(version_info)
    #     print(payload)
    #     guild = self.bot.get_guild(payload.guild_id)
    #     log_channel = self.bot.get_log_channel(payload.guild_id)

    #     if int(payload.message_id) == get_guild_yoinker(payload.guild_id):
    #         print(user_id)
    #         member = await guild.fetch_member(payload.user_id)
    #         # need permission to manage server
    #         if not member.guild_permissions.manage_guild:
    #             return
                
    #         emoji = payload.emoji
    #         # we need to get the actual Emoji object
    #         for e in guild.emojis:
    #             if emoji == e:
    #                 embed = create_embed(f"Emoji removed from {guild.name}!", f"{emoji.name}", 
    #                                     image_url=emoji.url, color=Color.dark_magenta())
    #                 await e.delete()
    #                 await log_channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Emoji(bot))