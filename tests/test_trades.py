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
    
    @patch('requests.post')
    def test_buy_market_stock(self, mock_post):
        self.trades._buy_market_stock(symbol='AAPL', quantity=10, action='BUY', order_type='MARKET')
        expected_order_data = {
            "orderType": 'MARKET',
            "session": "NORMAL",
            "duration": "DAY",
            "orderStrategyType": "SINGLE",
            "orderLegCollection": [
                {
                    "instruction": 'BUY',
                    "quantity": 10,
                    "instrument": {
                        "symbol": 'AAPL',
                        "assetType": "EQUITY"
                    }
                }
            ]
        }
        self.assertEqual(self.trades.order_data, expected_order_data)


    def test_place_order_buy_market_stock(self):
        order_data = self.trades.place_order('account_id', asset_type='EQUITY', trading_strategy='buy_market_stock', symbol='AAPL', quantity=10)
        self.assertIsInstance(order_data, dict)

    def test_place_order_buy_limit_stock(self):
        order_data = self.trades.place_order('account_id', asset_type='EQUITY', trading_strategy='buy_limit_stock', symbol='AAPL', quantity=10, price=150)
        self.assertIsInstance(order_data, dict)

    def test_place_order_sell_trailing_stop(self):
        order_data = self.trades.place_order('account_id', asset_type='EQUITY', trading_strategy='sell_trailing_stop', symbol='AAPL', quantity=10, trail_offset=10)
        self.assertIsInstance(order_data, dict)

    def test_place_order_ota_conditional_order(self):
        order_data = self.trades.place_order('account_id', asset_type='EQUITY', trading_strategy='ota_conditional_order', symbol='AAPL', buy_quantity=10, buy_price=150, sell_quantity=10, sell_price=160)
        self.assertIsInstance(order_data, dict)

    def test_place_order_oca_conditional_order(self):
        order_data = self.trades.place_order('account_id', asset_type='EQUITY', trading_strategy='oca_conditional_order', symbol='AAPL', quantity=10, limit_price=160, stop_price=140, stop_limit_price=139)
        self.assertIsInstance(order_data, dict)

    def test_place_order_invalid_asset_type(self):
        with self.assertRaises(ValueError):
            self.trades.place_order('account_id', asset_type='INVALID', trading_strategy='buy_market_stock', symbol='AAPL', quantity=10)

    def test_place_order_invalid_trading_strategy(self):
        with self.assertRaises(ValueError):
            self.trades.place_order('account_id', asset_type='EQUITY', trading_strategy='invalid_strategy', symbol='AAPL', quantity=10)

    def test_place_order_access_strategy_directly(self):
        with self.assertRaises(AttributeError):
            self.trades.strategies.bear_call()


if __name__ == '__main__':
    unittest.main()
