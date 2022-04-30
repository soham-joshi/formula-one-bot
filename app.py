import logging
import os

import api.config

from discord.ext import commands

bot = commands.Bot(
    command_prefix=f"{api.config.CONFIG['BOT']['PREFIX']}f1 ",
    help_command=commands.DefaultHelpCommand(dm_help=True),
    case_insensitive=True
)

@bot.event
async def on_ready():
    print('I have logged in as {0.user}'.format(bot))

    
bot.run(os.getenv('BOT_TOKEN', api.config.CONFIG['BOT']['TOKEN']))
