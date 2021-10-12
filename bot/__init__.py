from typing import TYPE_CHECKING
import os
#from bot import mylogger, sql
#from bot.mybot import Bot


if not os.path.isdir(os.getcwd()+'/jsons'):
    os.mkdir(os.getcwd()+'/jsons')
if not os.path.exists(os.getcwd()+'/jsons/prefixes.json'):
    with open(os.getcwd()+'/jsons/prefixes.json', 'w') as f:
        f.write('{}')
