import requests
from .strategies import Strategies

class Trades:
    def __init__(self, auth):
        self.auth = auth
        self.base_url = 'https://api.schwabapi.com/trader/v1/accounts'        
        self.is_paper_account = False
        self.order_data = None
        self.supported_asset_types = ['EQUITY', 'OPTION', 'FUTURE', 'FOREX', 'INDEX', 'MUTUAL_FUND', 'CASH_EQUIVALENT', 'FIXED_INCOME']

    def set_paper_account(self, is_paper):
        self.is_paper_account = is_paper

    def place_order(self, account_id, asset_type='OPTION', trading_strategy='bull_call', is_paper=False, **kwargs):
        self.set_paper_account(is_paper)
        
        if asset_type not in self.supported_asset_types:
            raise ValueError(f"Asset type {asset_type} is not supported by the Schwab API.")
        
        if asset_type == 'EQUITY':
            if trading_strategy == 'buy_market_stock':
                self.order_data = self._buy_market_stock(account_id, **kwargs)
            elif trading_strategy.startswith('conditional_order'):
                self.order_data = self._conditional_order(account_id, **kwargs)
            else:
                raise ValueError(f"Trading strategy {trading_strategy} is not supported for EQUITY.")
        elif asset_type == 'FOREX':
            if trading_strategy == 'forex_order':
                self.order_data = self._forex_order(account_id, **kwargs)
            else:
                raise ValueError(f"Trading strategy {trading_strategy} is not supported for FOREX.")
        else:
            strategies = Strategies(self.auth)
            strategies_list = strategies.existing_strategies()

            if trading_strategy not in strategies_list:
                raise ValueError(f"Trading strategy {trading_strategy} is not implemented.")
            
            strategy_method = getattr(strategies, trading_strategy)
            self.order_data = strategy_method(account_id=account_id, asset_type=asset_type, **kwargs)

        if self.is_paper_account:
            self.base_url = None
        else:
            self.base_url = 'https://api.schwabapi.com/trader/v1/accounts'
        
        url = f"{self.base_url}/{account_id}/orders"
        headers = self.auth.get_headers()
        response = requests.post(url, headers=headers, json=self.order_data)
        response.raise_for_status()
        return response.json()

    def get_order_status(self, account_id, order_id):
        if self.is_paper_account:
            raise TypeError('Paper account does not support order status')
        else:
            self.base_url = 'https://api.schwabapi.com/trader/v1/accounts'
        
        url = f"{self.base_url}/{account_id}/orders/{order_id}"
        headers = self.auth.get_headers()
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    # Private methods for Buy Market: Stock, Conditional orders, and forex

    def _buy_market_stock(self, symbol, quantity, action, order_type):
        order_data = {
                "orderType": order_type, 
                "session": "NORMAL", 
                "duration": "DAY", 
                "orderStrategyType": "SINGLE", 
                "orderLegCollection": [ 
                { 
                    "instruction": action, 
                    "quantity": quantity, 
                    "instrument": { 
                    "symbol": symbol, 
                    "assetType": "EQUITY" 
                    } 
                } 
            ] 
                }
        return order_data

    def _conditional_order(self, symbol, quantity, condition, order_type='LIMIT', price=None):
        order_data = {
            'orderType': order_type,
            'price': price,
            'session': 'NORMAL',
            'duration': 'GOOD_TILL_CANCEL',
            'orderStrategyType': 'SINGLE',
            'orderLegCollection': [
                {
                    'instruction': 'BUY',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': symbol,
                        'assetType': 'EQUITY'
                    }
                }
            ],
            'specialInstruction': condition
        }
        return order_data

    def _forex_order(self,symbol, quantity, order_type='LIMIT', price=None):
        order_data = {
            'orderType': order_type,
            'price': price,
            'session': 'NORMAL',
            'duration': 'DAY',
            'orderStrategyType': 'SINGLE',
            'orderLegCollection': [
                {
                    'instruction': 'BUY',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': symbol,
                        'assetType': 'FOREX'
                    }
                }
            ]
        }
        return order_data
