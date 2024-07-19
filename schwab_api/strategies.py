import logging

logger = logging.getLogger(__name__)

class Strategies:
    def __init__(self, auth):
        self.auth = auth
        self.strategies_list = [
            'bear_call', 'bear_put', 'bull_call', 'bull_put', 'covered_call',
            'long_call_butterfly', 'long_call_condor', 'long_put_condor',
            'long_straddle', 'long_strangle', 'married_put',
            'protective_collar', 'short_call_butterfly', 'short_call_condor',
            'short_iron_condor', 'straddle_strangle_swap', 'calendar_call',
            'calendar_put', 'iron_butterfly', 'iron_condor', 'butterfly',
            'diagonal_spread', 'strangle'
        ]

    def existing_strategies(self):
        """
        Returns the list of existing strategies.

        :return: A list of existing strategies.
        :rtype: list
        """
        return self.strategies_list

    def bear_call(self, symbol, short_call_strike, long_call_strike, quantity, asset_type='OPTION', order_type='LIMIT', price=None):
        """
        A function to generate order data for a bear call strategy.

        :param symbol: The symbol for the option contract.
        :param short_call_strike: The strike price for the short call option.
        :param long_call_strike: The strike price for the long call option.
        :param quantity: The quantity of the options to be traded.
        :param asset_type: The type of asset (default is 'OPTION').
        :param order_type: The type of order (default is 'LIMIT').
        :param price: The price at which the order should be executed (default is None).
        :return: The order data for the bear call strategy.
        :rtype: dict
        """
        order_data = {
            'orderType': order_type,
            'price': price,
            'orderStrategyType': 'SINGLE',
            'orderLegCollection': [
                {
                    'instruction': 'SELL_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {short_call_strike} C',
                        'assetType': asset_type
                    }
                },
                {
                    'instruction': 'BUY_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {long_call_strike} C',
                        'assetType': asset_type
                    }
                }
            ]
        }
        logger.info(f"Generated bear call order data for symbol: {symbol}")
        return order_data

    def bear_put(self,  symbol, short_put_strike, long_put_strike, quantity, asset_type='OPTION', order_type='LIMIT', price=None):
        """
        A function to generate order data for a bear put strategy.

        :param symbol: The symbol for the option contract.
        :param short_put_strike: The strike price for the short put option.
        :param long_put_strike: The strike price for the long put option.
        :param quantity: The quantity of the options to be traded.
        :param asset_type: The type of asset (default is 'OPTION').
        :param order_type: The type of order (default is 'LIMIT').
        :param price: The price at which the order should be executed (default is None).
        :return: The order data for the bear put strategy.
        :rtype: dict
        """
        order_data = {
            'orderType': order_type,
            'price': price,
            'orderStrategyType': 'SINGLE',
            'orderLegCollection': [
                {
                    'instruction': 'BUY_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {long_put_strike} P',
                        'assetType': asset_type
                    }
                },
                {
                    'instruction': 'SELL_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {short_put_strike} P',
                        'assetType': asset_type
                    }
                }
            ]
        }
        logger.info(f"Generated bear put order data for symbol: {symbol}")
        return order_data

    def bull_call(self,  symbol, long_call_strike, short_call_strike, quantity, asset_type='OPTION', order_type='LIMIT', price=None):
        """
        Generates order data for a bull call strategy.

        Args:
            symbol (str): The symbol for the option contract.
            long_call_strike (float): The strike price for the long call option.
            short_call_strike (float): The strike price for the short call option.
            quantity (int): The quantity of the options to be traded.
            asset_type (str, optional): The type of asset (default is 'OPTION').
            order_type (str, optional): The type of order (default is 'LIMIT').
            price (float, optional): The price at which the order should be executed (default is None).

        Returns:
            dict: The order data for the bull call strategy.

        """
        order_data = {
            'orderType': order_type,
            'price': price,
            'orderStrategyType': 'SINGLE',
            'orderLegCollection': [
                {
                    'instruction': 'BUY_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {long_call_strike} C',
                        'assetType': asset_type
                    }
                },
                {
                    'instruction': 'SELL_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {short_call_strike} C',
                        'assetType': asset_type
                    }
                }
            ]
        }
        logger.info(f"Generated bull call order data for symbol: {symbol}")
        return order_data

    def bull_put(self,  symbol, long_put_strike, short_put_strike, quantity, asset_type='OPTION', order_type='LIMIT', price=None):
        """
        A function to generate order data for a bull put strategy.

        :param symbol: The symbol for the option contract.
        :param long_put_strike: The strike price for the long put option.
        :param short_put_strike: The strike price for the short put option.
        :param quantity: The quantity of the options to be traded.
        :param asset_type: The type of asset (default is 'OPTION').
        :param order_type: The type of order (default is 'LIMIT').
        :param price: The price at which the order should be executed (default is None).
        :return: The order data for the bull put strategy.
        :rtype: dict
        """
        order_data = {
            'orderType': order_type,
            'price': price,
            'orderStrategyType': 'SINGLE',
            'orderLegCollection': [
                {
                    'instruction': 'SELL_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {short_put_strike} P',
                        'assetType': asset_type
                    }
                },
                {
                    'instruction': 'BUY_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {long_put_strike} P',
                        'assetType': asset_type
                    }
                }
            ]
        }
        logger.info(f"Generated bull put order data for symbol: {symbol}")
        return order_data

    def covered_call(self,  symbol, quantity, call_strike, stock_quantity, asset_type='OPTION', order_type='LIMIT', price=None):
        """
        Generate order data for a covered call strategy.

        Args:
            symbol (str): The symbol for the option contract.
            quantity (int): The quantity of the options to be traded.
            call_strike (float): The strike price for the call option.
            stock_quantity (int): The quantity of the stock to be bought.
            asset_type (str, optional): The type of asset (default is 'OPTION').
            order_type (str, optional): The type of order (default is 'LIMIT').
            price (float, optional): The price at which the order should be executed (default is None).

        Returns:
            dict: The order data for the covered call strategy.

        """
        order_data = {
            'orderType': order_type,
            'price': price,
            'orderStrategyType': 'SINGLE',
            'orderLegCollection': [
                {
                    'instruction': 'SELL_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {call_strike} C',
                        'assetType': asset_type
                    }
                },
                {
                    'instruction': 'BUY',
                    'quantity': stock_quantity,
                    'instrument': {
                        'symbol': symbol,
                        'assetType': 'EQUITY'
                    }
                }
            ]
        }
        logger.info(f"Generated covered call order data for symbol: {symbol}")
        return order_data

    def long_call_butterfly(self,  symbol, lower_strike, middle_strike, upper_strike, quantity, asset_type='OPTION', order_type='LIMIT', price=None):
        """
        Generate order data for a long call butterfly strategy.

        Args:
            symbol (str): The symbol for the option contract.
            lower_strike (float): The lower strike price for the options.
            middle_strike (float): The middle strike price for the options.
            upper_strike (float): The upper strike price for the options.
            quantity (int): The quantity of the options to be traded.
            asset_type (str, optional): The type of asset (default is 'OPTION').
            order_type (str, optional): The type of order (default is 'LIMIT').
            price (float, optional): The price at which the order should be executed (default is None).

        Returns:
            dict: The order data for the long call butterfly strategy.
        """
        order_data = {
            'orderType': order_type,
            'price': price,
            'orderStrategyType': 'SINGLE',
            'orderLegCollection': [
                {
                    'instruction': 'BUY_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {lower_strike} C',
                        'assetType': asset_type
                    }
                },
                {
                    'instruction': 'SELL_TO_OPEN',
                    'quantity': 2 * quantity,
                    'instrument': {
                        'symbol': f'{symbol} {middle_strike} C',
                        'assetType': asset_type
                    }
                },
                {
                    'instruction': 'BUY_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {upper_strike} C',
                        'assetType': asset_type
                    }
                }
            ]
        }
        logger.info(f"Generated long call butterfly order data for symbol: {symbol}")
        return order_data

    def long_call_condor(self, symbol, lower_strike, lower_middle_strike, upper_middle_strike, upper_strike, quantity, asset_type='OPTION', order_type='LIMIT', price=None):
        """
        Generates a long call condor order data for a given symbol.

        Args:
            symbol (str): The symbol of the underlying asset.
            lower_strike (float): The strike price of the lower call option.
            lower_middle_strike (float): The strike price of the lower middle call option.
            upper_middle_strike (float): The strike price of the upper middle call option.
            upper_strike (float): The strike price of the upper call option.
            quantity (int): The quantity of options to buy or sell.
            asset_type (str, optional): The type of the asset. Defaults to 'OPTION'.
            order_type (str, optional): The type of the order. Defaults to 'LIMIT'.
            price (float, optional): The price of the order. Defaults to None.

        Returns:
            dict: The generated long call condor order data.

        """
        order_data = {
            'orderType': order_type,
            'price': price,
            'orderStrategyType': 'SINGLE',
            'orderLegCollection': [
                {
                    'instruction': 'BUY_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {lower_strike} C',
                        'assetType': asset_type
                    }
                },
                {
                    'instruction': 'SELL_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {lower_middle_strike} C',
                        'assetType': asset_type
                    }
                },
                {
                    'instruction': 'SELL_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {upper_middle_strike} C',
                        'assetType': asset_type
                    }
                },
                {
                    'instruction': 'BUY_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {upper_strike} C',
                        'assetType': asset_type
                    }
                }
            ]
        }
        logger.info(f"Generated long call condor order data for symbol: {symbol}")
        return order_data

    def long_put_condor(self,  symbol, lower_strike, lower_middle_strike, upper_middle_strike, upper_strike, quantity, asset_type='OPTION', order_type='LIMIT', price=None):
        """
        Generates a long put condor order data for a given symbol.

        Args:
            symbol (str): The symbol of the underlying asset.
            lower_strike (float): The strike price of the lower put option.
            lower_middle_strike (float): The strike price of the lower middle put option.
            upper_middle_strike (float): The strike price of the upper middle put option.
            upper_strike (float): The strike price of the upper put option.
            quantity (int): The quantity of options to buy or sell.
            asset_type (str, optional): The type of the asset. Defaults to 'OPTION'.
            order_type (str, optional): The type of the order. Defaults to 'LIMIT'.
            price (float, optional): The price of the order. Defaults to None.

        Returns:
            dict: The generated long put condor order data.
        """
        order_data = {
            'orderType': order_type,
            'price': price,
            'orderStrategyType': 'SINGLE',
            'orderLegCollection': [
                {
                    'instruction': 'BUY_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {lower_strike} P',
                        'assetType': asset_type
                    }
                },
                {
                    'instruction': 'SELL_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {lower_middle_strike} P',
                        'assetType': asset_type
                    }
                },
                {
                    'instruction': 'SELL_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {upper_middle_strike} P',
                        'assetType': asset_type
                    }
                },
                {
                    'instruction': 'BUY_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {upper_strike} P',
                        'assetType': asset_type
                    }
                }
            ]
        }
        logger.info(f"Generated long put condor order data for symbol: {symbol}")
        return order_data

    def long_straddle(self,  symbol, quantity, strike_price, asset_type='OPTION', order_type='LIMIT', price=None):
        """
        Generates a long straddle order for the given symbol, quantity, and strike price.

        :param symbol: str, the symbol for the option
        :param quantity: int, the quantity of contracts
        :param strike_price: float, the strike price of the option
        :param asset_type: str, the type of asset (default is 'OPTION')
        :param order_type: str, the type of order (default is 'LIMIT')
        :param price: float, the price of the order

        :return: dict, order data containing the order type, price, order strategy type, and order leg collection
        """
        order_data = {
            'orderType': order_type,
            'price': price,
            'orderStrategyType': 'SINGLE',
            'orderLegCollection': [
                {
                    'instruction': 'BUY_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {strike_price} C',
                        'assetType': asset_type
                    }
                },
                {
                    'instruction': 'BUY_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {strike_price} P',
                        'assetType': asset_type
                    }
                }
            ]
        }
        logger.info(f"Generated long straddle order data for symbol: {symbol}")
        return order_data

    def long_strangle(self,  symbol, quantity, call_strike, put_strike, asset_type='OPTION', order_type='LIMIT', price=None):
        """
        Generates a long strangle order data for a given symbol.

        :param symbol: str, the symbol of the underlying asset
        :param quantity: int, the quantity of options to buy or sell
        :param call_strike: float, the strike price of the call option
        :param put_strike: float, the strike price of the put option
        :param asset_type: str, the type of the asset (default is 'OPTION')
        :param order_type: str, the type of the order (default is 'LIMIT')
        :param price: float, the price of the order

        :return: dict, the generated long strangle order data
        """
        order_data = {
            'orderType': order_type,
            'price': price,
            'orderStrategyType': 'SINGLE',
            'orderLegCollection': [
                {
                    'instruction': 'BUY_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {call_strike} C',
                        'assetType': asset_type
                    }
                },
                {
                    'instruction': 'BUY_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {put_strike} P',
                        'assetType': asset_type
                    }
                }
            ]
        }
        logger.info(f"Generated long strangle order data for symbol: {symbol}")
        return order_data

    def married_put(self,  symbol, quantity, put_strike, stock_quantity, asset_type='OPTION', order_type='LIMIT', price=None):
        """
        A function to generate order data for a married put strategy.

        :param symbol: The symbol for the option contract.
        :param quantity: The quantity of the put option to be traded.
        :param put_strike: The strike price for the put option.
        :param stock_quantity: The quantity of the stock to be traded.
        :param asset_type: The type of asset (default is 'OPTION').
        :param order_type: The type of order (default is 'LIMIT').
        :param price: The price at which the order should be executed (default is None).
        :return: The order data for the married put strategy.
        :rtype: dict
        """
        order_data = {
            'orderType': order_type,
            'price': price,
            'orderStrategyType': 'SINGLE',
            'orderLegCollection': [
                {
                    'instruction': 'BUY_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {put_strike} P',
                        'assetType': asset_type
                    }
                },
                {
                    'instruction': 'BUY',
                    'quantity': stock_quantity,
                    'instrument': {
                        'symbol': symbol,
                        'assetType': 'EQUITY'
                    }
                }
            ]
        }
        logger.info(f"Generated married put order data for symbol: {symbol}")
        return order_data

    def protective_collar(self,  symbol, quantity, put_strike, call_strike, stock_quantity, asset_type='OPTION', order_type='LIMIT', price=None):
        """
        A function to generate order data for a protective collar strategy.

        :param symbol: The symbol for the option contract.
        :param quantity: The quantity of the options to be traded.
        :param put_strike: The strike price for the put option.
        :param call_strike: The strike price for the call option.
        :param stock_quantity: The quantity of the stock to be traded.
        :param asset_type: The type of asset (default is 'OPTION').
        :param order_type: The type of order (default is 'LIMIT').
        :param price: The price at which the order should be executed (default is None).
        :return: The order data for the protective collar strategy.
        :rtype: dict
        """
        order_data = {
            'orderType': order_type,
            'price': price,
            'orderStrategyType': 'SINGLE',
            'orderLegCollection': [
                {
                    'instruction': 'BUY_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {put_strike} P',
                        'assetType': asset_type
                    }
                },
                {
                    'instruction': 'SELL_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {call_strike} C',
                        'assetType': asset_type
                    }
                },
                {
                    'instruction': 'BUY',
                    'quantity': stock_quantity,
                    'instrument': {
                        'symbol': symbol,
                        'assetType': 'EQUITY'
                    }
                }
            ]
        }
        logger.info(f"Generated protective collar order data for symbol: {symbol}")
        return order_data

    def short_call_butterfly(self,  symbol, lower_strike, middle_strike, upper_strike, quantity, asset_type='OPTION', order_type='LIMIT', price=None):
        """
        Generate order data for a short call butterfly strategy.

        Args:
            symbol (str): The symbol for the option contract.
            lower_strike (float): The lower strike price for the options.
            middle_strike (float): The middle strike price for the options.
            upper_strike (float): The upper strike price for the options.
            quantity (int): The quantity of the options to be traded.
            asset_type (str, optional): The type of asset (default is 'OPTION').
            order_type (str, optional): The type of order (default is 'LIMIT').
            price (float, optional): The price at which the order should be executed (default is None).

        Returns:
            dict: The order data for the short call butterfly strategy.
        """
        order_data = {
            'orderType': order_type,
            'price': price,
            'orderStrategyType': 'SINGLE',
            'orderLegCollection': [
                {
                    'instruction': 'SELL_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {lower_strike} C',
                        'assetType': asset_type
                    }
                },
                {
                    'instruction': 'BUY_TO_OPEN',
                    'quantity': 2 * quantity,
                    'instrument': {
                        'symbol': f'{symbol} {middle_strike} C',
                        'assetType': asset_type
                    }
                },
                {
                    'instruction': 'SELL_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {upper_strike} C',
                        'assetType': asset_type
                    }
                }
            ]
        }
        logger.info(f"Generated short call butterfly order data for symbol: {symbol}")
        return order_data

    def short_call_condor(self,  symbol, lower_strike, lower_middle_strike, upper_middle_strike, upper_strike, quantity, asset_type='OPTION', order_type='LIMIT', price=None):
        """
        Generates a short call condor order data for a given symbol.

        Args:
            symbol (str): The symbol of the underlying asset.
            lower_strike (float): The strike price of the lower call option.
            lower_middle_strike (float): The strike price of the lower middle call option.
            upper_middle_strike (float): The strike price of the upper middle call option.
            upper_strike (float): The strike price of the upper call option.
            quantity (int): The quantity of options to buy or sell.
            asset_type (str, optional): The type of the asset. Defaults to 'OPTION'.
            order_type (str, optional): The type of the order. Defaults to 'LIMIT'.
            price (float, optional): The price of the order. Defaults to None.

        Returns:
            dict: The generated short call condor order data.
        """
        order_data = {
            'orderType': order_type,
            'price': price,
            'orderStrategyType': 'SINGLE',
            'orderLegCollection': [
                {
                    'instruction': 'SELL_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {lower_strike} C',
                        'assetType': asset_type
                    }
                },
                {
                    'instruction': 'BUY_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {lower_middle_strike} C',
                        'assetType': asset_type
                    }
                },
                {
                    'instruction': 'BUY_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {upper_middle_strike} C',
                        'assetType': asset_type
                    }
                },
                {
                    'instruction': 'SELL_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {upper_strike} C',
                        'assetType': asset_type
                    }
                }
            ]
        }
        logger.info(f"Generated short call condor order data for symbol: {symbol}")
        return order_data

    def short_iron_condor(self,  symbol, lower_put_strike, upper_put_strike, lower_call_strike, upper_call_strike, quantity, asset_type='OPTION', order_type='LIMIT', price=None):
        """
        A function to generate a short iron condor order. 
        Parameters:
            self: the object itself
            symbol: the trading symbol
            lower_put_strike: the strike price for the lower put option
            upper_put_strike: the strike price for the upper put option
            lower_call_strike: the strike price for the lower call option
            upper_call_strike: the strike price for the upper call option
            quantity: the quantity of the options to trade
            asset_type: the type of asset (default is 'OPTION')
            order_type: the type of order (default is 'LIMIT')
            price: the price of the order (default is None)
        Returns:
            order_data: a dictionary containing the order details
        """
        order_data = {
            'orderType': order_type,
            'price': price,
            'orderStrategyType': 'SINGLE',
            'orderLegCollection': [
                {
                    'instruction': 'SELL_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {lower_put_strike} P',
                        'assetType': asset_type
                    }
                },
                {
                    'instruction': 'BUY_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {upper_put_strike} P',
                        'assetType': asset_type
                    }
                },
                {
                    'instruction': 'SELL_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {lower_call_strike} C',
                        'assetType': asset_type
                    }
                },
                {
                    'instruction': 'BUY_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {upper_call_strike} C',
                        'assetType': asset_type
                    }
                }
            ]
        }
        logger.info(f"Generated short iron condor order data for symbol: {symbol}")
        return order_data

    def iron_butterfly(self,  symbol, lower_put_strike, middle_strike, upper_call_strike, quantity, asset_type='OPTION', order_type='LIMIT', price=None):
        """
        Generate an iron butterfly order data dictionary.

        Args:
            symbol (str): The trading symbol.
            lower_put_strike (float): The strike price for the lower put option.
            middle_strike (float): The strike price for the middle strike.
            upper_call_strike (float): The strike price for the upper call option.
            quantity (int): The quantity of the options to trade.
            asset_type (str, optional): The type of asset (default is 'OPTION').
            order_type (str, optional): The type of order (default is 'LIMIT').
            price (float, optional): The price of the order (default is None).

        Returns:
            dict: A dictionary containing the order details.
        """
        order_data = {
            'orderType': order_type,
            'price': price,
            'orderStrategyType': 'SINGLE',
            'orderLegCollection': [
                {
                    'instruction': 'BUY_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {lower_put_strike} P',
                        'assetType': asset_type
                    }
                },
                {
                    'instruction': 'SELL_TO_OPEN',
                    'quantity': 2 * quantity,
                    'instrument': {
                        'symbol': f'{symbol} {middle_strike} C',
                        'assetType': asset_type
                    }
                },
                {
                    'instruction': 'BUY_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {upper_call_strike} C',
                        'assetType': asset_type
                    }
                }
            ]
        }
        logger.info(f"Generated iron butterfly order data for symbol: {symbol}")
        return order_data

    def iron_condor(self,  symbol, lower_put_strike, upper_put_strike, lower_call_strike, upper_call_strike, quantity, asset_type='OPTION', order_type='LIMIT', price=None):
        """
        A function to generate an iron condor order data dictionary.

        Args:
            self: the object itself
            symbol (str): the trading symbol
            lower_put_strike (float): the strike price for the lower put option
            upper_put_strike (float): the strike price for the upper put option
            lower_call_strike (float): the strike price for the lower call option
            upper_call_strike (float): the strike price for the upper call option
            quantity (int): the quantity of the options to trade
            asset_type (str, optional): the type of asset (default is 'OPTION')
            order_type (str, optional): the type of order (default is 'LIMIT')
            price (float, optional): the price of the order (default is None)

        Returns:
            dict: a dictionary containing the order details
        """
        order_data = {
            'orderType': order_type,
            'price': price,
            'orderStrategyType': 'SINGLE',
            'orderLegCollection': [
                {
                    'instruction': 'BUY_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {lower_put_strike} P',
                        'assetType': asset_type
                    }
                },
                {
                    'instruction': 'SELL_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {upper_put_strike} P',
                        'assetType': asset_type
                    }
                },
                {
                    'instruction': 'SELL_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {lower_call_strike} C',
                        'assetType': asset_type
                    }
                },
                {
                    'instruction': 'BUY_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {upper_call_strike} C',
                        'assetType': asset_type
                    }
                }
            ]
        }
        logger.info(f"Generated iron condor order data for symbol: {symbol}")
        return order_data

    def calendar_spread(self,  symbol, front_month_strike, back_month_strike, quantity, asset_type='OPTION', order_type='LIMIT', price=None):
        """
        Generates order data for a calendar spread strategy.
        
        Parameters:
            symbol (str): The symbol for the asset.
            front_month_strike (float): The strike price of the front month option.
            back_month_strike (float): The strike price of the back month option.
            quantity (int): The quantity of contracts.
            asset_type (str, optional): The type of asset. Defaults to 'OPTION'.
            order_type (str, optional): The type of order. Defaults to 'LIMIT'.
            price (float, optional): The price of the order. Defaults to None.
        
        Returns:
            dict: The order data for the calendar spread.
        """
        order_data = {
            'orderType': order_type,
            'price': price,
            'orderStrategyType': 'SINGLE',
            'orderLegCollection': [
                {
                    'instruction': 'SELL_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {front_month_strike} {self.get_month_code(front_month_strike)} C',
                        'assetType': asset_type
                    }
                },
                {
                    'instruction': 'BUY_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {back_month_strike} {self.get_month_code(back_month_strike)} C',
                        'assetType': asset_type
                    }
                }
            ]
        }
        logger.info(f"Generated calendar spread order data for symbol: {symbol}")
        return order_data

    def diagonal_spread(self,  symbol, front_month_strike, back_month_strike, quantity, asset_type='OPTION', order_type='LIMIT', price=None):
        """
        Generate a diagonal spread order for options with the specified parameters.

        Parameters:
            symbol (str): The symbol of the option.
            front_month_strike (float): The strike price for the front month option.
            back_month_strike (float): The strike price for the back month option.
            quantity (int): The quantity of options to trade.
            asset_type (str, optional): The type of asset (default is 'OPTION').
            order_type (str, optional): The type of order (default is 'LIMIT').
            price (float, optional): The price for the order.

        Returns:
            dict: The order data for the diagonal spread.
        """
        order_data = {
            'orderType': order_type,
            'price': price,
            'orderStrategyType': 'SINGLE',
            'orderLegCollection': [
                {
                    'instruction': 'SELL_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {front_month_strike} {self.get_month_code(front_month_strike)} C',
                        'assetType': asset_type
                    }
                },
                {
                    'instruction': 'BUY_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {back_month_strike} {self.get_month_code(back_month_strike)} C',
                        'assetType': asset_type
                    }
                }
            ]
        }
        logger.info(f"Generated diagonal spread order data for symbol: {symbol}")
        return order_data
    
    def diagonal_spread(self,  symbol, short_strike, short_expiration, long_strike, long_expiration, quantity, order_type='LIMIT', price=None):
        """
        Generate a diagonal spread order for options with the specified parameters.

        Parameters:
            symbol (str): The symbol of the option.
            short_strike (float): The strike price for the short option.
            short_expiration (str): The expiration date for the short option.
            long_strike (float): The strike price for the long option.
            long_expiration (str): The expiration date for the long option.
            quantity (int): The quantity of options to trade.
            order_type (str, optional): The type of order (default is 'LIMIT').
            price (float, optional): The price for the order.

        Returns:
            dict: The order data for the diagonal spread.
        """
        order_data = {
            'orderType': order_type,
            'price': price,
            'orderStrategyType': 'SINGLE',
            'orderLegCollection': [
                {
                    'instruction': 'SELL_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {short_strike} {short_expiration}',
                        'assetType': 'OPTION'
                    }
                },
                {
                    'instruction': 'BUY_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {long_strike} {long_expiration}',
                        'assetType': 'OPTION'
                    }
                }
            ]
        }
        logger.info(f"Generated diagonal spread order data for symbol: {symbol}")
        return order_data


    def get_month_code(self, date):
        """
        A method to convert a date into the appropriate option month code.

        Parameters:
            self: The Strategies object.
            date (datetime): The date to convert.

        Returns:
            str: The option month code.
        """
        # This method should convert a date into the appropriate option month code
        month = date.strftime("%m")
        month_codes = {
            '01': 'A',
            '02': 'B',
            '03': 'C',
            '04': 'D',
            '05': 'E',
            '06': 'F',
            '07': 'G',
            '08': 'H',
            '09': 'I',
            '10': 'J',
            '11': 'K',
            '12': 'L'
        }
        return month_codes[month]


    def straddle_strangle_swap(self,  symbol, straddle_strike, strangle_strike_1, strangle_strike_2, quantity, asset_type='OPTION', order_type='LIMIT', price=None):
        """
        A method to generate straddle, strangle, and swap order data for a given symbol.

        Parameters:
            self: The Strategies object.
            symbol (str): The symbol of the underlying asset.
            straddle_strike (float): The strike price for the straddle option.
            strangle_strike_1 (float): The strike price for the first leg of the strangle option.
            strangle_strike_2 (float): The strike price for the second leg of the strangle option.
            quantity (int): The quantity of options to buy or sell.
            asset_type (str): The type of the asset (default is 'OPTION').
            order_type (str): The type of the order (default is 'LIMIT').
            price (float): The price of the order.

        Returns:
            dict: The generated straddle, strangle, and swap order data.
        """
        order_data = {
            'orderType': order_type,
            'price': price,
            'orderStrategyType': 'SINGLE',
            'orderLegCollection': [
                {
                    'instruction': 'SELL_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {straddle_strike} C',
                        'assetType': asset_type
                    }
                },
                {
                    'instruction': 'SELL_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {straddle_strike} P',
                        'assetType': asset_type
                    }
                },
                {
                    'instruction': 'BUY_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {strangle_strike_1} C',
                        'assetType': asset_type
                    }
                },
                {
                    'instruction': 'BUY_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {strangle_strike_2} P',
                        'assetType': asset_type
                    }
                }
            ]
        }
        return order_data



    def strangle(self,  symbol, lower_strike, upper_strike, quantity, order_type='LIMIT', price=None):
        """
        A function to generate a strangle order data for a given symbol.

        Parameters:
            self: The Strategies object.
            symbol (str): The symbol of the underlying asset.
            lower_strike (float): The strike price for the lower option.
            upper_strike (float): The strike price for the upper option.
            quantity (int): The quantity of options to buy or sell.
            order_type (str): The type of the order (default is 'LIMIT').
            price (float): The price of the order (default is None).

        Returns:
            dict: The generated strangle order data.
        """
        order_data = {
            'orderType': order_type,
            'price': price,
            'orderStrategyType': 'SINGLE',
            'orderLegCollection': [
                {
                    'instruction': 'SELL_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {lower_strike} P',
                        'assetType': 'OPTION'
                    }
                },
                {
                    'instruction': 'SELL_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {upper_strike} C',
                        'assetType': 'OPTION'
                    }
                }
            ]
        }
        logger.info(f"Generated strangle order data for symbol: {symbol}")
        return order_data

    def iron_condor(self,  symbol, lower_put_strike, higher_put_strike, lower_call_strike, higher_call_strike, quantity, order_type='LIMIT', price=None):
        """
        A function to generate an iron condor order. 
        Parameters:
            self: the object itself
            symbol: the trading symbol
            lower_put_strike: the strike price for the lower put option
            higher_put_strike: the strike price for the higher put option
            lower_call_strike: the strike price for the lower call option
            higher_call_strike: the strike price for the higher call option
            quantity: the quantity of the options to trade
            order_type: the type of order (default is 'LIMIT')
            price: the price of the order (default is None)
        Returns:
            order_data: a dictionary containing the order details
        """
        order_data = {
            'orderType': order_type,
            'price': price,
            'orderStrategyType': 'SINGLE',
            'orderLegCollection': [
                {
                    'instruction': 'SELL_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {lower_put_strike} P',
                        'assetType': 'OPTION'
                    }
                },
                {
                    'instruction': 'BUY_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {higher_put_strike} P',
                        'assetType': 'OPTION'
                    }
                },
                {
                    'instruction': 'SELL_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {lower_call_strike} C',
                        'assetType': 'OPTION'
                    }
                },
                {
                    'instruction': 'BUY_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {higher_call_strike} C',
                        'assetType': 'OPTION'
                    }
                }
            ]
        }
        logger.info(f"Generated iron condor order data for symbol: {symbol}")
        return order_data

    def butterfly(self,symbol, lower_strike, middle_strike, upper_strike, quantity, order_type='LIMIT', price=None):
        """
        Generate a butterfly order data dictionary.

        Args:
            self: The instance of the class.
            symbol (str): The trading symbol.
            lower_strike (float): The lower strike price for the options.
            middle_strike (float): The middle strike price for the options.
            upper_strike (float): The upper strike price for the options.
            quantity (int): The quantity of the options to trade.
            order_type (str): The type of order (default is 'LIMIT').
            price (float, optional): The price of the order (default is None).

        Returns:
            dict: A dictionary containing the order details.
        """
        order_data = {
            'orderType': order_type,
            'price': price,
            'orderStrategyType': 'SINGLE',
            'orderLegCollection': [
                {
                    'instruction': 'BUY_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {lower_strike} C',
                        'assetType': 'OPTION'
                    }
                },
                {
                    'instruction': 'SELL_TO_OPEN',
                    'quantity': 2 * quantity,
                    'instrument': {
                        'symbol': f'{symbol} {middle_strike} C',
                        'assetType': 'OPTION'
                    }
                },
                {
                    'instruction': 'BUY_TO_OPEN',
                    'quantity': quantity,
                    'instrument': {
                        'symbol': f'{symbol} {upper_strike} C',
                        'assetType': 'OPTION'
                    }
                }
            ]
        }
        logger.info(f"Generated butterfly order data for symbol: {symbol}")
        return order_data

   