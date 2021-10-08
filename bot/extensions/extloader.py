import discord.ext.commands
from discord.ext import commands, tasks
from discord import Permissions
import bot.bot
from bot.mylogger import MyLogger


class Loader(commands.Cog):
    def __init__(self, client: bot.bot.Bot):
        self.client = client
        self.logger = MyLogger('Loader', 'loader.log', levels=(client.level, 20))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def load(self, ctx: commands.Context, ext: str):
        try:
            await self.client.load_extension(ext)
        except Exception as e:
            self.logger.error(f'Extension "{ext}" load failed.')
        else:
            self.logger.info(f'Extension "{ext}" loaded.')
            await ctx.send(f'Extension "{ext}" loaded.')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unload(self, ctx: commands.Context, ext: str):
        try:
            await self.client.unload_extension(ext)
        except Exception as e:
            self.logger.error(f'Extension "{ext}" unload failed.')
        else:
            self.logger.info(f'Extension "{ext}" unloaded.')
            await ctx.send(f'Extension "{ext}" unloaded.')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reload(self, ctx: commands.Context, ext: str):
        try:
            await self.client.unload_extension(ext)
            await self.client.load_extension(ext)
        except Exception as e:
            self.logger.error(f'Extension "{ext}" reload failed.')
        else:
            self.logger.info(f'Extension "{ext}" reloaded.')
            await ctx.send(f'Extension "{ext}" reloaded.')


def setup(client: bot.bot.Bot):
    client.add_cog(Loader(client))
