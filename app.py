import logging
import os

import api.config
from api import commands 
    
commands.bot.run(os.getenv('BOT_TOKEN', api.config.CONFIG['BOT']['TOKEN']))
