import logging
import os

import api.config
from api import commands 
from api import parser
import asyncio

output = asyncio.run(parser.get_soup(f"{parser.BASE_URL}/current"))
races = output.find_all("race")
print(races)

# commands.bot.run(os.getenv('BOT_TOKEN', api.config.CONFIG['BOT']['TOKEN']))
