import datetime

class HelperFuncs:
    def __init__(self):
        pass

    def __validate_fields(self, fields):
        """
        Validates the fields parameter.
        
        :param fields: Fields to include in the response
        :return: None
        """
        valid_fields = ['quote', 'fundamental', 'extended', 'reference', 'regular']
        if fields not in valid_fields:
            raise ValueError("Fields parameter must be one of: " + ", ".join(valid_fields))
        else:
            if fields is str:
                fields = fields.replace(' ', '')
            else:
                fields = ','.join(fields).replace(' ', '')
            return fields
        
    def __format_symbols(self, symbols):
        """
        Formats the symbols parameter.
        
        :param symbols: List of symbols to retrieve quotes for
        :return: Formatted symbols string
        """
        if symbols is str:
            symbols = symbols.replace(' ', '')
        else:
            symbols = ','.join(symbols).replace(' ', '')
        return symbols
    
    def __validate_contractType(self, contractType):
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
        
    def __validate_strategy(self, strategy):
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
        
    def __validate_assetType(self, assetType):
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

    def __validate_abbr_contractType(self, contractType):
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

    def __validate_range(self, range):
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

    def __validate_periodType(self, periodType):
        """
        Validates the periodType parameter.
        
        :param periodType: The chart period being requested.
        """
        valid_periodTypes = ['day', 'month', 'year', 'ytd']
        if periodType not in valid_periodTypes:
            raise ValueError("Period type parameter must be one of: " + ", ".join(valid_periodTypes))
        else:
            return periodType
           
    def __validate_period(self,periodType,period):
        """
        Validates the period parameter.
        
        :param period: The number of chart period types.
        """
        day_valid_values = [1, 2, 3, 4, 5, 10]
        month_valid_values = [1, 2, 3, 6]
        year_valid_values = [1, 2, 3, 5, 10, 15, 20]
        ytd_valid_value = 1
        periodType = self.__validate_periodType(periodType)
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
        
    def __validate_frequencyType(self, frequencyType, periodType):
        """
        Validates the frequencyType parameter.
        
        :param frequencyType: The timefrequency with which a new candle is formed.
        """
        day_valid_value = 'minute' # valid values is minute
        month_valid_values = ['daily', 'weekly']
        year_valid_values = ['daily', 'weekly', 'monthly']
        ytd_valid_values = ['daily', 'weekly']

        periodType = self.__validate_periodType(periodType)

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


    def __validate_frequency(self, frequencyType, frequency):
        """
        Validates the frequency parameter.
        """    
        frequencyType = self.__validate_frequencyType(frequencyType)
        
        minute_valid_values = [1, 5, 10, 15, 30]
        daily_valid_value = 1
        weekly_valid_value = 1
        monthly_valid_value = 1
        
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

    def __date_format(self, date):
        """
        Formats the date parameter.
        """
        return datetime.epoch(date)