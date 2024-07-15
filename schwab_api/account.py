import requests

class Account:
    def __init__(self, auth):
        self.auth = auth
        self.base_url = 'https://api.schwabapi.com/trader/v1/'

    def get_account_info(self, account_id):
        url = f"{self.base_url}/accounts/{account_id}"
        headers = self.auth.get_headers()
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_all_accounts(self):
        url = f"{self.base_url}/accounts/"
        headers = self.auth.get_headers()
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_all_accountIDs(self):
        url = f"{self.base_url}/accounts/accountNumbers"
        headers = self.auth.get_headers()
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    
    def get_all_transactions(self, account_id):
        url = f"{self.base_url}/accounts/{account_id}/transactions"
        headers = self.auth.get_headers()
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    
    def get_transaction(self, account_id, transaction_id):
        url = f"{self.base_url}/accounts/{account_id}/transactions/{transaction_id}"
        headers = self.auth.get_headers()
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_user_preferences(self):
        url = f"{self.base_url}/userPreferences"
        headers = self.auth.get_headers()
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    
    def set_trade_environment(self, trades_object, is_paper):
        trades_object.set_paper_account(is_paper)
