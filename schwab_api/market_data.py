import requests
import pandas as pd
import numpy as np
import json

class MarketData:
    def __init__(self, auth):
        self.auth = auth
        self.base_url = 'https://api.schwabapi.com/marketdata/v1'
        
    # Get the quotes for a single symbol
    def get_symbol_quotes(self, symbol, fields='quote, reference'):
        url = f"{self.base_url}/{symbol}/quotes"
        headers = self.auth.get_headers()
        params = {'symbol': symbol,
                  'fields': fields}
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        return pd.DataFrame(data)
    
    # Get the quotes for multiple symbols
    def get_quotes(self, symbols, fields='quote, reference', indicative=False):
        url = f"{self.base_url}/quotes"
        headers = self.auth.get_headers()
        params = {'symbol': ','.join(symbols),
                  fields: fields,
                  'indicative': str(indicative).lower()}
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        return pd.DataFrame(data)

    
    # Get the quotes for a symbol
    def get_option_chains(self, symbol, contract_type='CALL', strike_count=None, includeUnderlyingQuote=True, 
                        strategy ="ANALYTICAL", interval= 1, strike_price=None, 
                        range='ITM', fromDate=None, toDate=None, volatility=None, 
                        underlying_price=None, interest_rate=None, daysToExpire=None, 
                        expMonth=None, option_type=None, entillment="PP"):
        url = f"{self.base_url}/chains"
        headers = self.auth.get_headers()
        params = {'symbol': symbol,
                    'contractType': contract_type,
                    'strikeCount': strike_count,
                    'includeUnderlyingQuote': includeUnderlyingQuote,
                    'strategy': strategy,
                    'interval': interval,
                    'strike': strike_price,
                    'range': range,
                    'fromDate': fromDate,
                    'toDate': toDate,
                    'volatility': volatility,
                    'underlyingPrice': underlying_price,
                    'interestRate': interest_rate,
                    'daysToExpiration': daysToExpire,
                    'expMonth': expMonth,
                    'optionType': option_type,
                    'entitlement': entillment}
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        return pd.DataFrame(data)

    # Get the option expiration chains for a symbol
    def get_option_expiration_chain(self, symbol):
        url = f"{self.base_url}/expirationchain"
        param ={'symbol': symbol}
        headers = self.auth.get_headers()
        response = requests.get(url, headers=headers, params=param)
        response.raise_for_status()
        return response.json()


    # Get historical data for a symbol
    def get_historical_data(self, symbol, period_type='year', period=1, frequency_type='minute', 
                            frequency=1, start_date=None, end_date=None, needExtendedHoursData=False,
                            needPreviousClose=False):
        url = f"{self.base_url}/pricehistory"
        headers = self.auth.get_headers()
        params = {
            'symbol': symbol,
            'periodType': period_type,
            'period': period,
            'frequencyType': frequency_type,
            'frequency': frequency,
            'startDate': start_date,
            'endDate': end_date,
            'needExtendedHoursData': needExtendedHoursData,
            'needPreviousClose': needPreviousClose
        }
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data['candles'])
        df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
        return df


    # Get active gainers and losers
    def get_active_gainers_losers(self, index_symbol="$SPX", sort = "VOLUME", frequency = 5):
        url = f"{self.base_url}/movers/{index_symbol}"
        params = {
            'symbol_id': index_symbol,
            'sort': sort,
            'frequency': frequency
        }
        headers = self.auth.get_headers()
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()


    # Stream live data for a list of symbols
    def stream_live_data(self, symbols):
        url = f"{self.base_url}/stream"
        headers = self.auth.get_headers()
        params = {'symbols': ','.join(symbols)}
        response = requests.get(url, headers=headers, params=params, stream=True)
        response.raise_for_status()
        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode('utf-8'))
                yield pd.DataFrame([data])
    

    # Helper functions
    def _concatenate_symbols(self,string_list):
        result = ""
        for s in string_list:
            if s.startswith("$"):
                separator = "%24"
                s = s[1:]  # Remove the leading "$"
            else:
                separator = "%2"
            
            if result:
                result += separator
            result += s
        return result
    

    # Get market hours for all available markets
    def get_market_hours(self, date=None):
        url = f"{self.base_url}/markets"
        params = {
            'date': date
        }
        headers = self.auth.get_headers()
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()

    # Get market hours for a specific market
    def get_market_hours(self, market_id="option", date=None):
        url = f"{self.base_url}/markets/""
        params = {
            'market_id': market_id,
            'date': date
        }
        headers = self.auth.get_headers()
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    
    '''Get Get Instruments details by using different projections.
       Get more specific fundamental instrument 
       data by using fundamental as the projection.'''

    def get_instruments(self, symbol, projection="symbol-search"):
        url = f"{self.base_url}/instruments"
        params = {
            'symbol': symbol,
            'projection': projection
        }
        headers = self.auth.get_headers()
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    
    # Get basic instrument details by cusip
    def get_instrument_by_cusip(self, cusip):
        url = f"{self.base_url}/instruments/"
        params = {
            'cusip': cusip
        }
        headers = self.auth.get_headers()
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()