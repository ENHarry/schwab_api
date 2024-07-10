from schwab_api import SchwabAPI

client_id = 'your_client_id'
client_secret = 'your_client_secret'
schwab = SchwabAPI(client_id, client_secret)

# Get account information
account_info = schwab.account.get_account_info('your_account_id')
print(account_info)

# Place an order using a trading strategy
order_response = schwab.trades.place_order(
    account_id='your_account_id',
    asset_type='OPTION',
    trading_strategy='iron_condor',
    is_paper=True,
    symbol='AAPL',
    lower_put_strike='130',
    upper_put_strike='135',
    lower_call_strike='145',
    upper_call_strike='150',
    quantity=1,
    order_type='LIMIT',
    price=1.00
)
print(order_response)
