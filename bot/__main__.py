import argparse
import logging
import asyncio
import sys
import os
#import discord
#from discord.ext import commands, tasks
from mylogger import MyLogger

# Constants and global parameters
DEBUG = False


def main():
    """Main function of bot"""

    pass


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
    '''logging.basicConfig(
        # filename='debug.log',
        format='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%dT%H:%M:%S',
        level=level)'''

    # Create my logger
    '''
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    formats = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
                                datefmt='%Y-%m-%dT%H:%M:%S')
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formats)
    file_handler = logging.FileHandler('debug.log')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formats)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    '''
    logger = MyLogger(__name__, levels=(level, logging.INFO), filename=f"{__name__}.log")
    logger.debug('Debug message')
    logger.info('INFO message')
    logger.warning('WARNING message')
    logger.critical('CRITICAL message')
    try:
        raise Exception('TEST EXCEPTION')
    except Exception as e:
        logger.error(e, exc_info=sys.exc_info())

    pass