from discord import Colour, File
from discord.activity import Activity, ActivityType
from discord.embeds import Embed
from discord.ext import commands

from api import api_calls
from api.config import CONFIG
from api.utils import make_table
from api import parser
from api import utils

# Prefix includes the config symbol and the 'f1' name with hard-coded space
bot = commands.AutoShardedBot(
    shard_count=3,
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
    shard_id = ctx.guild.shard_id
    shard = bot.get_shard(shard_id)
    user = ctx.message.author
    print(f'Command: {ctx.prefix}{ctx.command} in {channel} by {user} on shard {shard_id}')
    # logger.info()


@bot.event
async def on_command_completion(ctx):
    # await ctx.message.add_reaction(u'🏁')
    print("Complete command")


# ===================
# Main command group
# ==================


@bot.command(aliases=['calendar', 'schedule'])
async def races(ctx, *args):
    """Display the full race schedule for the current season."""
    result = await api_calls.get_race_schedule()
    # print(result)
    # Use simple table to not exceed content limit
    table = make_table(result['data'], fmt='simple')
    # target = await get_target(ctx, 'table')
    await ctx.send(f"**{result['season']} Formula 1 Race Calendar**\n")
    await ctx.send(f"```\n{table}\n```")

async def check_season(ctx, season):
    """Raise error if the given season is in the future."""
    if utils.is_future(season):
        await ctx.send(f"Can't predict future :thinking:")
        raise commands.BadArgument('Given season is in the future.')

@bot.command(aliases=['teams', 'constructors'])
async def season_standings_teams(ctx, season='current'):
    """Display Constructor Championship standings as of the last race or `season`.
    Usage:
    ------
        !f1 wcc            Current WCC standings as of the last race.
        !f1 wcc [season]   WCC standings from [season].
    """
    await check_season(ctx, season)
    result = await parser.get_team_standings(season)
    table = make_table(result['data'])
    
    await ctx.send(
        f"**World Constructor Championship**\n" +
        f"Season: {result['season']} Round: {result['round']}\n"
    )
    await ctx.send(f"```\n{table}\n```")

@bot.command(aliases=['drivers', 'championship'])
async def world_drivers_championship(ctx, season='current'):
    """Display the Driver Championship standings as of the last race or `season`.
    Usage:
    ------
        !f1 wdc [season]    WDC standings from [season].
    """
    await check_season(ctx, season)
    result = await parser.get_season_driver_standings(season)
    table = make_table(result['data'], fmt='simple')
    await ctx.send(
        f"**World Driver Championship**\n" +
        f"Season: {result['season']} Round: {result['round']}\n"
    )
    await ctx.send(f"```\n{table}\n```")

