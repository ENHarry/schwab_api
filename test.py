from schwab_api import SchwabAPI

client_id = 'your_client_id'
client_secret = 'your_client_secret'
schwab = SchwabAPI(client_id, client_secret)

# Get account information
account_info = schwab.account.get_account_info('your_account_id')
print(account_info)

# Set trade environment to paper trading
schwab.account.set_trade_environment(schwab.trades, is_paper=True)

# Place an option trade order with margin
option_order = schwab.trades.place_option_order('your_account_id', 'AAPL', 10, 'BUY_TO_OPEN', 'LIMIT', price=150.00, use_margin=True)
print(option_order)

# Use a trading strategy
iron_condor = schwab.strategies.iron_condor('your_account_id', 'AAPL', 1, '150C', '155C', '145P', '140P')
print(iron_condor)

# Get market quotes
quotes = schwab.market_data.get_quotes(['AAPL', 'GOOGL'])
print(quotes)

# Get historical data
historical_data = schwab.market_data.get_historical_data('AAPL', period_type='month', period=6)
print(historical_data)

# Stream live data
for live_data in schwab.market_data.stream_live_data(['AAPL', 'GOOGL']):
    print(live_data)
