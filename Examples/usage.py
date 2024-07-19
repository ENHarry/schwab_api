from schwab_api.auth import SchwabAuth

auth = SchwabAuth(client_id='your_client_id', client_secret='your_client_secret')
auth.authenticate()


from schwab_api.account import Account

account = Account(auth)
account_info = account.get_account_info('account_id')


from schwab_api.market_data import MarketData

market_data = MarketData(auth)
quotes = market_data.get_symbol_quotes('AAPL')



from schwab_api.trades import Trades

trades = Trades(auth)
order_data = trades.place_order('account_id', asset_type='EQUITY', trading_strategy='buy_market_stock', symbol='AAPL', quantity=10)
