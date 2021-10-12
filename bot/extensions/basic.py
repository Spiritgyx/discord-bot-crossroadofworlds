import discord.ext.commands
from discord.ext import commands, tasks
from discord import Permissions
import bot.mybot
from bot.mylogger import MyLogger
from typing import List, Iterator


class Basic(commands.Cog):
    def __init__(self, client: bot.mybot.Bot):
        self.client = client
        self.sql = self.client.sql
        self.logger = MyLogger('bot', 'bot.log', levels=(client.level, 20))

    @commands.Cog.listener()
    async def on_ready(self):
        curr_guilds = self.client.guilds
        sql_guilds = self.sql.get_guilds()
        if len(sql_guilds) > 0:
            sql_guilds = list(map(lambda x: x[0], sql_guilds))
        guilds_add = []
        # sql_members = []
        for guild in curr_guilds:
            if guild.id not in sql_guilds:
                guilds_add.append((guild.id, guild.name))
                self.logger.info(f"Guild [{guild.id}] not exists in DB. Appended.")
            # else:
            #     sql_members.extend()
        self.sql.add_guilds(guilds_add)

        members_add = []  # (guild_id, member_id, member_tag, member_nickname)
        # curr_members: Iterator[discord.Member] = self.client.get_all_members()
        guild: discord.Guild
        member: discord.Member
        for guild in self.client.guilds:
            sql_members = self.sql.get_members(guild.id)
            if len(sql_members) > 0:
                sql_members = list(map(lambda x: x[2], sql_members))
            for member in guild.members:
                if member.id not in sql_members:
                    members_add.append(
                        (member.guild.id, member.id, member.name+'#'+member.discriminator, member.display_name)
                    )
        self.sql.add_members(members_add)
        self.logger.info('Bot is ready!')

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        sql_guilds = self.sql.get_guilds()
        if len(sql_guilds) > 0:
            sql_guilds = list(map(lambda x: x[0], sql_guilds))
        if guild.id not in sql_guilds:
            task = (guild.id, guild.name)
            self.sql.add_guilds([task])

        members_add = []  # (guild_id, member_id, member_tag, member_nickname)
        # curr_members: Iterator[discord.Member] = self.client.get_all_members()
        member: discord.Member
        sql_members = self.sql.get_members(guild.id)
        if len(sql_members) > 0:
            sql_members = list(map(lambda x: x[2], sql_members))
        for member in guild.members:
            if member.id not in sql_members:
                members_add.append((member.guild.id, member.id, member.name+'#'+member.discriminator, member.display_name))
        self.sql.add_members(members_add)
        self.logger.info(f'Bot joined into new guild. ID:{guild.id}; Name:{guild.name}')

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        sql_members = self.sql.get_members(member.guild.id)
        if len(sql_members) > 0:
            sql_members = list(map(lambda x: x[2], sql_members))
        if member.id not in sql_members:
            self.sql.add_members([(member.guild.id, member.id, member.name+'#'+member.discriminator, member.display_name)])


def setup(client: bot.mybot.Bot):
    client.add_cog(Basic(client))
