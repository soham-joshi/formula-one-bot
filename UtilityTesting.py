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

    def test_filter_laps(self):
        laps = {'data': {
            1: [{'id': 'vettel', 'pos': 1, 'time': '1:10.202'},
                {'id': 'max', 'pos': 2, 'time': '1:20.205'},
                {'id': 'leclerc', 'pos': 3, 'time': '1:30.205'}],
            2: [{'id': 'vettel', 'pos': 2, 'time': '1:11.102'},
                {'id': 'max', 'pos': 1, 'time': '1:21.905'},
                {'id': 'leclerc', 'pos': 3, 'time': '1:31.105'}]
        }}

        filter_laps = utils.filter_laps_by_driver(laps, ['vettel'])
        # Only one driver given, so check only one timing
        self.assertEqual(len(filter_laps['data'][1]), 1, "Timing entries for 1 driver arg don't match result.")
        # Check driver matches
        self.assertEqual(filter_laps['data'][1][0]['id'], 'vettel', "Driver ID doesn't match provided arg.")

    def test_filter_laps_multiple_drivers(self):
        laps = {'data': {
            1: [{'id': 'vettel', 'pos': 1, 'time': '1:10.202'},
                {'id': 'max', 'pos': 2, 'time': '1:20.205'},
                {'id': 'leclerc', 'pos': 3, 'time': '1:30.205'}],
            2: [{'id': 'vettel', 'pos': 2, 'time': '1:11.102'},
                {'id': 'max', 'pos': 1, 'time': '1:21.905'},
                {'id': 'leclerc', 'pos': 3, 'time': '1:31.105'}]
        }}

        filter_laps = utils.filter_laps_by_driver(laps, ['max', 'vettel'])
        # Two drivers given, check timings for both
        self.assertEqual(len(filter_laps['data'][1]), 2, "Timing entries for 2 drivers args don't match result.")
        # Check the drivers
        self.assertEqual(filter_laps['data'][1][0]['id'], 'vettel')
        self.assertEqual(filter_laps['data'][1][1]['id'], 'max')

    def test_filter_times(self):
        times = sr.best_laps
        sorted_times = utils.rank_best_lap_times(times)
        [fast, slow, top, bottom] = [
            utils.filter_times(sorted_times, 'fastest'),
            utils.filter_times(sorted_times, 'slowest'),
            utils.filter_times(sorted_times, 'top'),
            utils.filter_times(sorted_times, 'bottom')
        ]
        # Check lengths
        self.assertEqual(len(fast), 1, "Fastest filter should return 1 item.")
        self.assertEqual(len(slow), 1, "Slowest filter should return 1 item.")
        self.assertEqual(len(top), 5, "Should return top 5.")
        self.assertEqual(len(bottom), 5, "Should return bottom 5.")
        # Compare data with mocked model data which has 7 laps
        self.assertEqual(fast[0]['Rank'], 1, "Fastest should return top rank.")
        self.assertEqual(slow[0]['Rank'], 7, "Slowest should return bottom rank.")


if __name__ == '__main__':
    unittest.main()