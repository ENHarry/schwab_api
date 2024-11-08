import requests
import logging
from .strategies import Strategies

logger = logging.getLogger(__name__)
'''
Object for placing trades on Charles Schwab. 

'''
class Trader:
    def __init__(self, auth, override_base_url=None, override_paper_account=None):
        self.auth = auth
        if override_base_url is not None:
            self.base_url = override_base_url
        else:
            self.base_url = 'https://api.schwabapi.com/trader/v1/'
        
        if override_paper_account is not None:
            self.is_paper_account = override_paper_account
        else:
            self.is_paper_account = self.auth.is_paper_account

        self.order_data = None
        self.supported_asset_types = ['EQUITY', 'OPTION', 'FUTURE', 'FOREX', 'INDEX', 'MUTUAL_FUND', 'CASH_EQUIVALENT', 'FIXED_INCOME']
        self.order_type_list = ['MARKET', 'LIMIT', 'STOP', 'STOP_LIMIT', 'TRAILING_STOP', 
                               'NET_DEBIT','OCO', 'TRAILING_STOP_LIMIT']
        self.strategies = Strategies(self.auth)

    def _set_paper_account(self):
        """
        Set the account type to either paper or live.
        """
        self.is_paper_account = self.auth.get_accType()
        logger.info(f"Set account to {'paper' if self.is_paper_account else 'live'}")

    def place_order(self, account_id, asset_type='OPTION', trading_strategy='buy_market_stock',  **kwargs):
        """
        Place an order for a specific trading strategy and asset type.
        """
        self._set_paper_account()
        
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

    def get_account_info(self, account_id):
        """
        Retrieves information for a specific account.
        
        :param account_id: ID of the account
        :return: JSON response containing account information
        """
        url = f"{self.base_url}/accounts/{account_id}"
        headers = self.auth.get_headers()
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            logger.info(f"Retrieved account info for account ID: {account_id}")
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred while retrieving account info: {http_err}")
            raise SystemExit(f"HTTP error occurred while retrieving account info: {http_err}")
        except Exception as err:
            logger.error(f"An error occurred while retrieving account info: {err}")
            raise SystemExit(f"An error occurred while retrieving account info: {err}")

    def get_all_accounts(self):
        """
        Retrieves information for all accounts.
        
        :return: JSON response containing all account information
        """
        url = f"{self.base_url}/accounts/"
        headers = self.auth.get_headers()
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            logger.info("Retrieved all account info")
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred while retrieving all accounts: {http_err}")
            raise SystemExit(f"HTTP error occurred while retrieving all accounts: {http_err}")
        except Exception as err:
            logger.error(f"An error occurred while retrieving all accounts: {err}")
            raise SystemExit(f"An error occurred while retrieving all accounts: {err}")

    def get_all_accountIDs(self):
        """
        Retrieves all account IDs.
        
        :return: JSON response containing all account IDs
        """
        url = f"{self.base_url}/accounts/accountNumbers"
        headers = self.auth.get_headers()
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            logger.info("Retrieved all account IDs")
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred while retrieving account IDs: {http_err}")
            raise SystemExit(f"HTTP error occurred while retrieving account IDs: {http_err}")
        except Exception as err:
            logger.error(f"An error occurred while retrieving account IDs: {err}")
            raise SystemExit(f"An error occurred while retrieving account IDs: {err}")

    def get_all_transactions(self, account_id):
        """
        Retrieves all transactions for a specific account.
        
        :param account_id: ID of the account
        :return: JSON response containing all transactions for the account
        """
        url = f"{self.base_url}/accounts/{account_id}/transactions"
        headers = self.auth.get_headers()
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            logger.info(f"Retrieved all transactions for account ID: {account_id}")
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred while retrieving transactions: {http_err}")
            raise SystemExit(f"HTTP error occurred while retrieving transactions: {http_err}")
        except Exception as err:
            logger.error(f"An error occurred while retrieving transactions: {err}")
            raise SystemExit(f"An error occurred while retrieving transactions: {err}")

    def get_transaction(self, account_id, transaction_id):
        """
        Retrieves details for a specific transaction.
        
        :param account_id: ID of the account
        :param transaction_id: ID of the transaction
        :return: JSON response containing transaction details
        """
        url = f"{self.base_url}/accounts/{account_id}/transactions/{transaction_id}"
        headers = self.auth.get_headers()
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            logger.info(f"Retrieved transaction details for transaction ID: {transaction_id}")
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred while retrieving transaction: {http_err}")
            raise SystemExit(f"HTTP error occurred while retrieving transaction: {http_err}")
        except Exception as err:
            logger.error(f"An error occurred while retrieving transaction: {err}")
            raise SystemExit(f"An error occurred while retrieving transaction: {err}")

    def get_user_preferences(self):
        """
        Retrieves user preferences.
        
        :return: JSON response containing user preferences
        """
        url = f"{self.base_url}/userPreferences"
        headers = self.auth.get_headers()
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            raise SystemExit(f"HTTP error occurred while retrieving user preferences: {http_err}")
        except Exception as err:
            raise SystemExit(f"An error occurred while retrieving user preferences: {err}")

    '''def set_trade_environment(self, trades_object, is_paper):
        """
        Sets the trading environment (paper/live) for the trades object.
        
        :param trades_object: Trades object to set environment for
        :param is_paper: Boolean indicating if the environment is paper (True) or live (False)
        """
        trades_object.set_paper_account(is_paper)'''