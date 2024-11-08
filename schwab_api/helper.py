import datetime
import pandas as pd
from typing import Union


class HelperFuncs:
    def __init__(self):
        pass
        

    @staticmethod
    def _validate_fields(fields: Union[list, str]):
        """
        Validates the fields parameter.
        
        :param fields: Fields to include in the response
        :return: None
        """
        valid_fields = ['quote', 'fundamental', 'extended', 'reference', 'regular']

        if isinstance(fields, str):
            fields = fields.split(',')
            for field in fields:
                if field.strip() not in valid_fields:
                    raise ValueError("Fields parameter must be one of: " + ", ".join(valid_fields))
            new_fields = ','.join(fields).replace(' ', '')
            return new_fields
        elif isinstance(fields, list):
            for field in fields:
                if field.strip() not in valid_fields:
                    raise ValueError("Fields parameter must be one of: " + ", ".join(valid_fields))
            new_fields = ','.join(fields).replace(' ', '')
            return new_fields      
        
        
    @staticmethod
    def _format_symbols(symbols):
        """
        Formats the symbols parameter.
        
        :param symbols: List of symbols to retrieve quotes for
        :return: Formatted symbols string
        """
        if isinstance(symbols, str):
            symb = symbols.replace(' ', '')
            return symb
        elif isinstance(symbols, list):
            if not all(isinstance(item, str) for item in symbols):
                raise ValueError("All items in the symbols list must be strings")
            print("Converting the Symbols list to string: ", symbols)
            symb = ','.join(symbols).replace(' ', '')
            return symb
        else:
            raise ValueError("Symbols parameter must be a string or list of strings")

    
    @staticmethod 
    def _validate_contractType(contractType: str):
        """
        Validates the contractType parameter.
        
        :param contractType: Contract type to retrieve quotes for
        :return: None
        """
        valid_contractTypes = ['ALL', 'CALL', 'PUT']
        if contractType not in valid_contractTypes:
            raise ValueError("Contract type parameter must be one of: " + ", ".join(valid_contractTypes))
        else:
            return contractType
    @staticmethod  
    def _validate_strategy(strategy: str):
        """
        Validates the strategy parameter.
        
        :param strategy: allows the use of volatility, underlyingPrice, interestRate, 
        and daysToExpiration params to calculate theoretical values for an Option Chain Strategy.
        """
        valid_strategies = ['SINGLE','ANALYTICAL','COVERED','VERTICAL',
                            'CALENDAR', 'STRANGLE','STRADDLE','BUTTERFLY',
                            'CONDOR', 'DIAGONAL', 'COLLAR', 'ROLL']
        if strategy not in valid_strategies:
            raise ValueError("Strategy parameter must be one of: " + ", ".join(valid_strategies))
        else:
            return strategy
    @staticmethod  
    def _validate_assetType(assetType: str):
        """
        Validates the assetType parameter.
        
        :param assetType: Asset type to retrieve quotes for
        :return: None
        """
        valid_assetTypes = ['BOND','FOREX','EQUITY','OPTION','FUTURE', 
                            'FUTURES_OPTION','INDEX','MUTUAL_FUND']
        if assetType not in valid_assetTypes:
            raise ValueError("Asset type parameter must be one of: " + ", ".join(valid_assetTypes))
        else:
            return assetType  

    @staticmethod
    def _validate_abbr_contractType(contractType: str):
        """
        Validates the contractType parameter.
        
        :param contractType: Contract type to retrieve quotes for
        :return: None
        """
        valid_contractTypes = ['ALL', 'CALL', 'PUT']
        if contractType not in valid_contractTypes:
            raise ValueError("Contract type parameter must be one of: " + ", ".join(valid_contractTypes))
        else:
            if contractType == 'ALL':
                contractType = 'C,P'
            elif contractType == 'CALL':
                contractType = 'C'
            elif contractType == 'PUT':
                contractType = 'P'
            return contractType 
    @staticmethod
    def _validate_range(range: str):
        """
        Validates the range parameter.
        
        :param range: Range for the option chain
        :return: None
        """
        valid_ranges = ['ITM', 'NTM', 'OTM', 'ATM', 'SAK', 'SBK', 'SNK', 'ALL']
        if range not in valid_ranges:
            raise ValueError("Range parameter must be one of: " + ", ".join(valid_ranges))
        else:
            return range

    @staticmethod
    def _validate_periodType(periodType: str):
        """
        Validates the periodType parameter.
        
        :param periodType: The chart period being requested.
        """
        valid_periodTypes = ['day', 'month', 'year', 'ytd']
        if periodType not in valid_periodTypes:
            raise ValueError("Period type parameter must be one of: " + ", ".join(valid_periodTypes))
        else:
            return periodType

    @staticmethod       
    def _validate_period(periodType,period: int):
        """
        Validates the period parameter.
        
        :param period: The number of chart period types.
        """
        day_valid_values = [1, 2, 3, 4, 5, 10]
        month_valid_values = [1, 2, 3, 6]
        year_valid_values = [1, 2, 3, 5, 10, 15, 20]
        ytd_valid_value = [1]
        periodType = HelperFuncs._validate_periodType(periodType=periodType)
        if periodType == 'day' and period not in day_valid_values:
            raise ValueError("Due to your periodType being 'day', the Period parameter must be one of: " + ", ".join(day_valid_values))
        elif periodType == 'month' and period not in month_valid_values:
            raise ValueError("Due to your periodType being 'month', the Period parameter must be one of: " + ", ".join(month_valid_values))
        elif periodType == 'year' and period not in year_valid_values:
            raise ValueError("Due to your periodType being 'year', the Period parameter must be one of: " + ", ".join(year_valid_values))
        elif periodType == 'ytd' and period not in ytd_valid_value:
            raise ValueError("Due to your periodType being 'ytd', the Period parameter must be one of: " + ", ".join(ytd_valid_value))
        else:
            return period
        
    @staticmethod
    def _validate_frequencyType( frequencyType: str, periodType):
        """
        Validates the frequencyType parameter.
        
        :param frequencyType: The timefrequency with which a new candle is formed.
        """
        day_valid_value = ['minute'] # valid values is minute
        month_valid_values = ['daily', 'weekly']
        year_valid_values = ['daily', 'weekly', 'monthly']
        ytd_valid_values = ['daily', 'weekly']

        periodType = HelperFuncs._validate_periodType(periodType=periodType)

        if periodType == 'day' and frequencyType not in day_valid_value:
            raise ValueError("Due to your periodType being 'day', the FrequencyType parameter must be one of: " + ", ".join(day_valid_value))
        elif periodType == 'month' and frequencyType not in month_valid_values:
            raise ValueError("Due to your periodType being 'month', the FrequencyType parameter must be one of: " + ", ".join(month_valid_values))
        elif periodType == 'year' and frequencyType not in year_valid_values:
            raise ValueError("Due to your periodType being 'year', the FrequencyType parameter must be one of: " + ", ".join(year_valid_values))
        elif periodType == 'ytd' and frequencyType not in ytd_valid_values:
            raise ValueError("Due to your periodType being 'ytd', the FrequencyType parameter must be one of: " + ", ".join(ytd_valid_values))
        else:
            return frequencyType


    @staticmethod
    def _validate_frequency(frequencyType, frequency: int, periodType):
        """
        Validates the frequency parameter.
        """    
        frequencyType = HelperFuncs._validate_frequencyType(frequencyType=frequencyType, periodType=periodType)
        
        minute_valid_values = [1, 5, 10, 15, 30]
        daily_valid_value = [1]
        weekly_valid_value = [1]
        monthly_valid_value = [1]
        
        if frequencyType == 'minute' and frequency not in minute_valid_values:
            raise ValueError("Due to your frequencyType being 'minute', the Frequency parameter must be one of: " + ", ".join(minute_valid_values))
        elif frequencyType == 'daily' and frequency not in daily_valid_value:
            raise ValueError("Due to your frequencyType being 'daily', the Frequency parameter must be one of: " + ", ".join(daily_valid_value))
        elif frequencyType == 'weekly' and frequency not in weekly_valid_value:
            raise ValueError("Due to your frequencyType being 'weekly', the Frequency parameter must be one of: " + ", ".join(weekly_valid_value))
        elif frequencyType == 'monthly' and frequency not in monthly_valid_value:
            raise ValueError("Due to your frequencyType being 'monthly', the Frequency parameter must be one of: " + ", ".join(monthly_valid_value))
        else:
            return frequency    

    @staticmethod
    def _date_format(date: Union[int, str]):
        """
        Formats the date parameter.
        """
        if isinstance(date, int):
            return date
        ndate = datetime.datetime.strptime(date, "%Y-%m-%d")
        return int(ndate.timestamp())
    
    @staticmethod
    def _parse_json_to_dataframe(json_file):
    
        # Create a list to store all rows of data
        rows = []
        
        # Iterate over each key (symbol) in the JSON data
        for symbol, details in json_file.items():
            # Flatten the nested structure for the 'quote' and 'reference' keys
            flattened_data = {**details['quote'], **details['reference']}
            
            # Add the symbol to the data
            flattened_data['symbol'] = symbol
            
            # Append to the list of rows
            rows.append(flattened_data)
        
        # Convert the list of rows to a DataFrame
        df = pd.DataFrame(rows)
        
        return df
    
    @staticmethod
    def _validate_month(month: Union[int, str]):
        """
        Validates the month parameter.
        """

        if isinstance(month, int) and month not in range(1, 13):
            raise ValueError("The Month parameter must be an integer between 1 and 12.")
        elif isinstance(month, str):
            if len(month) > 3:
                month = month[:3].upper()
                return month
            elif len(month) == 3:
                month = month.upper()
                return month    
        elif isinstance(month, int) in range(1, 13):
            mnth_str = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 
                        'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
            mnth_int = list(range(1, 13))
            mnth_dict = dict(zip(mnth_int, mnth_str))
            month = mnth_dict[month]
            return month
        else:   
            month = 'ALL' 
            return month 
        

    '''@staticmethod
    def _flatten_json(self, nested_json, parent_key='', sep='_'):
        """
        Flatten a nested JSON object into a flat dictionary.
        """
        items = []
        for k, v in nested_json.items():
            new_key = f'{parent_key}{sep}{k}' if parent_key else k
            if isinstance(v, dict):
                items.extend(self._flatten_json(nested_json=v, parent_key=new_key, sep=sep).items())
            elif isinstance(v, list):
                if all(isinstance(i, dict) for i in v):
                    for idx, item in enumerate(v):
                        items.extend(self._flatten_json(nested_json=item, parent_key=f'{new_key}_{idx}', sep=sep).items())
                else:
                    items.append((new_key, v))
            else:
                items.append((new_key, v))
        return dict(items)'''

    @staticmethod
    def _flatten_json(nested_json, parent_key='', sep='_'):
        """
        Flattens a nested JSON object into a flat dictionary.
        
        :param nested_json: The JSON object to flatten
        :param parent_key: The base key for the flattened keys
        :param sep: The separator between keys
        :return: A flattened dictionary
        """
        items = []
        for k, v in nested_json.items():
            new_key = f'{parent_key}{sep}{k}' if parent_key else k
            if isinstance(v, dict):
                items.extend(HelperFuncs._flatten_json(v, new_key, sep=sep).items())
            elif isinstance(v, list):
                if all(isinstance(i, dict) for i in v):
                    for idx, item in enumerate(v):
                        items.extend(HelperFuncs._flatten_json(item, f'{new_key}_{idx}', sep=sep).items())
                else:
                    items.append((new_key, v))
            else:
                items.append((new_key, v))
        return dict(items)

    @staticmethod
    def _extract_specific_keys(option_data):
        """
        Extract specific keys and their values from the option data.
        """
        specific_keys = [
            'bid', 'ask', 'last', 'mark', 'bidSize', 'askSize', 'closePrice', 'totalVolume',
            'tradeTimeInLong', 'quoteTimeInLong', 'volatility', 'delta', 'timeValue',
            'theoreticalOptionValue', 'theoreticalVolatility', 'intrinsicValue', 'extrinsicValue',
            'inTheMoney'
        ]
        extracted_data = {key: option_data.get(key) for key in specific_keys}
        return extracted_data

    
    def _optionchain_to_dataframe(self,json_data):
        # Load the JSON data from the file
        

        # Initialize a list to store all rows for the dataframe
        rows = []

        # Flatten the "underlying" data
        underlying_data = self._flatten_json(json_data.get("underlying", {}))

        # Check and process callExpDateMap if present
        if "callExpDateMap" in json_data:
            call_exp_date_map = json_data["callExpDateMap"]
            for exp_date, strikes in call_exp_date_map.items():
                for  strike_price, options_list in strikes.items():
                    for option in options_list:
                        row = underlying_data.copy()
                        row.update(self._flatten_json(option))
                        row.update(self._extract_specific_keys(option))
                        row['exp_date_type'] = "CALL"
                        row['exp_date'] = exp_date
                        rows.append(row)
        
        # Check and process putExpDateMap if present
        if "putExpDateMap" in json_data:
            put_exp_date_map = json_data["putExpDateMap"]
            for exp_date, strikes in put_exp_date_map.items():
                for strike_price, options_list in strikes.items():
                    for option in options_list:
                        row = underlying_data.copy()
                        row.update(self._flatten_json(option))
                        row.update(self._extract_specific_keys(option))
                        row['exp_date_type'] = "PUT"
                        row['exp_date'] = exp_date
                        rows.append(row)

        # Create a DataFrame
        df = pd.DataFrame(rows)

        # Ensure all columns are unique
        df = df.loc[:, ~df.columns.duplicated()]

        return df
    
    @staticmethod
    def _validate_indexSymbol(indexSymbol):
        """
        Validates the indexSymbol parameter.
        """
        available_values = ['$DJI', '$COMPX', '$SPX', 'NYSE', 'NASDAQ', 'OTCBB', 
                            'INDEX_ALL', 'EQUITY_ALL', 'OPTION_ALL', 'OPTION_PUT', 'OPTION_CALL']
        if indexSymbol not in available_values:
            raise ValueError(f"Invalid indexSymbol. Available values: {', '.join(available_values)}")
        else:
            return indexSymbol
        
    @staticmethod
    def _validate_sort(sort):
        """
        Validates the sort parameter.
        """
        available_values = ['VOLUME', 'TRADES', 'PERCENT_CHANGE_UP', 'PERCENT_CHANGE_DOWN']
        if sort not in available_values:
            raise ValueError(f"Invalid sort. Available values: {', '.join(available_values)}")
        else:
            return sort
        
    @staticmethod
    def _validate_history_frequency(frequency):
        """
        Validates the frequency parameter.
        """
        available_values = [0, 1, 5, 10, 30, 60]
        if frequency not in available_values:
            raise ValueError(f"Invalid frequency. Available values: {', '.join(available_values)}")
        else:
            return frequency
        
    @staticmethod
    def _validate_markets(market):
        """
        Validates the market parameter.
        """
        available_values = ['equity','option','bond', 'forex', 'future']
        if market not in available_values:
            raise ValueError(f"Invalid market. Available values: {', '.join(available_values)}")
        else:
            return market
        
    