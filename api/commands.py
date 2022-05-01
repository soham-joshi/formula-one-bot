from discord import Colour, File
from discord.activity import Activity, ActivityType
from discord.embeds import Embed
from discord.ext import commands

from api import api_calls
from api.config import CONFIG
from api.utils import make_table



# Prefix includes the config symbol and the 'f1' name with hard-coded space
bot = commands.Bot(
    command_prefix=f"{CONFIG['BOT']['PREFIX']}f1 ",
    help_command=commands.DefaultHelpCommand(dm_help=True),
    case_insensitive=True
)

@bot.event
async def on_ready():
    print('I have logged in as {0.user}'.format(bot))

