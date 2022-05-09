from discord import Colour, File
from discord.activity import Activity, ActivityType
from discord.embeds import Embed
from discord.ext import commands

from api import api_calls
from api.config import CONFIG
from api.utils import make_table
from api import parser
from api import utils
from operator import itemgetter

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