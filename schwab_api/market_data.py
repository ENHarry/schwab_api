import requests
import pandas as pd
import numpy as np
import json

class MarketData:
    def __init__(self, auth):
        self.auth = auth
        self.base_url = 'https://api.schwabapi.com/marketdata'

    def get_quotes(self, symbols):
        url = f"{self.base_url}/quotes"
        headers = self.auth.get_headers()
        params = {'symbols': ','.join(symbols)}
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        return pd.DataFrame(data)

    def get_historical_data(self, symbol, period_type='year', period=1):
        url = f"{self.base_url}/pricehistory"
        headers = self.auth.get_headers()
        params = {
            'symbol': symbol,
            'periodType': period_type,
            'period': period
        }
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data['candles'])
        df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
        return df

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
