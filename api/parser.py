"""
Utilities to grab latest F1 results from Ergast API.
"""
import asyncio
from bs4 import BeautifulSoup
from datetime import datetime
from api.api_calls import fetch

from api import utils

BASE_URL = 'http://ergast.com/api/f1'


async def get_soup(url):
    """Request the URL and return response as BeautifulSoup object or None."""
    res = await fetch(url)
    if res is None:
        return None
    
    return BeautifulSoup(res, 'lxml')

async def get_race_schedule():
    url = f'{BASE_URL}/current'
    soup = await get_soup(url)
    if soup:
        races = soup.find_all('race')
        results = {
            'season': soup.racetable['season'],
            'data': []
        }
        for race in races:
            results['data'].append(
                {
                    'Round': int(race['round']),
                    'Circuit': race.circuit.circuitname.string,
                    'Date': utils.date_parser(race.date.string),
                    'Time': utils.time_parser(race.time.string),
                    'Country': race.location.country.string,
                }
            )
        return results
    
    return None

# if(__name__ == "__main__"):
#     output = asyncio.run(get_soup(f'{BASE_URL}/current'))
#     races = output.find_all('race')
#     print(races,type(races))