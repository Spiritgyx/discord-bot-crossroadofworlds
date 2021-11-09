import sys

import discord.ext.commands
from discord.ext import commands, tasks
from discord import Permissions
import bot.mybot
from bot.mylogger import MyLogger
from typing import Sequence, Tuple, List


class VoiceCreate(commands.Cog):
    def __init__(self, client: bot.mybot.Bot):
        self.client = client
        self.logger = MyLogger('VoiceCreate', 'voice.log', levels=(client.level, 20))

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member,
                                    before: discord.VoiceState,
                                    after: discord.VoiceState):
        """
        Event that checks the entry and exit of the user to the voice channel.

        Parameters
        -----------
        member: :class:`discord.Member`
            Member
        before: :class:`discord.VoiceState`
            State before update
        after: :class:`discord.VoiceState`
            State after update
        """
        # ➕➖
        b_channel: discord.VoiceChannel = before.channel
        a_channel: discord.VoiceChannel = after.channel
        if b_channel is not None and b_channel.name.startswith('➖'):
            # Check the custom channel for empty
            b_members = b_channel.members
            # Delete empty channel
            if len(b_members) == 0:
                await b_channel.delete()
            pass
        if a_channel is not None and a_channel.name.startswith('➕'):
            # Create new channel

            # Copy category and permissions from parent channel
            category = a_channel.category
            overwrites = a_channel.overwrites

            channel_name = '➖ ' + member.display_name
            guild: discord.Guild = a_channel.guild
            # Create channel & get object
            new_channel = await guild.create_voice_channel(name=channel_name,
                                                           category=category,
                                                           overwrites=overwrites)
            # Move member to new channel
            await member.move_to(channel=new_channel)
            pass
        pass


def setup(client: bot.mybot.Bot):
    client.add_cog(VoiceCreate(client))