import os, sys, asyncio, json
import discord
from discord.ext import commands, tasks

import bot
from bot.mylogger import MyLogger
from bot.utils.exts import EXTS
from bot.sql import Sql


def get_prefix(cl, msg: commands.Context):
    with open(os.getcwd()+'/jsons/prefixes.json') as f:
        prefixes = json.load(f)
    return prefixes.get(str(msg.guild.id), '##')


# TODO:
# TODO: documentation
class Bot(commands.Bot):
    def __init__(self, *args, token=None, level=20, **kwargs):
        self.level = level
        self.logger = MyLogger('bot', filename='bot.log', levels=(level, 20))
        self.sql = Sql(level=level)
        # if token is None:
        #    raise Exception("Enter token")
        super().__init__(*args, **kwargs)

    def load_exts(self):
        #self.load_extension('extensions.extloader')
        exts = set(EXTS)
        for ext in exts:
            try:
                self.load_extension(ext)
            except Exception:
                self.logger.error(f'Extension "{ext}" load failed')
            else:
                self.logger.info(f'Extension "{ext}" loaded')
        self.logger.info('Bot starting...')

