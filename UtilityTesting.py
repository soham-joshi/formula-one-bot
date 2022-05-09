import re
import unittest
from unittest.mock import patch
from datetime import datetime

from api import utils
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.errors import MissingDataError, MessageTooLongError, DriverNotFoundError
from api.TestingHelpers.async_wrapper import async_wrapper

# from f1.tests.mock_response.response import models
# from f1.tests.mock_response.response import get_mock_response

from api.TestingHelpers.BaseTest import BaseTest

from api.TestingHelpers.responses import SampleResponses as sr


class UtilityTests(BaseTest):
    """Testing utility functions not tied to API data."""
    def test_utility_age(self):
        age_str = '2001-04-25'
        age = utils.age(age_str[:4])
        # arbirary check for extreme values, active F1 drivers avg 18-40
        self.assertTrue(int(age) > 0 and int(age) < 99, "Age not valid.")

    def test_driver_age_with_future_yob(self):
        yob = '3000'
        self.assertEqual(utils.age(yob), 0)

    def test_message_too_long_raises_exception(self):
        # discord limit 2000 chars
        msg = ['x'] * 3000
        with self.assertRaises(MessageTooLongError):
            utils.make_table(msg, headers='first_row')

    def test_is_year_in_future(self):
        year = '3333'
        # print(utils.is_future(year))
        self.assertTrue(utils.is_future(year))

    def test_is_year_in_past(self):
        year = '1111'
        # print(utils.is_future(year))
        self.assertFalse(utils.is_future(year))

    def test_lap_time_to_seconds(self):
        laps = ['1:30.202', '1:29.505', '0:00.000']
        # print([utils.lap_time_to_seconds(x) for x in laps])
        seconds = [utils.lap_time_to_seconds(x) for x in laps]
        self.assertEqual(seconds[0], 90.202)
        self.assertEqual(seconds[1], 89.505)
        self.assertEqual(seconds[2], 0.0)

    def test_lap_time_rankings(self):
        times = sr.best_laps
        sorted_times = utils.rank_best_lap_times(times)
        self.assertTrue(sorted_times[0]['Rank'] == 1)
        prev_rank = 0
        self.assertTrue(t['Rank'] > prev_rank for t in sorted_times)

if __name__ == '__main__':
    unittest.main()