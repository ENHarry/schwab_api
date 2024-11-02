import requests
from datetime import datetime
import json
import logging
import websockets
import asyncio
import pandas as pd
from typing import Union
from functools import lru_cache
from schwab_api.helper import HelperFuncs
from schwab_api.urls import SchwabUrls


logger = logging.getLogger(__name__)
class MarketData():
    """
    Provides methods to retrieve market data.
    """

    def __init__(self, auth):
        """
        Initializes MarketData with authentication object.
        
        :param auth: SchwabAuth object for authentication
        """
        self.auth = auth
        self.urls = SchwabUrls()
        self.helper = HelperFuncs()
        

    def get_symbol_quote(self, symbol: str,
                         fields: Union[list, str] =['quote', 'reference']):
        """
        Retrieves quotes for a single symbol.
        
        :param symbol: Symbol to retrieve quotes for
        :param fields: Fields to include in the quote
        :return: DataFrame containing symbol quotes
        """
        fields = self.helper._validate_fields(fields)

        url = self.urls.get_symbol_quote_url(symbol)
        headers = self.auth.get_headers()
        params = {'fields': fields}
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            logger.info(f"Retrieved symbol quotes for {symbol}")
            return self.helper._parse_json_to_dataframe(data)
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred while fetching symbol quotes: {http_err}")
            raise SystemExit(f"HTTP error occurred while fetching symbol quotes: {http_err}")
        except Exception as err:
            logger.error(f"An error occurred while fetching symbol quotes: {err}")
            raise SystemExit(f"An error occurred while fetching symbol quotes: {err}")

    @lru_cache(maxsize=128)    
    def get_quotes(self, symbols: Union[list, str],
                   fields: Union[list, str] = 'quote, reference', indicative=False):
        """
        Retrieves quotes for multiple symbols.
        
        :param symbols: List of symbols to retrieve quotes for
        :param fields: Fields to include in the quotes
        :param indicative: Boolean indicating if indicative prices should be included
        :return: DataFrame containing quotes for multiple symbols
        """
        syms = self.helper._format_symbols(symbols=symbols)
        
        # Ensure fields are validated and converted to a string
        fields = self.helper._validate_fields(fields=fields)
        
        url = self.urls.get_quotes_url()
        headers = self.auth.get_headers()
        
        params = {
            'symbols': syms, 
            'fields': fields, 
            'indicative': str(indicative).lower()
        }
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            logger.info(f"Retrieved quotes for symbols: {syms}")
            return self.helper._parse_json_to_dataframe(data)
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred while fetching quotes: {http_err}")
            raise SystemExit(f"HTTP error occurred while fetching quotes: {http_err}")
        except Exception as err:
            logger.error(f"An error occurred while fetching quotes: {err}")
            raise SystemExit(f"An error occurred while fetching quotes: {err}")


    @lru_cache(maxsize=128)    
    def get_option_chains(self, symbol: str, contract_type: str, strike_count=None, 
                          includeUnderlyingQuote: bool =True, strategy=None, interval=None, 
                          strike_price=None, range=None, fromDate=None, toDate=None, volatility=None, 
                        underlying_price=None, interest_rate=None, daysToExpire=None, 
                        expMonth=None,option_type=None, entillment=None):
        """
        Retrieves option chains for a specific symbol.
        
        :param symbol: Symbol to retrieve option chains for
        :param contract_type: Type of contract ('CALL' or 'PUT')
        :param strike_count: Number of strikes to include
        :param includeUnderlyingQuote: Boolean indicating if the underlying quote should be included
        :param strategy: Strategy for the option chain
        :param interval: Interval for the option chain
        :param strike_price: Strike price for the option chain
        :param range: Range for the option chain
        :param fromDate: Start date for the option chain
        :param toDate: End date for the option chain
        :param volatility: Volatility for the option chain
        :param underlying_price: Underlying price for the option chain
        :param interest_rate: Interest rate for the option chain
        :param daysToExpire: Days to expiration for the option chain
        :param expMonth: Expiration month for the option chain
        :param option_type: Type of option
        :param entillment: Entitlement for the option chain
        :return: DataFrame containing option chains
        """
        url = self.urls.get_optionchains_url()
        headers = self.auth.get_headers()
        if strategy is not None:
            strategy = self.helper._validate_strategy(strategy=strategy)
        
        if range is not None:
            range = self.helper._validate_range(range=range)
        
        if contract_type is not None:
            contract_type = self.helper._validate_contractType(contractType=contract_type)

        if expMonth is not None:
            expMonth = self.helper._validate_month(month=expMonth)    

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
                    'entitlement': entillment
                    }
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            logger.info(f"Retrieved option chains for {symbol}")
            
            return self.helper._optionchain_to_dataframe(json_data=data)
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred while fetching option chains: {http_err}")
            raise SystemExit(f"HTTP error occurred while fetching option chains: {http_err}")
        except Exception as err:
            logger.error(f"An error occurred while fetching option chains: {err}")
            raise SystemExit(f"An error occurred while fetching option chains: {err}")


    @lru_cache(maxsize=128)
    def get_option_expiration_chain(self, symbol: str):
        """
        Retrieves option expiration chains for a symbol.
        
        :param symbol: Symbol to retrieve option expiration chains for
        :return: JSON response containing option expiration chains
        """
        url = self.urls.get_optionchain_expiry_url()
        param ={'symbol': symbol}
        headers = self.auth.get_headers()
        try:
            response = requests.get(url, headers=headers, params=param)
            response.raise_for_status()
            logger.info(f"Retrieved option expiration chain for {symbol}")
            data = response.json()['expirationList']
            return pd.DataFrame(data)
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred while fetching option expiration chain: {http_err}")
            raise SystemExit(f"HTTP error occurred while fetching option expiration chain: {http_err}")
        except Exception as err:
            logger.error(f"An error occurred while fetching option expiration chain: {err}")
            raise SystemExit(f"An error occurred while fetching option expiration chain: {err}")

    @lru_cache(maxsize=128)    
    def get_historical_data(self, symbol, period_type=None, period=None, frequency_type=None, 
                            frequency=None, start_date:Union[str, int] =None, end_date: Union[str, int]=None, needExtendedHoursData=False,
                            needPreviousClose=True):
        """
        Retrieves historical data for a symbol.
        
        :param symbol: Symbol to retrieve historical data for
        :param period_type: Type of period (e.g., 'year', 'month')
        :param period: Period for the historical data
        :param frequency_type: Frequency type for the historical data (e.g., 'minute', 'daily')
        :param frequency: Frequency for the historical data
        :param start_date: Start date for the historical data
        :param end_date: End date for the historical data
        :param needExtendedHoursData: Boolean indicating if extended hours data is needed
        :param needPreviousClose: Boolean indicating if previous close data is needed
        :return: DataFrame containing historical data
        """
        url = self.urls.get_pricehistory_url()
        headers = self.auth.get_headers()
        if period_type is not None:
            period_type = self.helper._validate_periodType(periodType=period_type)
        
        if frequency_type is not None and period_type is not None:
            frequency_type = self.helper._validate_frequencyType(frequencyType=frequency_type,
                                                                 periodType=period_type)
        elif frequency_type is not None and period_type is None:
            raise ValueError("If 'frequency_type' is provided, 'period_type' must also be provided.")
        
        if period is not None and period_type is not None:
            period = self.helper._validate_period(period=period, periodType=period_type)
        elif period is not None and period_type is None:
            raise ValueError("If 'period' is provided, 'period_type' must also be provided.")
        
        if frequency is not None and frequency_type is not None:
            frequency = self.helper._validate_frequency(frequency=frequency, 
                                                        frequencyType=frequency_type, periodType=period_type)
        elif frequency is not None and frequency_type is None:
            raise ValueError("If 'frequency' is provided, 'frequency_type' must also be provided.")
        
        if start_date is not None:
            start_date = self.helper._date_format(date=start_date)
        if end_date is not None:
            end_date = self.helper._date_format(date=end_date)

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


        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            print(data)
            df = pd.DataFrame(data['candles'])
            """df['date'] = datetime.fromtimestamp(df['datetime']).strftime("%Y-%m-%d")
            df['time'] = datetime.fromtimestamp(df['datetime']).strftime("%H:%M:%S")
            df['previousClose'] = data['previousClose'].astype(float)
            df['symbol'] = data['symbol']
            df['previousCloseDate'] = data['previousCloseDate'].astype('datetime64[ns]')"""
            logger.info(f"Retrieved historical data for {symbol}")
            return df
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred while fetching historical data: {http_err}")
            raise SystemExit(f"HTTP error occurred while fetching historical data: {http_err}")
        except Exception as err:
            logger.error(f"An error occurred while fetching historical data: {err}")
            raise SystemExit(f"An error occurred while fetching historical data: {err}") 
        
    
    @lru_cache(maxsize=128)    
    def get_active_gainers_losers(self, index_symbol: str = "$SPX", sort = "VOLUME", frequency = 5):
        """
        Retrieves active gainers and losers for a specified index.
        
        :param index_symbol: Symbol of the index (e.g., '$SPX')
        :param sort: Sort criteria (e.g., 'VOLUME')
        :param frequency: Frequency of the data
        :return: JSON response containing active gainers and losers
        """
        url = self.urls.get_movers_url(index_symbol)
        params = {
            'symbol_id': self.helper._validate_indexSymbol(index_symbol),
            'sort': self.helper._validate_sort(sort),
            'frequency': self.helper._validate_history_frequency(frequency)
        }
        headers = self.auth.get_headers()
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            logger.info(f"Retrieved active gainers and losers for {index_symbol}")
            data = response.json()['screeners']
            return pd.DataFrame(data)
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred while fetching active gainers/losers: {http_err}")
            raise SystemExit(f"HTTP error occurred while fetching active gainers/losers: {http_err}")
        except Exception as err:
            logger.error(f"An error occurred while fetching active gainers/losers: {err}")
            raise SystemExit(f"An error occurred while fetching active gainers/losers: {err}")

    def stream_live_data(self, symbols):
        """
        Streams live data for a list of symbols.
        
        :param symbols: List of symbols to stream live data for
        :yield: DataFrame containing live data for each symbol
        """
        url = self.urls.get_livedata_url()
        headers = self.auth.get_headers()
        params = {'symbols': ','.join(symbols)}
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    data = json.loads(line.decode('utf-8'))
                    logger.info(f"Streaming live data for symbols: {', '.join(symbols)}")
                    yield self.helper._parse_json_to_dataframe([data])
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred while streaming live data: {http_err}")
            raise SystemExit(f"HTTP error occurred while streaming live data: {http_err}")
        except Exception as err:
            logger.error(f"An error occurred while streaming live data: {err}")
            raise SystemExit(f"An error occurred while streaming live data: {err}")

    async def stream_real_time_data(self, symbols):
        """
        Streams real-time data using WebSocket for a list of symbols.
        """
        async with websockets.connect(self.urls.get_livestream_url()) as websocket:
            subscribe_message = json.dumps({
                "action": "subscribe",
                "symbols": symbols
            })
            await websocket.send(subscribe_message)
            logger.info(f"Subscribed to real-time data for symbols: {', '.join(symbols)}")
            async for message in websocket:
                data = json.loads(message)
                logger.info(f"Received real-time data: {data}")
                yield self.helper._parse_json_to_dataframe(data)

    def run_stream(self, symbols):
        """
        Runs the real-time data stream using asyncio.
        """
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(self.stream_real_time_data(symbols))
        finally:
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()

    def get_all_market_hours(self, date: str =None):
        """
        Retrieves market hours for all available markets.
        
        :param date: Date for which to retrieve market hours
        :return: JSON response containing market hours
        """
        url = self.urls.get_markethours_url()
        params = {
            'date': date
        }
        headers = self.auth.get_headers()
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            logger.info(f"Retrieved market hours for all available markets")
            return self.helper._parse_json_to_dataframe(response.json())
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred while fetching market hours: {http_err}")
            raise SystemExit(f"HTTP error occurred while fetching market hours: {http_err}")
        except Exception as err:
            logger.error(f"An error occurred while fetching market hours: {err}")
            raise SystemExit(f"An error occurred while fetching market hours: {err}")

    def get_market_hours(self, market_id="option", date=None):
        """
        Retrieves market hours for a specific market.
        
        :param market_id: ID of the market
        :param date: Date for which to retrieve market hours
        :return: JSON response containing market hours
        """
        url = self.urls.get_markethours_url()
        params = {
            'market_id': self.helper._validate_markets(market_id),
            'date': date
        }
        headers = self.auth.get_headers()
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            logger.info(f"Retrieved market hours for market {market_id}")
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred while fetching market hours: {http_err}")
            raise SystemExit(f"HTTP error occurred while fetching market hours: {http_err}")
        except Exception as err:
            logger.error(f"An error occurred while fetching market hours: {err}")
            raise SystemExit(f"An error occurred while fetching market hours: {err}")

    def get_instruments(self, symbol, projection="symbol-search"):
        """
        Retrieves instrument details using different projections.
        
        :param symbol: Symbol to retrieve instruments for
        :param projection: Projection type (e.g., 'symbol-search', 'fundamental')
        :return: JSON response containing instrument details
        """
        url = self.urls.get_instruments_url()
        params = {
            'symbol': symbol,
            'projection': projection
        }
        headers = self.auth.get_headers()
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            logger.info(f"Retrieved instrument details for {symbol}")
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred while fetching instruments: {http_err}")
            raise SystemExit(f"HTTP error occurred while fetching instruments: {http_err}")
        except Exception as err:
            logger.error(f"An error occurred while fetching instruments: {err}")
            raise SystemExit(f"An error occurred while fetching instruments: {err}")

    def get_instrument_by_cusip(self, cusip):
        """
        Retrieves basic instrument details by CUSIP.
        
        :param cusip: CUSIP of the instrument
        :return: JSON response containing instrument details
        """
        url = self.urls.get_instruments_url()
        params = {
            'cusip': cusip
        }
        headers = self.auth.get_headers()
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            logger.info(f"Retrieved instrument details for CUSIP {cusip}")
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred while fetching instrument by CUSIP: {http_err}")
            raise SystemExit(f"HTTP error occurred while fetching instrument by CUSIP: {http_err}")
        except Exception as err:
            logger.error(f"An error occurred while fetching instrument by CUSIP: {err}")
            raise SystemExit(f"An error occurred while fetching instrument by CUSIP: {err}")

    