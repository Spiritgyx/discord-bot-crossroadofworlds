import argparse
import logging
import asyncio
import sys
import os
import bot
from bot.mybot import Bot, get_prefix
from bot.mylogger import MyLogger

# Constants and global parameters
DEBUG = False


def get_token() -> str:
    """Return token from <.env> file.
    If the file does not exist, then the token is entered manually."""
    if os.path.exists('.env'):
        try:
            from dotenv import load_dotenv
            load_dotenv()
            token = os.getenv('TOKEN')
            if not token:
                raise Exception("Token is empty")
            return token
        except:
            logger.warning('Token is empty')
            print(sys.exc_info())
    token = input("Enter bot token: ")
    with open('.env', 'w') as f:
        f.write(f"TOKEN='{token}'")
    return token


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Discord bot main script.')
    parser.add_argument('-d', '--debug', help='Debug mode.', action='store_true')
    args = parser.parse_args()
    DEBUG = args.debug
    if DEBUG:
        print('Debug mode ON.')
        level = logging.DEBUG
    else:
        level = logging.INFO

    # Create my logger
    logger = MyLogger(__name__, levels=(level, logging.INFO), filename=f"{__name__}.log")
    logger.debug('Start program')
    token = get_token()
    client = Bot(command_prefix=get_prefix, level=level)
    client.load_exts()
    client.run(token)
