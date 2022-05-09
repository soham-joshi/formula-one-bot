import re
import unittest
from unittest.mock import patch
from datetime import datetime

from api import utils
# from api.errors import MissingDataError, MessageTooLongError, DriverNotFoundError
from api.tests.async_wrapper import async_wrapper
# from f1.tests.mock_response.response import models
# from f1.tests.mock_response.response import get_mock_response

from api.tests.BaseTest import BaseTest

best_laps = {
    'data': [
        {
            'Rank': 1,
            'Time': '1:30.202',
        },
        {
            'Rank': 2,
            'Time': '1:29.200',
        },
        {
            'Rank': 3,
            'Time': '1:29:190',
        },
        {
            'Rank': 4,
            'Time': '1:29.150',
        },
        {
            'Rank': 5,
            'Time': '1:28.100',
        },
        {
            'Rank': 6,
            'Time': '1:28.100',
        },
        {
            'Rank': 7,
            'Time': '1:28.100',
        }
    ]
}

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

    # def test_message_too_long_raises_exception(self):
    #     # discord limit 2000 chars
    #     msg = ['x'] * 3000
    #     with self.assertRaises(MessageTooLongError):
    #         utils.make_table(msg, headers='first_row')

    def test_is_year_in_future(self):
        year = '3333'
        self.assertTrue(utils.is_future(year))

    def test_is_year_in_past(self):
        year = '1111'
        self.assertFalse(utils.is_future(year))