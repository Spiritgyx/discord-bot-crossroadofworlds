import sys

import discord.ext.commands
from discord.ext import commands, tasks
from discord import Permissions
import bot.mybot
from bot.mylogger import MyLogger
from typing import List, Iterator
import os
import json



class Basic(commands.Cog):
    def __init__(self, client: bot.mybot.Bot):
        """Cog. Basic events and admin commands.
        :param client:
        """
        self.client = client
        self.sql = self.client.sql
        self.logger = MyLogger('bot', 'bot.log', levels=(client.level, 20))

    @commands.Cog.listener()
    async def on_ready(self):
        """Event of bot, whole bot has been starting.
        """
        # Get current guilds from discord.
        curr_guilds = self.client.guilds
        # Get current guilds in SQL DB.
        sql_guilds = self.sql.get_guilds()
        if len(sql_guilds) > 0:
            sql_guilds = list(map(lambda x: x[0], sql_guilds))
        # Check guilds in DB, if not then add to DB.
        guilds_add = []
        for guild in curr_guilds:
            if guild.id not in sql_guilds:
                guilds_add.append((guild.id, guild.name))
                self.logger.info(f"Guild [{guild.id}] not exists in DB. Appended.")
        self.sql.add_guilds(guilds_add)

        members_add = []  # (guild_id, member_id, member_tag, member_nickname)
        guild: discord.Guild
        member: discord.Member
        # Iterating all guild.
        for guild in self.client.guilds:
            # Get current members in SQL DB.
            sql_members = self.sql.get_members(guild.id)
            if len(sql_members) > 0:
                sql_members = list(map(lambda x: x[2], sql_members))
            self.logger.debug(f'Guild: {guild.id}; Count: {len(guild.members)};')
            # Check members in DB, if not then add to DB.
            fetch_members = await guild.fetch_members().flatten()
            self.logger.debug('Fetch members: ' + str(fetch_members))
            while len(fetch_members) != 0:
                for member in fetch_members:
                    self.logger.debug(f'Member: {str(member)}')
                    if member.id not in sql_members:
                        members_add.append(
                            (member.guild.id, member.id, member.name + '#' + member.discriminator, member.display_name)
                        )
                        sql_members.append(member.id)
                fetch_members = await guild.fetch_members(after=fetch_members[0]).flatten()
        self.sql.add_members(members_add)

        # Check emojis
        try:
            self.check_emojis()
        except:
            self.logger.error(sys.exc_info())
        self.logger.info('Bot is ready!')

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        """Event of guild, whole Bot has been join or rejoin to new guild.
        @param guild: discord.Guild
        """
        # Get current guilds in SQL DB.
        sql_guilds = self.sql.get_guilds()
        if len(sql_guilds) > 0:
            sql_guilds = list(map(lambda x: x[0], sql_guilds))
        # Check guild in DB, if not then add to DB.
        if guild.id not in sql_guilds:
            task = (guild.id, guild.name)
            self.sql.add_guilds([task])

        members_add = []  # (guild_id, member_id, member_tag, member_nickname)
        member: discord.Member
        # Get current members in SQL DB.
        sql_members = self.sql.get_members(guild.id)
        if len(sql_members) > 0:
            sql_members = list(map(lambda x: x[2], sql_members))
        # Check members in DB, if not then add to DB.
        fetch_members = await guild.fetch_members().flatten()
        while len(fetch_members) != 0:
            for member in fetch_members:
                if member.id not in sql_members:
                    members_add.append(
                        (member.guild.id, member.id, member.name + '#' + member.discriminator, member.display_name))
                    sql_members.append(member.id)
            fetch_members = await guild.fetch_members(after=fetch_members[0]).flatten()
        self.sql.add_members(members_add)
        self.logger.info(f'Bot joined into new guild. ID:{guild.id}; Name:{guild.name}')

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """Event of guild, whole new member has been join or rejoin to guild.
        @param member: discord.Member
        """
        # Get current members in SQL DB.
        sql_members = self.sql.get_members(member.guild.id)
        if len(sql_members) > 0:
            sql_members = list(map(lambda x: x[2], sql_members))
        # Check member in DB, if not then add to DB.
        if member.id not in sql_members:
            self.sql.add_members(
                [(member.guild.id, member.id, member.name + '#' + member.discriminator, member.display_name)])

    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild, before, after):
        try:
            self.check_emojis(guild.id)
        except:
            self.logger.error(sys.exc_info())
        pass

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def prefix_change(self, ctx: commands.Context, prefix: str = "##"):
        """Command for change prefix in current guild.
        @param ctx: commands.Context
        @param prefix: str
        """
        # Get current prefixes.
        with open(os.getcwd() + '/jsons/prefixes.json', 'r') as f:
            prefixes = json.load(f)
        # Set default prefixes, if guild not added.
        if str(ctx.guild.id) not in prefixes.keys():
            prefixes[str(ctx.guild.id)] = '##'
        # Set new prefix.
        prefixes[str(ctx.guild.id)] = prefix
        # Write edited prefixes.
        with open(os.getcwd() + '/jsons/prefixes.json', 'w') as f:
            data = json.dumps(prefixes, indent=4, ensure_ascii=True)
            f.write(data)
        # Send message of change to admin.
        await ctx.send(f"Префикс комманд изменён на '{prefix}'.")

    def check_emojis(self, guild_id: int = None):
        sql_emojis = self.sql.get_emojis(guild_id)
        emoji_all_id = list(map(lambda x: x[0], sql_emojis))
        add_emojis = []
        emoji: discord.Emoji
        for emoji in self.client.emojis:
            # emoji.id, emoji.guild_id, emoji.animated, emoji.name
            raw = (emoji.id, emoji.guild_id, emoji.name, int(emoji.animated))
            if emoji.id not in emoji_all_id:
                add_emojis.append(raw)
        self.sql.add_emojis(add_emojis)


def setup(client: bot.mybot.Bot):
    client.add_cog(Basic(client))
