import unittest
from schwab_api.auth import SchwabAuth

class TestSchwabAuth(unittest.TestCase):
    def setUp(self):
        self.client_id = 'test_client_id'
        self.client_secret = 'test_client_secret'
        self.auth = SchwabAuth(self.client_id, self.client_secret)

    def test_authenticate(self):
        self.auth.authenticate()
        self.assertIsNotNone(self.auth.token)
        self.assertIsNotNone(self.auth.refresh_token)
        self.assertIsNotNone(self.auth.token_expiry)

    def test_get_headers(self):
        headers = self.auth.get_headers()
        self.assertIn('Authorization', headers)
        self.assertIn('Content-Type', headers)

if __name__ == '__main__':
    unittest.main()
