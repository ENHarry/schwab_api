import unittest
from unittest.mock import patch
from schwab_api.strategies import Strategies

class TestStrategies(unittest.TestCase):
    def setUp(self):
        self.auth = patch('schwab_api.auth.SchwabAuth').start()
        self.strategies = Strategies(self.auth)

    def tearDown(self):
        patch.stopall()

    def test_existing_strategies(self):
        strategies_list = self.strategies.existing_strategies()
        self.assertIn('bull_call', strategies_list)

    def test_strangle(self):
        order_data = self.strategies.strangle('account_id', 'AAPL', 100, 110, 1)
        self.assertIsInstance(order_data, dict)

    def test_iron_condor(self):
        order_data = self.strategies.iron_condor('account_id', 'AAPL', 100, 110, 120, 130, 1)
        self.assertIsInstance(order_data, dict)

    def test_butterfly(self):
        order_data = self.strategies.butterfly('account_id', 'AAPL', 100, 110, 120, 1)
        self.assertIsInstance(order_data, dict)

    def test_diagonal_spread(self):
        order_data = self.strategies.diagonal_spread('account_id', 'AAPL', 100, '2023-12-31', 110, '2024-12-31', 1)
        self.assertIsInstance(order_data, dict)

    def test_bear_call(self):
        self.assertIsNone(self.strategies.bear_call())

    def test_invalid_strategy(self):
        with self.assertRaises(AttributeError):
            getattr(self.strategies, 'non_existent_strategy')

if __name__ == '__main__':
    unittest.main()
