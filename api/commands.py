from discord import Colour, File
from discord.activity import Activity, ActivityType
from discord.embeds import Embed
from discord.ext import commands

from api import api_calls
from api.config import CONFIG
from api.utils import make_table
from api import parser
from api import utils
import asyncio
from api.utils import make_table, filter_times, rank_best_lap_times, rank_pitstops, filter_laps_by_driver
from operator import itemgetter
import logging

logging.getLogger("discord").setLevel(logging.WARNING)

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
    print(f'{ctx.prefix}{ctx.command} in {channel} by {user} on shard {shard_id}')
    
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
    result = await parser.get_race_schedule_calendar()
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

@bot.command(aliases=['grid'])
async def season_grid(ctx, season='current'):
    """Display all the drivers and teams participating in the current season or `season`.
    Usage:
    ------
        !f1 grid            All drivers and teams in the current season as of the last race.
        !f1 grid [season]   All drivers and teams at the end of [season].
    """
    await check_season(ctx, season)
    result = await parser.get_all_drivers_and_teams_for_season(season)
    # Use simple table to not exceed content limit
    table = make_table(sorted(result['data'], key=itemgetter('Team')), fmt='simple')
    await ctx.send(
        f"**Formula 1 {result['season']} Grid**\n" +
        f"Round: {result['round']}\n"
    )
    await ctx.send(f"```\n{table}\n```")


@bot.command(aliases=['source', 'git'])
async def github(ctx, *args):
    """Display a link to the GitHub repository."""
    await ctx.send("https://github.com/soham-joshi/formula-one-bot")


@bot.command(aliases=['finish'])
async def results(ctx, season='current', rnd='last'):
    """Results for race `round`. Default most recent.
    Displays an embed with details about the race event and wikipedia link. Followed by table
    of results. Data includes finishing position, fastest lap, finish status, pit stops per driver.
    Usage:
    ------
        !f1 results                     Results for last race.
        !f1 results [<season> <round>]  Results for [round] in [season].
    """
    await check_season(ctx, season)
    result = await parser.get_race_results(rnd, season)
    table = make_table(result['data'], fmt='simple')
    await ctx.send(f"**Race Results - {result['race']} ({result['season']})**")
    await ctx.send(f"```\n{table}\n```")

@bot.command(aliases=['quali'])
async def qualifying(ctx, season='current', rnd='last'):
    """Qualifying results for `round`. Defaults to latest.
    Includes best Q1, Q2 and Q3 times per driver.
    Usage:
    ------
        !f1 quali                    Latest results.
        !f1 quali [<season> <round>] Results for [round] in [season].
    """
    await check_season(ctx, season)
    result = await parser.get_qualifying_results(rnd, season)
    table = make_table(result['data'])
    await ctx.send(f"**Qualifying Results - {result['race']} ({result['season']})**")
    await ctx.send(f"```\n{table}\n```")

@bot.command(aliases=['driver'])
async def career(ctx, driver_id):
    """Career stats for the `driver_id`.
    Includes total poles, wins, points, seasons, teams, fastest laps, and DNFs.
    Parameters:
    -----------
    `driver_id`
        Supported Ergast API ID, e.g. 'alonso', 'michael_schumacher', 'vettel', 'di_resta'.
    Usage:
    --------
        !f1 career vettel | VET | 55   Get career stats for Sebastian Vettel.
    """
    await ctx.send("*Gathering driver data, this may take a few moments...*")
    driver = parser.get_driver_info(driver_id)
    result = await parser.get_driver_career(driver)
    thumb_url_task = asyncio.create_task(parser.get_wiki_thumbnail(driver['url']))
    season_list = result['data']['Seasons']['years']
    champs_list = result['data']['Championships']['years']
    embed = Embed(
        title=f"**{result['driver']['firstname']} {result['driver']['surname']} Career**",
        url=result['driver']['url'],
        colour=Colour.teal(),
    )
    embed.set_thumbnail(url=await thumb_url_task)
    embed.add_field(name='Number', value=result['driver']['number'], inline=True)
    embed.add_field(name='Nationality', value=result['driver']['nationality'], inline=True)
    embed.add_field(name='Age', value=result['driver']['age'], inline=True)
    embed.add_field(
        name='Seasons',
        # Total and start to latest season
        value=f"{result['data']['Seasons']['total']} ({season_list[0]}-{season_list[len(season_list)-1]})",
        inline=True
    )
    embed.add_field(name='Wins', value=result['data']['Wins'], inline=True)
    embed.add_field(name='Poles', value=result['data']['Poles'], inline=True)
    embed.add_field(
        name='Championships',
        # Total and list of seasons
        value=(
            f"{result['data']['Championships']['total']} " + "\n"
            + ", ".join(y for y in champs_list if champs_list)
        ),
        inline=False
    )
    embed.add_field(
        name='Teams',
        # Total and list of teams
        value=(
            f"{result['data']['Teams']['total']} " + "\n"
            + ", ".join(t for t in result['data']['Teams']['names'])
        ),
        inline=False
    )
    await ctx.send(embed=embed)

@bot.command(aliases=['bestlap'])
async def best(ctx, filter=None, season='current', rnd='last'):
    """Display the best lap times and delta for each driver in `round`.
    If no `round` specified returns results for the most recent race.
    Usage:
    ---------------
        !f1 best                             Return all best laps for the latest race.
        !f1 best [filter] [<season> <round>] Return best laps sorted by [filter].
        Optional filter:
        ----------------
        `all`     -  Do not apply a filter.
        `fastest` -  Only show the fastest lap of the race.
        `slowest` -  Only show the slowest lap of the race.
        `top`     -  Top 5 fastest drivers.
        `bottom`  -  Bottom 5 slowest drivers.
    """
    if filter not in ['all', 'top', 'fastest', 'slowest', 'bottom', None]:
        await ctx.send("Invalid filter given.")
        raise commands.BadArgument(message="Invalid filter given.")
    await check_season(ctx, season)
    results = await parser.get_best_laps(rnd, season)
    sorted_times = rank_best_lap_times(results)
    filtered = filter_times(sorted_times, filter)
    table = make_table(filtered)
    await ctx.send(
        f"**Fastest laps ranked {filter}**\n" +
        f"{results['season']} {results['race']}"
    )
    await ctx.send(f"```\n{table}\n```")

@bot.command(aliases=['pits', 'pitstops'])
async def stops(ctx, filter, season='current', rnd='last'):
    """Display pitstops for each driver in the race, optionally sorted with filter.
    If no `round` specified returns results for the most recent race. Data not available
    before 2012.
    Usage:
    ---------------
        !f1 stops <filter> [season] [round]     Return pitstops sorted by [filter].
        !f1 stops <driver_id> [season] [round]  Return pitstops for the driver.
        Filter:
        ----------------
        `<driver_id>`  -  Get the stops for the driver.
        `fastest` -  Only show the fastest pitstop the race.
        `slowest` -  Only show the slowest pitstop the race.
        `top`     -  Top 5 fastest pitstops.
        `bottom`  -  Bottom 5 slowest pitstops.
    """

    # Pit data only available from 2012 so catch seasons before
    if not season == 'current':
        if int(season) < 2012:
            await ctx.send("Pitstop data not available before 2012.")
            raise commands.BadArgument(message="Tried to get pitstops before 2012.")
    await check_season(ctx, season)

    # Get stops
    res = await parser.get_pitstops(rnd, season)

    # The filter is for stop duration
    if filter in ['top', 'bottom', 'fastest', 'slowest']:
        sorted_times = rank_pitstops(res)
        filtered = filter_times(sorted_times, filter)
    # The filter is for all stops by a driver
    else:
        try:
            driver = parser.get_driver_info(filter)
            filtered = [s for s in res['data'] if s['Driver'] == driver['code']]
        except:
            await ctx.send("Invalid filter or driver provided.")

    table = make_table(filtered)

    await ctx.send(
        f"**Pit stops ranked {filter}**\n" +
        f"{res['season']} {res['race']}"
    )
    await ctx.send(f"```\n{table}\n```")
