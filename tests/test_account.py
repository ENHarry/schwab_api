import unittest
from unittest.mock import patch
from schwab_api.account import Account

class TestAccount(unittest.TestCase):
    def setUp(self):
        self.auth = patch('schwab_api.auth.SchwabAuth').start()
        self.account = Account(self.auth)

    def tearDown(self):
        patch.stopall()

    @patch('requests.get')
    def test_get_account_info(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'account': 'info'}
        response = self.account.get_account_info('test_account_id')
        self.assertEqual(response, {'account': 'info'})

    @patch('requests.get')
    def test_get_all_accounts(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'accounts': 'all'}
        response = self.account.get_all_accounts()
        self.assertEqual(response, {'accounts': 'all'})

if __name__ == '__main__':
    unittest.main()
