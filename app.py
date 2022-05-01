import logging
import os

import api.config
from api import commands 
from api import parser
from api import utils
import asyncio

# result = asyncio.run(parser.get_race_schedule())
# print(utils.make_table(result["data"],fmt="fancy_grid"))

# output = asyncio.run(parser.get_soup(f"{parser.BASE_URL}/current"))
# races = output.find_all("race")
# print(races)

commands.bot.run(os.getenv('BOT_TOKEN', api.config.CONFIG['BOT']['TOKEN']))
