import requests
import logging
from .strategies import Strategies

logger = logging.getLogger(__name__)
'''
Object for placing trades on Charles Schwab. 

'''
class Trades:
    def __init__(self, auth):
        self.auth = auth
        self.base_url = None
        self.is_paper_account = False
        self.order_data = None
        self.supported_asset_types = ['EQUITY', 'OPTION', 'FUTURE', 'FOREX', 'INDEX', 'MUTUAL_FUND', 'CASH_EQUIVALENT', 'FIXED_INCOME']
        self.order_type_list = ['MARKET', 'LIMIT', 'STOP', 'STOP_LIMIT', 'TRAILING_STOP', 
                               'NET_DEBIT','OCO', 'TRAILING_STOP_LIMIT']
        self.strategies = Strategies(self.auth)

    def set_paper_account(self, is_paper):
        """
        Set the account type to either paper or live.
        """
        self.is_paper_account = is_paper
        logger.info(f"Set account to {'paper' if is_paper else 'live'}")

    def place_order(self, account_id, asset_type='OPTION', trading_strategy='bull_call', is_paper=False, **kwargs):
        """
        Place an order for a specific trading strategy and asset type.
        """
        self.set_paper_account(is_paper)
        
        if asset_type not in self.supported_asset_types:
            logger.error(f"Asset type {asset_type} is not supported by the Schwab API.")
            raise ValueError(f"Asset type {asset_type} is not supported by the Schwab API.")
        
        if asset_type == 'EQUITY':
            if trading_strategy == 'buy_market_stock':
                self.order_data = self.__buy_market_stock(account_id, **kwargs)
            elif trading_strategy == 'buy_limit_stock':
                self.order_data = self.__buy_limit_stock(account_id, **kwargs)
            elif trading_strategy == 'sell_trailing_stop':
                self.order_data = self.__sell_trailing_stop(account_id, **kwargs)
            elif trading_strategy == 'ota_conditional_order':
                self.order_data = self.__ota_conditional_order(account_id, **kwargs)
            elif trading_strategy == 'oca_conditional_order':
                self.order_data = self.__oca_conditional_order(account_id, **kwargs)
            elif trading_strategy.startswith('conditional_order'):
                self.order_data = self.__conditional_order(account_id, **kwargs)
            else:
                logger.error(f"Trading strategy {trading_strategy} is not supported for EQUITY.")
                raise ValueError(f"Trading strategy {trading_strategy} is not supported for EQUITY.")
        elif asset_type == 'FOREX':
            if trading_strategy == 'forex_order':
                self.order_data = self.__forex_order(account_id, **kwargs)
            elif trading_strategy == 'sell_trailing_stop':
                self.order_data = self.__sell_trailing_stop(account_id, **kwargs)
            else:
                logger.error(f"Trading strategy {trading_strategy} is not supported for FOREX.")
                raise ValueError(f"Trading strategy {trading_strategy} is not supported for FOREX.")
        else:
            strategies_list = self.strategies.existing_strategies()

            if trading_strategy not in strategies_list:
                logger.error(f"Trading strategy {trading_strategy} is not implemented.")
                raise ValueError(f"Trading strategy {trading_strategy} is not implemented.")
            
            strategy_method = getattr(self.strategies, trading_strategy)
            self.order_data = strategy_method(account_id=account_id, asset_type=asset_type, **kwargs)

        if self.is_paper_account:
            self.base_url = None
        else:
            self.base_url = 'https://api.schwabapi.com/trader/v1/accounts'
        
        url = f"{self.base_url}/{account_id}/orders"
        headers = self.auth.get_headers()
        try:
            response = requests.post(url, headers=headers, json=self.order_data)
            response.raise_for_status()
            logger.info(f"Placed order for account ID: {account_id}")
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred while placing order: {http_err}")
            raise SystemExit(f"HTTP error occurred while placing order: {http_err}")
        except Exception as err:
            logger.error(f"An error occurred while placing order: {err}")
            raise SystemExit(f"An error occurred while placing order: {err}")

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

    def __buy_market_stock(self, account_id, symbol, quantity):
        """
        Generate order data for buying stock at market price.
        """
        order_data = {
            "orderType": "MARKET", 
            "session": "NORMAL", 
            "duration": "DAY", 
            "orderStrategyType": "SINGLE", 
            "orderLegCollection": [ 
                { 
                    "instruction": "BUY", 
                    "quantity": quantity, 
                    "instrument": { 
                        "symbol": symbol, 
                        "assetType": "EQUITY" 
                    } 
                } 
            ] 
        }
        logger.info(f"Generated buy market stock order data for symbol: {symbol}")
        return order_data

    def __buy_limit_stock(self, account_id, symbol, quantity, price):
        """
        Generate order data for buying stock at limit price.
        """
        order_data = {
            "orderType": "LIMIT", 
            "session": "NORMAL", 
            "duration": "DAY", 
            "price": price,
            "orderStrategyType": "SINGLE", 
            "orderLegCollection": [ 
                { 
                    "instruction": "BUY", 
                    "quantity": quantity, 
                    "instrument": { 
                        "symbol": symbol, 
                        "assetType": "EQUITY" 
                    } 
                } 
            ] 
        }
        logger.info(f"Generated buy limit stock order data for symbol: {symbol}")
        return order_data

    def __sell_trailing_stop(self, account_id, symbol, quantity, trail_offset):
        """
        Generate order data for selling stock with trailing stop.
        """
        order_data = {
            "orderType": "TRAILING_STOP",
            "session": "NORMAL",
            "stopPriceLinkBasis": "BID",
            "stopPriceLinkType": "VALUE",
            "stopPriceOffset": trail_offset,
            "duration": "DAY",
            "orderStrategyType": "SINGLE",
            "orderLegCollection": [
                {
                    "instruction": "SELL",
                    "quantity": quantity,
                    "instrument": {
                        "symbol": symbol,
                        "assetType": "EQUITY"
                    }
                }
            ]
        }
        logger.info(f"Generated sell trailing stop order data for symbol: {symbol}")
        return order_data

    def __ota_conditional_order(self, account_id, symbol, buy_quantity, buy_price, sell_quantity, sell_price):
        """
        Generate order data for conditional order (one triggers another).
        """
        order_data = {
            "orderType": "LIMIT",
            "session": "NORMAL",
            "price": buy_price,
            "duration": "DAY",
            "orderStrategyType": "TRIGGER",
            "orderLegCollection": [
                {
                    "instruction": "BUY",
                    "quantity": buy_quantity,
                    "instrument": {
                        "symbol": symbol,
                        "assetType": "EQUITY"
                    }
                }
            ],
            "childOrderStrategies": [
                {
                    "orderType": "LIMIT",
                    "session": "NORMAL",
                    "price": sell_price,
                    "duration": "DAY",
                    "orderStrategyType": "SINGLE",
                    "orderLegCollection": [
                        {
                            "instruction": "SELL",
                            "quantity": sell_quantity,
                            "instrument": {
                                "symbol": symbol,
                                "assetType": "EQUITY"
                            }
                        }
                    ]
                }
            ]
        }
        logger.info(f"Generated conditional order (one triggers another) data for symbol: {symbol}")
        return order_data

    def __oca_conditional_order(self, account_id, symbol, quantity, limit_price, stop_price, stop_limit_price):
        """
        Generate order data for conditional order (one cancels another).
        """
        order_data = {
            "orderStrategyType": "OCO",
            "childOrderStrategies": [
                {
                    "orderType": "LIMIT",
                    "session": "NORMAL",
                    "price": limit_price,
                    "duration": "DAY",
                    "orderStrategyType": "SINGLE",
                    "orderLegCollection": [
                        {
                            "instruction": "SELL",
                            "quantity": quantity,
                            "instrument": {
                                "symbol": symbol,
                                "assetType": "EQUITY"
                            }
                        }
                    ]
                },
                {
                    "orderType": "STOP_LIMIT",
                    "session": "NORMAL",
                    "price": stop_limit_price,
                    "stopPrice": stop_price,
                    "duration": "DAY",
                    "orderStrategyType": "SINGLE",
                    "orderLegCollection": [
                        {
                            "instruction": "SELL",
                            "quantity": quantity,
                            "instrument": {
                                "symbol": symbol,
                                "assetType": "EQUITY"
                            }
                        }
                    ]
                }
            ]
        }
        logger.info(f"Generated conditional order (one cancels another) data for symbol: {symbol}")
        return order_data

    def __forex_order(self, symbol, quantity, order_type='LIMIT', price=None):
        """
        Generate order data for forex order.
        """
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
        logger.info(f"Generated forex order data for symbol: {symbol}")
        return order_data

    def __conditional_order(self, symbol, quantity, condition, order_type='LIMIT', price=None):
        """
        Generate order data for conditional order.
        """
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
        logger.info(f"Generated conditional order data for symbol: {symbol}")
        return order_data

    # hidden method that initiates market orders for sequrities
    def __place_security_order(self, account_id, symbol, quantity, action, order_type, price=None, use_margin=False):
        NotImplementedError

    def __place_index_order(self, account_id, symbol, quantity, action, order_type, price=None, use_margin=False):
        NotImplementedError