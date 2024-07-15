import unittest
from unittest.mock import patch
from schwab_api.trades import Trades

class TestTrades(unittest.TestCase):
    def setUp(self):
        self.auth = patch('schwab_api.auth.SchwabAuth').start()
        self.trades = Trades(self.auth)

    def tearDown(self):
        patch.stopall()

    @patch('requests.post')
    def test_place_order_equity(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {'order': 'placed'}
        response = self.trades.place_order(
            account_id='test_account_id',
            asset_type='EQUITY',
            trading_strategy='buy_market_stock',
            symbol='AAPL',
            quantity=10
        )
        self.assertEqual(response, {'order': 'placed'})

    @patch('requests.post')
    def test_place_order_forex(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {'order': 'placed'}
        response = self.trades.place_order(
            account_id='test_account_id',
            asset_type='FOREX',
            trading_strategy='forex_order',
            symbol='EUR/USD',
            quantity=1000,
            order_type='LIMIT',
            price=1.2
        )
        self.assertEqual(response, {'order': 'placed'})

    @patch('requests.post')
    def test_place_order_option(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {'order': 'placed'}
        response = self.trades.place_order(
            account_id='test_account_id',
            asset_type='OPTION',
            trading_strategy='bear_call',
            symbol='AAPL',
            short_call_strike='150',
            long_call_strike='155',
            quantity=1,
            order_type='LIMIT',
            price=1.00
        )
        self.assertEqual(response, {'order': 'placed'})

if __name__ == '__main__':
    unittest.main()
