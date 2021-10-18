import os, sys, asyncio, json
import discord
from discord.ext import commands, tasks
import bot
from bot.mylogger import MyLogger
from bot.utils.exts import EXTS
from bot.sql import Sql


def get_prefix(cl, msg: commands.Context):
    """Function return prefix for current message guild."""
    with open(os.getcwd()+'/jsons/prefixes.json', 'r') as f:
        prefixes = json.load(f)
    if str(msg.guild.id) not in prefixes.keys():
        prefixes[str(msg.guild.id)] = '##'
        with open(os.getcwd() + '/jsons/prefixes.json', 'w') as f:
            data = json.dumps(prefixes, indent=4, ensure_ascii=True)
            f.write(data)
    return prefixes.get(str(msg.guild.id), '##')


# TODO: reactions and roles
class Bot(commands.Bot):
    def __init__(self, *args, token=None, level=20, **kwargs):
        self.level = level
        self.logger = MyLogger('bot', filename='bot.log', levels=(level, 20))
        self.sql = Sql(level=level)
        super().__init__(*args, **kwargs)

    def load_exts(self):
        exts = set(EXTS)
        for ext in exts:
            try:
                self.load_extension(ext)
            except Exception:
                self.logger.error(f'Extension "{ext}" load failed')
            else:
                self.logger.info(f'Extension "{ext}" loaded')
        self.logger.info('Bot starting...')

