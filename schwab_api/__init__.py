from .authen import SchwabAuth
from .trades import Trader
from .strategies import Strategies
from .market_data import MarketData
from .fees import Fees
from .helper import HelperFuncs
from .urls import SchwabUrls
from .auth import SchwabAuthe as HeadlessAuth

class SchwabAPI:
    def __init__(self, client_id, client_secret):
        self.auth = SchwabAuth(client_id, client_secret)
        self.trader = Trader(self.auth)
        self.strategies = Strategies(self.auth)
        self.market_data = MarketData(self.auth)
        self.fees = Fees(self.auth)
        self.helper = HelperFuncs()
        self.urls = SchwabUrls()
        self.headless_auth = HeadlessAuth(client_id, client_secret)
