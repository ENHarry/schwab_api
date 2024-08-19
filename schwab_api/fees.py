import requests

class Fees:
    def __init__(self, auth):
        self.auth = auth
        self.fee_url = None

    '''def get_fees(self, trade_type):
        headers = self.auth.get_headers()
        params = {'tradeType': trade_type}
        response = requests.get(self.fee_url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
        '''
    def calculate_fees(self, trade_data, assetType: str = 'options'):
        if self.fee_url is not None:
            fees = self.get_fees(trade_data['type'])
        else:
            
            if assetType == 'options':
                fee_per_contract = 0.65
                fees = fee_per_contract * trade_data['quantity']
            elif assetType == 'otc':
                fees = 6.95
            elif assetType == 'stocks' or assetType == 'etf':
                fees = 0.0
            elif assetType == 'forex':
                fee_per_trade = 0.0
                spread_fee = ((trade_data["ask_price"] - trade_data["bid_price"])/trade_data['ask_price'])*100
                fees = fee_per_trade + spread_fee
            elif assetType == 'futures' or assetType == 'futures options':
                fee_per_contract = 2.25
                fees = fee_per_contract * trade_data['quantity']
            else:
                ValueError('Invalid asset type')
        return fees
