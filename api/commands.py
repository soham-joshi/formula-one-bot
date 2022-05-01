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

@bot.event
async def on_command(ctx):
    channel = ctx.message.channel
    user = ctx.message.author
    print(f'Command: {ctx.prefix}{ctx.command} in {channel} by {user}')

# ===================
# Main command group
# ==================


@bot.command(aliases=['calendar', 'schedule'])
async def races(ctx, *args):
    """Display the full race schedule for the current season."""
    result = await api_calls.get_race_schedule()
    print(result)
    # Use simple table to not exceed content limit
    table = make_table(result['data'], fmt='simple')
    # target = await get_target(ctx, 'table')
    await ctx.send(f"**{result['season']} Formula 1 Race Calendar**\n")
    await ctx.send(f"```\n{table}\n```")