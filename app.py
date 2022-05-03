import logging
import os
import api.config
from api import commands
    
commands.bot.run(api.config.CONFIG['BOT']['TOKEN'])
