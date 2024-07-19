import unittest
from unittest.mock import patch
from schwab_api.account import Account

class TestAccount(unittest.TestCase):
    def setUp(self):
        """
        Set up the necessary attributes for the test case including authentication and account instantiation.
        """
        self.auth = patch('schwab_api.auth.SchwabAuth').start()
        self.account = Account(self.auth)

    def tearDown(self):
        """
        A method to stop all patches applied during testing teardown.
        """
        patch.stopall()

    @patch('requests.get')
    def test_get_account_info(self, mock_get):
        """
        Test case for the `get_account_info` method of the `Account` class.

        This test case mocks the `requests.get` function to simulate the HTTP request and response.
        It sets the status code of the mocked response to 200 and the JSON response value to `{'account': 'info'}`.
        Then it calls the `get_account_info` method of the `Account` class with the argument `'test_account_id'`.
        Finally, it asserts that the response is equal to `{'account': 'info'}`.

        Parameters:
            - mock_get: A `MagicMock` object representing the `requests.get` function.

        Returns:
            None
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'account': 'info'}
        response = self.account.get_account_info('test_account_id')
        self.assertEqual(response, {'account': 'info'})

    @patch('requests.get')
    def test_get_all_accounts(self, mock_get):
        """
        A description of the entire function, its parameters, and its return types.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'accounts': 'all'}
        response = self.account.get_all_accounts()
        self.assertEqual(response, {'accounts': 'all'})

    @patch('requests.get')
    def test_get_all_accountIDs(self, mock_get):
        """
        A description of the entire function, its parameters, and its return types.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'accountIDs': 'all'}
        response = self.account.get_all_accountIDs()
        self.assertEqual(response, {'accountIDs': 'all'})

    @patch('requests.get')
    def test_get_all_transactions(self, mock_get):
        """
        Test case for the `get_all_transactions` method of the `Account` class.

        This test case mocks the `requests.get` function to simulate the HTTP request and response.
        It sets the status code of the mocked response to 200 and the JSON response value to `{'transactions': 'all'}`.
        Then it calls the `get_all_transactions` method of the `Account` class with the argument `'test_account_id'`.
        Finally, it asserts that the response is equal to `{'transactions': 'all'}`.

        Parameters:
            - mock_get: A `MagicMock` object representing the `requests.get` function.

        Returns:
            None
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'transactions': 'all'}
        response = self.account.get_all_transactions('test_account_id')
        self.assertEqual(response, {'transactions': 'all'})

    @patch('requests.get')
    def test_get_transaction(self, mock_get):
        """
        A description of the entire function, its parameters, and its return types.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'transaction': 'details'}
        response = self.account.get_transaction('test_account_id', 'test_transaction_id')
        self.assertEqual(response, {'transaction': 'details'})

    @patch('requests.get')
    def test_get_user_preferences(self, mock_get):
        """
        A description of the entire function, its parameters, and its return types.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'preferences': 'user'}
        response = self.account.get_user_preferences()
        self.assertEqual(response, {'preferences': 'user'})

    def test_get_account_info(self):
        """
        A description of the entire function, its parameters, and its return types.
        """
        account_info = self.account.get_account_info('account_id')
        self.assertIsInstance(account_info, dict)

    def test_get_all_accounts(self):
        """
        A description of the entire function, its parameters, and its return types.
        """
        all_accounts = self.account.get_all_accounts()
        self.assertIsInstance(all_accounts, dict)

    def test_get_all_accountIDs(self):
        """
        Test the `get_all_accountIDs` method of the `Account` class.

        This test case verifies that the `get_all_accountIDs` method returns a dictionary.

        Parameters:
            self (TestAccount): The test case instance.

        Returns:
            None
        """
        all_accountIDs = self.account.get_all_accountIDs()
        self.assertIsInstance(all_accountIDs, dict)

    def test_get_all_transactions(self):
        """
        Test case for the `get_all_transactions` method of the `Account` class.

        This test case verifies that the `get_all_transactions` method returns a dictionary.

        Parameters:
            self (TestAccount): The test case instance.

        Returns:
            None
        """
        all_transactions = self.account.get_all_transactions('account_id')
        self.assertIsInstance(all_transactions, dict)

    def test_get_transaction(self):
        """
        A description of the entire function, its parameters, and its return types.
        """
        transaction = self.account.get_transaction('account_id', 'transaction_id')
        self.assertIsInstance(transaction, dict)

    def test_get_user_preferences(self):
        """
        A description of the entire function, its parameters, and its return types.
        """
        user_preferences = self.account.get_user_preferences()
        self.assertIsInstance(user_preferences, dict)

    def test_get_account_info_invalid_account(self):
        """
        A description of the entire function, its parameters, and its return types.
        """
        with self.assertRaises(SystemExit):
            self.account.get_account_info('invalid_account_id')

    def test_get_transaction_invalid_transaction(self):
        """
        Test case for the `get_transaction` method of the `Account` class.

        This test case verifies that the `get_transaction` method raises a `SystemExit` exception when an invalid transaction ID is provided.

        Parameters:
            self (TestAccount): The test case instance.

        Returns:
            None
        """
        with self.assertRaises(SystemExit):
            self.account.get_transaction('account_id', 'invalid_transaction_id')

if __name__ == '__main__':
    unittest.main()
