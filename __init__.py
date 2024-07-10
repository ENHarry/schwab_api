from .auth import SchwabAuth
from .account import Account
from .trades import Trades
from .strategies import Strategies
from .market_data import MarketData
from .fees import Fees

class SchwabAPI:
    def __init__(self, client_id, client_secret):
        self.auth = SchwabAuth(client_id, client_secret)
        self.account = Account(self.auth)
        self.trades = Trades(self.auth)
        self.strategies = Strategies(self.auth)
        self.market_data = MarketData(self.auth)
        self.fees = Fees(self.auth)
