import requests
import logging

logger = logging.getLogger(__name__)

class Account:
    """
    Provides methods to interact with Schwab account data.
    """

    def __init__(self, auth):
        """
        Initializes Account with authentication object.
        
        :param auth: SchwabAuth object for authentication
        """
        self.auth = auth
        self.base_url = 'https://api.schwabapi.com/trader/v1/'

    def get_account_info(self, account_id):
        """
        Retrieves information for a specific account.
        
        :param account_id: ID of the account
        :return: JSON response containing account information
        """
        url = f"{self.base_url}/accounts/{account_id}"
        headers = self.auth.get_headers()
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            logger.info(f"Retrieved account info for account ID: {account_id}")
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred while retrieving account info: {http_err}")
            raise SystemExit(f"HTTP error occurred while retrieving account info: {http_err}")
        except Exception as err:
            logger.error(f"An error occurred while retrieving account info: {err}")
            raise SystemExit(f"An error occurred while retrieving account info: {err}")

    def get_all_accounts(self):
        """
        Retrieves information for all accounts.
        
        :return: JSON response containing all account information
        """
        url = f"{self.base_url}/accounts/"
        headers = self.auth.get_headers()
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            logger.info("Retrieved all account info")
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred while retrieving all accounts: {http_err}")
            raise SystemExit(f"HTTP error occurred while retrieving all accounts: {http_err}")
        except Exception as err:
            logger.error(f"An error occurred while retrieving all accounts: {err}")
            raise SystemExit(f"An error occurred while retrieving all accounts: {err}")

    def get_all_accountIDs(self):
        """
        Retrieves all account IDs.
        
        :return: JSON response containing all account IDs
        """
        url = f"{self.base_url}/accounts/accountNumbers"
        headers = self.auth.get_headers()
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            logger.info("Retrieved all account IDs")
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred while retrieving account IDs: {http_err}")
            raise SystemExit(f"HTTP error occurred while retrieving account IDs: {http_err}")
        except Exception as err:
            logger.error(f"An error occurred while retrieving account IDs: {err}")
            raise SystemExit(f"An error occurred while retrieving account IDs: {err}")

    def get_all_transactions(self, account_id):
        """
        Retrieves all transactions for a specific account.
        
        :param account_id: ID of the account
        :return: JSON response containing all transactions for the account
        """
        url = f"{self.base_url}/accounts/{account_id}/transactions"
        headers = self.auth.get_headers()
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            logger.info(f"Retrieved all transactions for account ID: {account_id}")
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred while retrieving transactions: {http_err}")
            raise SystemExit(f"HTTP error occurred while retrieving transactions: {http_err}")
        except Exception as err:
            logger.error(f"An error occurred while retrieving transactions: {err}")
            raise SystemExit(f"An error occurred while retrieving transactions: {err}")

    def get_transaction(self, account_id, transaction_id):
        """
        Retrieves details for a specific transaction.
        
        :param account_id: ID of the account
        :param transaction_id: ID of the transaction
        :return: JSON response containing transaction details
        """
        url = f"{self.base_url}/accounts/{account_id}/transactions/{transaction_id}"
        headers = self.auth.get_headers()
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            logger.info(f"Retrieved transaction details for transaction ID: {transaction_id}")
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred while retrieving transaction: {http_err}")
            raise SystemExit(f"HTTP error occurred while retrieving transaction: {http_err}")
        except Exception as err:
            logger.error(f"An error occurred while retrieving transaction: {err}")
            raise SystemExit(f"An error occurred while retrieving transaction: {err}")

    def get_user_preferences(self):
        """
        Retrieves user preferences.
        
        :return: JSON response containing user preferences
        """
        url = f"{self.base_url}/userPreferences"
        headers = self.auth.get_headers()
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            raise SystemExit(f"HTTP error occurred while retrieving user preferences: {http_err}")
        except Exception as err:
            raise SystemExit(f"An error occurred while retrieving user preferences: {err}")

    def set_trade_environment(self, trades_object, is_paper):
        """
        Sets the trading environment (paper/live) for the trades object.
        
        :param trades_object: Trades object to set environment for
        :param is_paper: Boolean indicating if the environment is paper (True) or live (False)
        """
        trades_object.set_paper_account(is_paper)
