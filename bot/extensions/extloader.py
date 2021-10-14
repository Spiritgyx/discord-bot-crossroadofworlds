import discord.ext.commands
from discord.ext import commands, tasks
from discord import Permissions
import bot.mybot
from bot.mylogger import MyLogger


def check_ext(ext: str):
    """
    Function check valid extensions **path** or **name**

    Parameters
    ------------
    ext: :class:`str`
        Extension path.
        Example: [bot.extension.EXTNAME]
    """
    if not ext.startswith('bot.extensions.'):
        raise Exception("Invalid extension path.")
    if ext.endswith(('.basic', '.extloader')):
        raise Exception("Invalid core extensions.")
    if ext.find('..') != -1:
        raise Exception("Invalid extension path.")
    return True


class Loader(commands.Cog):
    def __init__(self, client: bot.mybot.Bot):
        self.client = client
        self.logger = MyLogger('Loader', 'loader.log', levels=(client.level, 20))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def load(self, ctx: commands.Context, ext: str):
        """
        Function to load extension **path**

        Parameters
        ------------
        ctx: :class:`discord.ext.commands.Context`
            Context argument.
        ext: :class:`str`
            Extension path.
            Example: [bot.extension.EXTNAME]
        """
        try:
            check_ext(ext)
            self.client.load_extension(ext)
        except Exception as e:
            self.logger.error(f'Extension "{ext}" load failed. {e}')
        else:
            self.logger.info(f'Extension "{ext}" loaded.')
            await ctx.send(f'Extension "{ext}" loaded.')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unload(self, ctx: commands.Context, ext: str):
        """
        Function to unload extension **path**

        Parameters
        ------------
        ctx: :class:`discord.ext.commands.Context`
            Context argument.
        ext: :class:`str`
            Extension path.
            Example: [bot.extension.EXTNAME]
        """
        try:
            check_ext(ext)
            self.client.unload_extension(ext)
        except Exception as e:
            self.logger.error(f'Extension "{ext}" unload failed. {e}')
        else:
            self.logger.info(f'Extension "{ext}" unloaded.')
            await ctx.send(f'Extension "{ext}" unloaded.')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reload(self, ctx: commands.Context, ext: str):
        """
        Function to reload extension **path**

        Parameters
        ------------
        ctx: :class:`discord.ext.commands.Context`
            Context argument.
        ext: :class:`str`
            Extension path.
            Example: [bot.extension.EXTNAME]
        """
        try:
            check_ext(ext)

            self.client.unload_extension(ext)
            self.client.load_extension(ext)
        except Exception as e:
            self.logger.error(f'Extension "{ext}" reload failed. {e}')
        else:
            self.logger.info(f'Extension "{ext}" reloaded.')
            await ctx.send(f'Extension "{ext}" reloaded.')


def setup(client: bot.mybot.Bot):
    client.add_cog(Loader(client))
