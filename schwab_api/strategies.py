class Strategies:
    def __init__(self, auth):
        self.auth = auth
        self.strategies_list = [
            'bear_call', 'bear_put', 'bull_call', 'bull_put', 'covered_call',
            'long_call_butterfly', 'long_call_condor', 'long_put_condor',
            'long_straddle', 'long_strangle', 'married_put',
            'protective_collar', 'short_call_butterfly', 'short_call_condor',
            'short_iron_condor', 'straddle_strangle_swap', 'iron_butterfly',
            'iron_condor', 'calendar_spread', 'diagonal_spread'
        ]

    def existing_strategies(self):
        return self.strategies_list

    def bear_call(self, symbol, short_call_strike, long_call_strike, quantity, asset_type='OPTION', order_type='LIMIT', price=None):
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
        return order_data

    def bear_put(self,  symbol, short_put_strike, long_put_strike, quantity, asset_type='OPTION', order_type='LIMIT', price=None):
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
        return order_data

    def bull_call(self,  symbol, long_call_strike, short_call_strike, quantity, asset_type='OPTION', order_type='LIMIT', price=None):
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
        return order_data

    def bull_put(self,  symbol, long_put_strike, short_put_strike, quantity, asset_type='OPTION', order_type='LIMIT', price=None):
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
        return order_data

    def covered_call(self,  symbol, quantity, call_strike, stock_quantity, asset_type='OPTION', order_type='LIMIT', price=None):
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
        return order_data

    def long_call_butterfly(self,  symbol, lower_strike, middle_strike, upper_strike, quantity, asset_type='OPTION', order_type='LIMIT', price=None):
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
        return order_data

    def long_call_condor(self, symbol, lower_strike, lower_middle_strike, upper_middle_strike, upper_strike, quantity, asset_type='OPTION', order_type='LIMIT', price=None):
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
        return order_data

    def long_put_condor(self, account_id, symbol, lower_strike, lower_middle_strike, upper_middle_strike, upper_strike, quantity, asset_type='OPTION', order_type='LIMIT', price=None):
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
        return order_data

    def long_straddle(self, account_id, symbol, quantity, strike_price, asset_type='OPTION', order_type='LIMIT', price=None):
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
        return order_data

    def long_strangle(self, account_id, symbol, quantity, call_strike, put_strike, asset_type='OPTION', order_type='LIMIT', price=None):
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
        return order_data

    def married_put(self, account_id, symbol, quantity, put_strike, stock_quantity, asset_type='OPTION', order_type='LIMIT', price=None):
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
        return order_data

    def protective_collar(self, account_id, symbol, quantity, put_strike, call_strike, stock_quantity, asset_type='OPTION', order_type='LIMIT', price=None):
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
        return order_data

    def short_call_butterfly(self, account_id, symbol, lower_strike, middle_strike, upper_strike, quantity, asset_type='OPTION', order_type='LIMIT', price=None):
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
        return order_data

    def short_call_condor(self, account_id, symbol, lower_strike, lower_middle_strike, upper_middle_strike, upper_strike, quantity, asset_type='OPTION', order_type='LIMIT', price=None):
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
        return order_data

    def short_iron_condor(self, account_id, symbol, lower_put_strike, upper_put_strike, lower_call_strike, upper_call_strike, quantity, asset_type='OPTION', order_type='LIMIT', price=None):
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
        return order_data

    def iron_butterfly(self, account_id, symbol, lower_put_strike, middle_strike, upper_call_strike, quantity, asset_type='OPTION', order_type='LIMIT', price=None):
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
        return order_data

    def iron_condor(self, account_id, symbol, lower_put_strike, upper_put_strike, lower_call_strike, upper_call_strike, quantity, asset_type='OPTION', order_type='LIMIT', price=None):
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
        return order_data

    def calendar_spread(self, account_id, symbol, front_month_strike, back_month_strike, quantity, asset_type='OPTION', order_type='LIMIT', price=None):
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
        return order_data

    def diagonal_spread(self, account_id, symbol, front_month_strike, back_month_strike, quantity, asset_type='OPTION', order_type='LIMIT', price=None):
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
        return order_data

    def get_month_code(self, date):
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


    def straddle_strangle_swap(self, account_id, symbol, straddle_strike, strangle_strike_1, strangle_strike_2, quantity, asset_type='OPTION', order_type='LIMIT', price=None):
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
