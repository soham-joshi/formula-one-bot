import re
import unittest
from unittest.mock import patch
from datetime import datetime

from api import utils
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.errors import MissingDataError, MessageTooLongError, DriverNotFoundError
from api.TestingHelpers.async_wrapper import async_wrapper

# Path for patch should be module where it is used, not where defined
fetch_path = 'api.api_calls.fetch'

from api.TestingHelpers.BaseTest import BaseTest
from api import parser

from api.TestingHelpers.responses.response import models
from api.TestingHelpers.responses.response import get_mock_response

class LiveAPITests(BaseTest):
    """Using real requests to check API status, validate response structure and error handling."""

    @async_wrapper
    async def test_get_past_race_results(self):
        past_res = await parser.get_race_results('12', '2017')
        self.check_data(past_res['data'])
        self.assertEqual(past_res['season'], '2017', "Requested season and result don't match.")
        self.assertEqual(past_res['round'], '12', "Requested round and result don't match.")

    @async_wrapper
    async def test_get_next_race_countdown(self):
        res = await parser.get_next_race()
        time = res['data']['Time']
        date = res['data']['Date']
        self.assertTrue(res['data'], "Results empty.")
        self.assertTrue(datetime.strptime(date, '%d %b %Y'), "Date not valid.")
        self.assertTrue(datetime.strptime(time, '%H:%M UTC'), "Time not valid.")

if __name__ == '__main__':
    unittest.main()