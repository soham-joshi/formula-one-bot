"""
Perform asyncronous web requests.
"""
from urllib import response
import aiohttp
import logging
import asyncio
import requests

SESSION_TIMEOUT = 120

logger = logging.getLogger(__name__)


def is_xml(res): 
    return 'application/xml' in res.content_type


async def send_request(session, url):
    """Attempt to request the URL. Returns content of the Response if successful or None."""
    # open connection context, all response handling must be within
    async with session.get(url) as res:
        if is_xml(res):
            content = await res.read()
        return content


async def fetch(url):
    """Request the url and await response. Returns response content or None."""
    tmout = aiohttp.ClientTimeout(total=SESSION_TIMEOUT)
    async with aiohttp.ClientSession(timeout=tmout) as session:
        res = await send_request(session, url)
        return res


async def test_func():
    response = await fetch('http://ergast.com/api/f1/current')
    print(response)
    return response
