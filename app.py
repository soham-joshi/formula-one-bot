import logging
import os
import api.config
from api import commands
    
logging.basicConfig(level=logging.NOTSET,
                filename="Calclogs.log",filemode="a",
                format="%(asctime)s %(levelname)s-%(message)s",
                datefmt='%Y-%m-%d %H:%M:%S')

commands.bot.run(api.config.CONFIG['BOT']['TOKEN'])
