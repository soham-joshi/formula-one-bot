import unittest

class BaseTest(unittest.TestCase):
    """Base testing class."""

    def check_data(self, data):
        self.assertTrue(len(data) > 0, "Results are empty.")
        self.assertNotIn(None, [i for i in data[0]], "None values present. Check keys.")

    def check_total_and_num_results(self, total, data):
        self.assertTrue(isinstance(total, int), "Total is not valid.")
        self.assertEqual(total, len(data), "Total and number of results don't match.")