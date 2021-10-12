import discord.ext.commands
from discord.ext import commands, tasks
from discord import Permissions
import bot.mybot
from bot.mylogger import MyLogger
from typing import List, Iterator


class Testing(commands.Cog):
    def __init__(self, client: bot.mybot.Bot):
        self.client = client
        self.sql = self.client.sql
        self.logger = MyLogger('testing', 'testing.log', levels=(client.level, 20))

    @commands.command()
    async def get_current_members(self, ctx: commands.Context):
        sql_members = self.sql.get_members(ctx.guild.id)
        await ctx.send('\n'.join(map(str,sql_members)))



def setup(client: bot.mybot.Bot):
    client.add_cog(Testing(client))
