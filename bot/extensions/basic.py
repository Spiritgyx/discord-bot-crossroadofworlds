import discord.ext.commands
from discord.ext import commands, tasks
from discord import Permissions
import bot.bot
from bot.mylogger import MyLogger


class Basic(commands.Cog):
    def __init__(self, client: bot.bot.Bot):
        self.client = client
        self.logger = MyLogger('Loader', 'loader.log', levels=(client.level, 20))

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info('Bot is ready!')



def setup(client: bot.bot.Bot):
    client.add_cog(Basic(client))
