import os, sys, asyncio
import discord
from discord.ext import commands, tasks

from mylogger import MyLogger
from bot.utils.extensions import EXTS


# TODO: simple bot with commands
class Bot(commands.Bot):
    def __init__(self, token=None, level=20):
        self.level = level
        self.logger = MyLogger('bot', filename='bot.log', levels=(level, 20))
        if token is None:
            raise Exception("Enter token")
        super().__init__(token)

    def load_exts(self):
        #self.load_extension('extensions.extloader')
        extensions = set(EXTS)
        for ext in extensions:
            try:
                self.load_extension(ext)
            except Exception:
                self.logger.error('Extension "{ext}" load failed')
            else:
                self.logger.info('Extension "{ext}" loaded')
        self.logger.info('Bot is ready!')

