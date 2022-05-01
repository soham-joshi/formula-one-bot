"""
Utilities to grab latest F1 results from Ergast API.
"""
import asyncio
from bs4 import BeautifulSoup
from datetime import datetime
from api.api_calls import fetch

# from api import utils

BASE_URL = 'http://ergast.com/api/f1'


async def get_soup(url):
    """Request the URL and return response as BeautifulSoup object or None."""
    res = await fetch(url)
    if res is None:
        return None
    
    return BeautifulSoup(res, 'lxml')

if(__name__ == "__main__"):
    output = asyncio.run(get_soup(f'{BASE_URL}/current'))
    races = output.find_all('race')
    print(races,type(races))