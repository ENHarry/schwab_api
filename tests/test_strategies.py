import unittest
from schwab_api.strategies import Strategies

class TestStrategies(unittest.TestCase):
    def setUp(self):
        self.auth = patch('schwab_api.auth.SchwabAuth').start()
        self.strategies = Strategies(self.auth)

    def tearDown(self):
        patch.stopall()

    def test_bear_call(self):
        order_data = self.strategies.bear_call(
            account_id='test_account_id',
            symbol='AAPL',
            short_call_strike='150',
            long_call_strike='155',
            quantity=1,
            order_type='LIMIT',
            price=1.00
        )
        expected_order_data = {
            'orderType': 'LIMIT',
            'price': 1.00,
            'orderStrategyType': 'SINGLE',
            'orderLegCollection': [
                {
                    'instruction': 'SELL_TO_OPEN',
                    'quantity': 1,
                    'instrument': {
                        'symbol': 'AAPL 150 C',
                        'assetType': 'OPTION'
                    }
                },
                {
                    'instruction': 'BUY_TO_OPEN',
                    'quantity': 1,
                    'instrument': {
                        'symbol': 'AAPL 155 C',
                        'assetType': 'OPTION'
                    }
                }
            ]
        }
        self.assertEqual(order_data, expected_order_data)

    def test_long_call_butterfly(self):
        order_data = self.strategies.long_call_butterfly(
            account_id='test_account_id',
            symbol='AAPL',
            lower_strike='145',
            middle_strike='150',
            upper_strike='155',
            quantity=1,
            order_type='LIMIT',
            price=1.00
        )
        expected_order_data = {
            'orderType': 'LIMIT',
            'price': 1.00,
            'orderStrategyType': 'SINGLE',
            'orderLegCollection': [
                {
                    'instruction': 'BUY_TO_OPEN',
                    'quantity': 1,
                    'instrument': {
                        'symbol': 'AAPL 145 C',
                        'assetType': 'OPTION'
                    }
                },
                {
                    'instruction': 'SELL_TO_OPEN',
                    'quantity': 2,
                    'instrument': {
                        'symbol': 'AAPL 150 C',
                        'assetType': 'OPTION'
                    }
                },
                {
                    'instruction': 'BUY_TO_OPEN',
                    'quantity': 1,
                    'instrument': {
                        'symbol': 'AAPL 155 C',
                        'assetType': 'OPTION'
                    }
                }
            ]
        }
        self.assertEqual(order_data, expected_order_data)

if __name__ == '__main__':
    unittest.main()
