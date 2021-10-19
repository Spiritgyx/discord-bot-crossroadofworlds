import sys

import discord.ext.commands
from discord.ext import commands, tasks
from discord import Permissions
import bot.mybot
from bot.mylogger import MyLogger
from typing import Sequence, Tuple, List


class Reactions(commands.Cog):
    def __init__(self, client: bot.mybot.Bot):
        self.client = client
        self.logger = MyLogger('React', 'reactions.log', levels=(client.level, 20))

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        self.logger.debug(f"Role add "
                          f"{payload.member}; {payload.event_type}; {payload.user_id}")
        member: discord.Member = payload.member
        if member.id == 895029252519526451:
            return None
        gid = payload.guild_id
        mid = payload.message_id
        sql_reactions = self.client.sql.get_react_msg(gid, mid)
        if len(sql_reactions) == 0:
            return
        emoji: discord.Emoji
        emoji = payload.emoji
        if emoji.id is None:
            emoji: str = emoji.name
        else:
            _animated = 'a' if emoji.animated else ''
            emoji: str = f'<{_animated}:{emoji.name}:{emoji.id}>'
        guild: discord.Guild
        self.logger.debug(f"{member.name}; [{emoji}]")
        for reaction in sql_reactions:
            # self.logger.debug(f"{mid == reaction[0]} and {gid == reaction[1]}"
            #                   f" and {emoji == reaction[3]}")
            # self.logger.debug(f"{reaction[0]} {reaction[1]} [{reaction[3]}]"
            #                   f"{reaction[4]} {reaction[5]} {reaction}")
            # self.logger.debug(f"{(mid, gid, emoji)}")
            if mid == reaction[0] and gid == reaction[1] and emoji == reaction[3]:
                if reaction[4] == 'add_role':
                    guild = self.client.get_guild(gid)
                    role = guild.get_role(int(reaction[5]))
                    # member.get
                    await member.add_roles(role, reason=f'Reaction to {mid} [{emoji}]')
                    self.logger.debug(f"Added role {role.name} to {member.name}")
                    break
        pass

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        self.logger.debug(f"Role remove "
                          # f"{payload}\n"
                          f"{payload.member}; {payload.event_type}; {payload.user_id}")
        member: discord.Member = self.client.get_guild(payload.guild_id).get_member(payload.user_id)
        if member.id == 895029252519526451:
            return None
        gid = payload.guild_id
        mid = payload.message_id
        sql_reactions = self.client.sql.get_react_msg(gid, mid)
        if len(sql_reactions) == 0:
            return
        emoji: discord.Emoji
        emoji = payload.emoji
        if emoji.id is None:
            emoji: str = emoji.name
        else:
            _animated = 'a' if emoji.animated else ''
            emoji: str = f'<{_animated}:{emoji.name}:{emoji.id}>'
        guild: discord.Guild
        self.logger.debug(f"{member.name}; [{emoji}]")
        for reaction in sql_reactions:
            # self.logger.debug(f"{mid == reaction[0]} and {gid == reaction[1]}"
            #                   f" and {emoji == reaction[3]}")
            # self.logger.debug(f"{reaction[0]} {reaction[1]} [{reaction[3]}]"
            #                   f"{reaction[4]} {reaction[5]} {reaction}")
            # self.logger.debug(f"{(mid, gid, emoji)}")
            if mid == reaction[0] and gid == reaction[1] and emoji == reaction[3]:
                if reaction[4] == 'add_role':
                    guild = self.client.get_guild(gid)
                    role = guild.get_role(int(reaction[5]))
                    # member.get
                    await member.remove_roles(role, reason=f'Reaction to {mid} [{emoji}]')
                    self.logger.debug(f"Removed role {role.name} to {member.name}")
                    break
        pass

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reaction(self, ctx: commands.Context, message: commands.MessageConverter,
                       emoji: str, cmd: str, argument: str):
        message: discord.Message
        if cmd == 'add_role':
            try:
                role = ''
                if not (argument.startswith('<@&') and argument.endswith('>')):
                    role_id = int(argument)
                    role = ctx.guild.get_role(role_id)
                    # discord.Guild.get_role()
                else:
                    role_id = int(argument[3:-1])
                    role = ctx.guild.get_role(role_id)
                    # role = argument

                if emoji.startswith('<'):
                    # check in DB?

                    pass
                guild_id = ctx.guild.id
                if guild_id != message.guild.id:
                    return await ctx.send(f"Error guild ID of message")
                self.logger.debug((
                    f"Add reaction: CID:{message.channel.id}-"
                    f"MID:{message.id}-GID:{message.guild.id};"
                    f" {emoji}; {cmd}; {role.id}")
                )
                self.client.sql.add_react(
                    message.id, message.guild.id, message.channel.id,
                    emoji, 'add_role', str(role.id)
                )
                await message.add_reaction(emoji)
            except:
                self.logger.error(sys.exc_info())
        pass

'''
on_raw_reaction_clear_emoji
on_raw_reaction_clear
on_raw_reaction_remove
on_raw_reaction_add
'''


def setup(client: bot.mybot.Bot):
    client.add_cog(Reactions(client))
