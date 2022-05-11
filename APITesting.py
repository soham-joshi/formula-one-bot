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


class MockAPITests(BaseTest):
    """Using mock data models to test response parsing and data output."""

    def test_get_driver_info(self):
        res_with_id = parser.get_driver_info('hamilton')
        res_with_no = parser.get_driver_info('44')
        res_with_code = parser.get_driver_info('HAM')
        self.assertEqual(res_with_id['id'], 'hamilton')
        self.assertEqual(res_with_no['id'], 'hamilton')
        self.assertEqual(res_with_no['number'], '44')
        self.assertEqual(res_with_code['id'], 'hamilton')
        self.assertEqual(res_with_code['code'], 'HAM')

    def test_get_driver_info_code_or_number_conversion(self):
        res = parser.get_driver_info('abate')
        self.assertEqual(res['id'], 'abate')
        self.assertTrue(res['number'] is None)
        self.assertTrue(res['code'] is None)


    @patch(fetch_path)
    @async_wrapper
    async def test_get_team_standings(self, mock_fetch):
        mock_fetch.return_value = await  get_mock_response('constructor_standings')
        res = await parser.get_team_standings('current')
        self.check_data(res['data'])

    @patch(fetch_path)
    @async_wrapper
    async def test_get_driver_standings(self, mock_fetch):
        mock_fetch.return_value = await get_mock_response('driver_standings')
        res = await parser.get_driver_standings('current')
        self.check_data(res['data'])

    @patch(fetch_path)
    @async_wrapper
    async def test_get_qualifying_results(self, mock_fetch):
        mock_fetch.return_value = await get_mock_response('qualifying_results')
        res = await parser.get_qualifying_results('last', 'current')
        self.check_data(res['data'])


    @patch(fetch_path)
    @async_wrapper
    async def test_get_race_results(self, mock_fetch):
        mock_fetch.return_value = await  get_mock_response('race_results')
        res = await parser.get_race_results('last', 'current')
        self.check_data(res['data'])
        self.check_data(res['timings'])

    

    @patch(fetch_path)
    @async_wrapper
    async def test_get_all_laps(self, mock_fetch):
        mock_fetch.return_value = await  get_mock_response('all_laps')
        res = await parser.get_all_laps(1, 2019)
        self.assertNotIn(None, res['data'][1])


    @patch(fetch_path)
    @async_wrapper
    async def test_get_pitstops(self, mock_fetch):
        mock_fetch.side_effect = [await get_mock_response('pitstops'), await get_mock_response('race_results')]
        res = await parser.get_pitstops('last', 'current')
        self.check_data(res['data'])


    @patch(fetch_path)
    @async_wrapper
    async def test_get_all_laps_for_driver(self, mock_fetch):
        mock_fetch.return_value = await get_mock_response('all_laps')
        driver = parser.get_driver_info('alonso')
        laps = await parser.get_all_laps(15, 2008)
        res = await parser.get_all_laps_for_driver(driver, laps)
        self.check_data(res['data'])
        self.assertEqual(res['data'][0]['Lap'], 1, "First lap should be 1.")
        self.assertEqual(res['driver']['surname'], 'Alonso', "Driver doesn't match that provided.")

    
    @patch(fetch_path)
    @async_wrapper
    async def test_get_driver_poles(self, mock_fetch):
        mock_fetch.return_value = await get_mock_response('driver_poles')
        res = await parser.get_driver_poles('alonso')
        self.check_data(res['data'])
        self.check_total_and_num_results(res['total'], res['data'])
    

    # test career
    @patch(fetch_path)
    @async_wrapper
    async def test_get_driver_wins(self, mock_fetch):
        mock_fetch.return_value = await get_mock_response('driver_wins')
        res = await parser.get_driver_wins('alonso')
        self.check_data(res['data'])
        self.check_total_and_num_results(res['total'], res['data'])

    
    @patch(fetch_path)
    @async_wrapper
    async def test_get_driver_teams(self, mock_fetch):
        mock_fetch.return_value = await get_mock_response('driver_teams')
        res = await parser.get_driver_teams('hamilton')
        # print("API OUTPUT: ", res)
        # self.assertTrue(res['data'], "Results empty.")
        self.check_data(res['data'])
        self.assertEqual(len(res['data']), 2)
        self.assertTrue(res['data'][0] == 'McLaren') 


    @patch(fetch_path)
    @async_wrapper
    async def test_get_driver_seasons(self, mock_fetch):
        mock_fetch.return_value = await get_mock_response('driver_seasons')
        res = await parser.get_driver_seasons('hamilton')
        self.check_data(res['data'])
        self.assertEqual(len(res['data']), 16)
        self.assertTrue(res['data'][0]['year'] == 2007)

    

    @patch(fetch_path)
    @async_wrapper
    async def test_get_driver_career(self, mock_fetch):
        mock_fetch.side_effect = [
            await get_mock_response('driver_championships'),
            await get_mock_response('driver_wins'),
            await get_mock_response('driver_poles'),
            await get_mock_response('driver_seasons'),
            await get_mock_response('driver_teams'),
        ]
        driver = parser.get_driver_info('alonso')
        res = await parser.get_driver_career(driver)
        self.assertEqual(res['driver']['surname'], 'Alonso')
        # Check length of results
        data = res['data']
        self.check_total_and_num_results(data['Championships']['total'], data['Championships']['years'])
        self.check_total_and_num_results(data['Seasons']['total'], data['Seasons']['years'])
        self.check_total_and_num_results(data['Teams']['total'], data['Teams']['names'])

if __name__ == '__main__':
    unittest.main()