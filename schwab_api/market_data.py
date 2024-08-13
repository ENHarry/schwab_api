import requests
import pandas as pd
import json
import logging
import websockets
import asyncio
from typing import Union
from functools import lru_cache
from schwab_api.helper import HelperFuncs

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
        self.base_url = 'https://api.schwabapi.com/marketdata/v1'
        self.websocket_url = 'wss://api.schwabapi.com/marketdata/v1/stream'
        

    def get_symbol_quote(self, symbol: str, fields: Union[list, str] =['quote', 'reference']):
        """
        Retrieves quotes for a single symbol.
        
        :param symbol: Symbol to retrieve quotes for
        :param fields: Fields to include in the quote
        :return: DataFrame containing symbol quotes
        """
        fields = HelperFuncs._validate_fields(fields)

        url = f"{self.base_url}/{symbol}/quotes"
        headers = self.auth.get_headers()
        params = {'fields': fields}
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            logger.info(f"Retrieved symbol quotes for {symbol}")
            return HelperFuncs._parse_json_to_dataframe(data)
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred while fetching symbol quotes: {http_err}")
            raise SystemExit(f"HTTP error occurred while fetching symbol quotes: {http_err}")
        except Exception as err:
            logger.error(f"An error occurred while fetching symbol quotes: {err}")
            raise SystemExit(f"An error occurred while fetching symbol quotes: {err}")

    @lru_cache(maxsize=128)    
    def get_quotes(self, symbols: Union[list, str], fields: Union[list, str] ='quote, reference', indicative=False):
        """
        Retrieves quotes for multiple symbols.
        
        :param symbols: List of symbols to retrieve quotes for
        :param fields: Fields to include in the quotes
        :param indicative: Boolean indicating if indicative prices should be included
        :return: DataFrame containing quotes for multiple symbols
        """
        url = f"{self.base_url}/quotes"
        headers = self.auth.get_headers()
        fields = HelperFuncs._validate_fields(fields)
        symbols = HelperFuncs._format_symbols(symbols)

        params = {'symbols': symbols, 
                  'fields': fields, 
                  'indicative': str(indicative).lower()}
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            logger.info(f"Retrieved quotes for symbols: {symbols}")
            return HelperFuncs._parse_json_to_dataframe(data)
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred while fetching quotes: {http_err}")
            raise SystemExit(f"HTTP error occurred while fetching quotes: {http_err}")
        except Exception as err:
            logger.error(f"An error occurred while fetching quotes: {err}")
            raise SystemExit(f"An error occurred while fetching quotes: {err}")

    @lru_cache(maxsize=128)    
    def get_option_chains(self, symbol: str, contract_type: str, strike_count=None, includeUnderlyingQuote=True, 
                        strategy=None, interval=None, strike_price=None, 
                        range=None, fromDate=None, toDate=None, volatility=None, 
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
        url = f"{self.base_url}/chains"
        headers = self.auth.get_headers()
        if strategy is not None:
            strategy = HelperFuncs._validate_strategy(strategy=strategy)
        
        if range is not None:
            range = HelperFuncs._validate_range(range=range)
        
        if contract_type is not None:
            contract_type = HelperFuncs._validate_contractType(contractType=contract_type)

        if expMonth is not None:
            expMonth = HelperFuncs._validate_month(expMonth)    

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
            return HelperFuncs._parse_json_to_dataframe(data)
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred while fetching option chains: {http_err}")
            raise SystemExit(f"HTTP error occurred while fetching option chains: {http_err}")
        except Exception as err:
            logger.error(f"An error occurred while fetching option chains: {err}")
            raise SystemExit(f"An error occurred while fetching option chains: {err}")

    @lru_cache(maxsize=128)
    def get_option_expiration_chain(self, symbol):
        """
        Retrieves option expiration chains for a symbol.
        
        :param symbol: Symbol to retrieve option expiration chains for
        :return: JSON response containing option expiration chains
        """
        url = f"{self.base_url}/expirationchain"
        param ={'symbol': symbol}
        headers = self.auth.get_headers()
        try:
            response = requests.get(url, headers=headers, params=param)
            response.raise_for_status()
            logger.info(f"Retrieved option expiration chain for {symbol}")
            return HelperFuncs._parse_json_to_dataframe(response.json())
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred while fetching option expiration chain: {http_err}")
            raise SystemExit(f"HTTP error occurred while fetching option expiration chain: {http_err}")
        except Exception as err:
            logger.error(f"An error occurred while fetching option expiration chain: {err}")
            raise SystemExit(f"An error occurred while fetching option expiration chain: {err}")

    @lru_cache(maxsize=128)    
    def get_historical_data(self, symbol, period_type=None, period=None, frequency_type=None, 
                            frequency=None, start_date=None, end_date=None, needExtendedHoursData=False,
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
        url = f"{self.base_url}/pricehistory"
        headers = self.auth.get_headers()
        if period_type is not None:
            period_type = HelperFuncs._validate_period_type(period_type)
        
        if frequency_type is not None and period_type is not None:
            frequency_type = HelperFuncs._validate_frequency_type(frequency_type)
        elif frequency_type is not None and period_type is None:
            raise ValueError("If 'frequency_type' is provided, 'period_type' must also be provided.")
        
        if period is not None and period_type is not None:
            period = HelperFuncs._validate_period(period)
        elif period is not None and period_type is None:
            raise ValueError("If 'period' is provided, 'period_type' must also be provided.")
        
        if frequency is not None and frequency_type is not None:
            frequency = HelperFuncs._validate_frequency(frequency)
        elif frequency is not None and frequency_type is None:
            raise ValueError("If 'frequency' is provided, 'frequency_type' must also be provided.")
        
        if start_date is not None:
            start_date = HelperFuncs._validate_date(start_date)
        if end_date is not None:
            end_date = HelperFuncs._validate_date(end_date)

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
            df = HelperFuncs._parse_json_to_dataframe(data['candles'])
            df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
            logger.info(f"Retrieved historical data for {symbol}")
            return df
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred while fetching historical data: {http_err}")
            raise SystemExit(f"HTTP error occurred while fetching historical data: {http_err}")
        except Exception as err:
            logger.error(f"An error occurred while fetching historical data: {err}")
            raise SystemExit(f"An error occurred while fetching historical data: {err}") 
        
    
    @lru_cache(maxsize=128)    
    def get_active_gainers_losers(self, index_symbol="$SPX", sort = "VOLUME", frequency = 5):
        """
        Retrieves active gainers and losers for a specified index.
        
        :param index_symbol: Symbol of the index (e.g., '$SPX')
        :param sort: Sort criteria (e.g., 'VOLUME')
        :param frequency: Frequency of the data
        :return: JSON response containing active gainers and losers
        """
        url = f"{self.base_url}/movers/{index_symbol}"
        params = {
            'symbol_id': index_symbol,
            'sort': sort,
            'frequency': frequency
        }
        headers = self.auth.get_headers()
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            logger.info(f"Retrieved active gainers and losers for {index_symbol}")
            return HelperFuncs._parse_json_to_dataframe(response.json())
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
        url = f"{self.base_url}/stream"
        headers = self.auth.get_headers()
        params = {'symbols': ','.join(symbols)}
        try:
            response = requests.get(url, headers=headers, params=params, stream=True)
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    data = json.loads(line.decode('utf-8'))
                    logger.info(f"Streaming live data for symbols: {', '.join(symbols)}")
                    yield HelperFuncs._parse_json_to_dataframe([data])
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
        async with websockets.connect(self.websocket_url) as websocket:
            subscribe_message = json.dumps({
                "action": "subscribe",
                "symbols": symbols
            })
            await websocket.send(subscribe_message)
            logger.info(f"Subscribed to real-time data for symbols: {', '.join(symbols)}")
            async for message in websocket:
                data = json.loads(message)
                logger.info(f"Received real-time data: {data}")
                yield HelperFuncs._parse_json_to_dataframe(data)

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

    def get_all_market_hours(self, date=None):
        """
        Retrieves market hours for all available markets.
        
        :param date: Date for which to retrieve market hours
        :return: JSON response containing market hours
        """
        url = f"{self.base_url}/markets"
        params = {
            'date': date
        }
        headers = self.auth.get_headers()
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            logger.info(f"Retrieved market hours for all available markets")
            return HelperFuncs._parse_json_to_dataframe(response.json())
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
        url = f"{self.base_url}/markets/"
        params = {
            'market_id': market_id,
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
        url = f"{self.base_url}/instruments"
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
        url = f"{self.base_url}/instruments/"
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

    