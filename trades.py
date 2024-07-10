import requests
from .strategies import Strategies

class Trades:
    def __init__(self, auth):
        self.auth = auth
        self.base_url = 'https://api.schwabapi.com/trades'
        self.is_paper_account = False
        self.order_data = None
        self.supported_asset_types = ['EQUITY', 'OPTION', 'FUTURE', 'FOREX', 'INDEX', 'MUTUAL_FUND', 'CASH_EQUIVALENT', 'FIXED_INCOME']

    def set_paper_account(self, is_paper):
        self.is_paper_account = is_paper

    def place_order(self, account_id, asset_type='OPTION', trading_strategy='bull_call', is_paper=False, **kwargs):
        self.set_paper_account(is_paper)
        
        if asset_type not in self.supported_asset_types:
            raise ValueError(f"Asset type {asset_type} is not supported by the Schwab API.")
        
        strategies = Strategies(self.auth)
        strategies_list = strategies.existing_strategies()

        if trading_strategy not in strategies_list:
            raise ValueError(f"Trading strategy {trading_strategy} is not implemented.")
        
        strategy_method = getattr(strategies, trading_strategy)
        self.order_data = strategy_method(account_id=account_id, asset_type=asset_type, **kwargs)

        if self.is_paper_account:
            self.base_url = 'https://api.schwabapi.com/paper_trades'
        else:
            self.base_url = 'https://api.schwabapi.com/live_trades'
        
        url = f"{self.base_url}/{account_id}/orders"
        headers = self.auth.get_headers()
        response = requests.post(url, headers=headers, json=self.order_data)
        response.raise_for_status()
        return response.json()

    def get_order_status(self, account_id, order_id):
        if self.is_paper_account:
            self.base_url = 'https://api.schwabapi.com/paper_trades'
        else:
            self.base_url = 'https://api.schwabapi.com/live_trades'
        
        url = f"{self.base_url}/{account_id}/orders/{order_id}"
        headers = self.auth.get_headers()
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()


    def place_option_order(self, account_id, symbol, quantity, action, order_type, price=None, use_margin=False):
        order_data = {
            'orderType': order_type,
            'price': price,
            'quantity': quantity,
            'symbol': symbol,
            'action': action,
            'assetType': 'OPTION',
            'useMargin': use_margin
        }
        return self.place_order(account_id, order_data)

    def place_future_order(self, account_id, symbol, quantity, action, order_type, price=None, use_margin=False):
        order_data = {
            'orderType': order_type,
            'price': price,
            'quantity': quantity,
            'symbol': symbol,
            'action': action,
            'assetType': 'FUTURE',
            'useMargin': use_margin
        }
        return self.place_order(account_id, order_data)

    def place_forex_order(self, account_id, symbol, quantity, action, order_type, price=None, use_margin=False):
        order_data = {
            'orderType': order_type,
            'price': price,
            'quantity': quantity,
            'symbol': symbol,
            'action': action,
            'assetType': 'FOREX',
            'useMargin': use_margin
        }
        return self.place_order(account_id, order_data)

    def place_security_order(self, account_id, symbol, quantity, action, order_type, price=None, use_margin=False):
        order_data = {
            'orderType': order_type,
            'price': price,
            'quantity': quantity,
            'symbol': symbol,
            'action': action,
            'assetType': 'EQUITY',
            'useMargin': use_margin
        }
        return self.place_order(account_id, order_data)

    def place_index_order(self, account_id, symbol, quantity, action, order_type, price=None, use_margin=False):
        order_data = {
            'orderType': order_type,
            'price': price,
            'quantity': quantity,
            'symbol': symbol,
            'action': action,
            'assetType': 'INDEX',
            'useMargin': use_margin
        }
        return self.place_order(account_id, order_data)

    def place_stop_loss_order(self, account_id, symbol, quantity, action, stop_price, use_margin=False):
        order_data = {
            'orderType': 'STOP',
            'stopPrice': stop_price,
            'quantity': quantity,
            'symbol': symbol,
            'action': action,
            'useMargin': use_margin
        }
        return self.place_order(account_id, order_data)

    def place_trailing_stop_order(self, account_id, symbol, quantity, action, trail_amount, use_margin=False):
        order_data = {
            'orderType': 'TRAILING_STOP',
            'trailAmount': trail_amount,
            'quantity': quantity,
            'symbol': symbol,
            'action': action,
            'useMargin': use_margin
        }
        return self.place_order(account_id, order_data)

    def place_limit_order(self, account_id, symbol, quantity, action, limit_price, use_margin=False):
        order_data = {
            'orderType': 'LIMIT',
            'price': limit_price,
            'quantity': quantity,
            'symbol': symbol,
            'action': action,
            'useMargin': use_margin
        }
        return self.place_order(account_id, order_data)

    def place_stop_limit_order(self, account_id, symbol, quantity, action, stop_price, limit_price, use_margin=False):
        order_data = {
            'orderType': 'STOP_LIMIT',
            'stopPrice': stop_price,
            'price': limit_price,
            'quantity': quantity,
            'symbol': symbol,
            'action': action,
            'useMargin': use_margin
        }
        return self.place_order(account_id, order_data)

    def place_oco_order(self, account_id, primary_order, secondary_order, use_margin=False):
        order_data = {
            'orderStrategyType': 'OCO',
            'primaryOrder': primary_order,
            'secondaryOrder': secondary_order,
            'useMargin': use_margin
        }
        return self.place_order(account_id, order_data)
