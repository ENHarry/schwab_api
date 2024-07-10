import requests

class Account:
    def __init__(self, auth):
        self.auth = auth
        self.base_url = 'https://api.schwabapi.com/accounts'

    def get_account_info(self, account_id):
        url = f"{self.base_url}/{account_id}"
        headers = self.auth.get_headers()
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_all_accounts(self):
        url = self.base_url
        headers = self.auth.get_headers()
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def set_trade_environment(self, trades_object, is_paper):
        trades_object.set_paper_account(is_paper)
