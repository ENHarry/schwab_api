import unittest
from schwab_api.auth import SchwabAuth

class TestSchwabAuth(unittest.TestCase):
    
    def setUp(self):
        """
        Set up the test case by creating an instance of the SchwabAuth class with the provided client ID and client secret.

        This method is called before each test case is executed. It initializes the `self.auth` attribute with an instance of the `SchwabAuth` class.

        Parameters:
            self (TestSchwabAuth): The current test case instance.

        Returns:
            None
        """
        self.auth = SchwabAuth(client_id='your_client_id', client_secret='your_client_secret')


    def test_authenticate(self):
        """
        A method to test the authentication process by calling the authenticate method of the SchwabAuth class and checking the token, refresh token, and token expiry.
        
        Parameters:
            self (TestSchwabAuth): The current test case instance.
        
        Returns:
            None
        """
        self.auth.authenticate()
        self.assertIsNotNone(self.auth.token)
        self.assertIsNotNone(self.auth.refresh_token)
        self.assertIsNotNone(self.auth.token_expiry)

    def test_get_headers(self):
        """
        Test the function to get the headers and check if 'Authorization' and 'Content-Type' are included.
        """
        headers = self.auth.get_headers()
        self.assertIn('Authorization', headers)
        self.assertIn('Content-Type', headers)

    def test_refresh(self):
        """
        Test the `refresh` method of the `SchwabAuth` class.

        This test case verifies that the `refresh` method of the `SchwabAuth` class
        correctly refreshes the access token. It calls the `refresh` method on the
        `self.auth` instance and asserts that the `token` and `refresh_token` attributes
        of the `self.auth` instance are not `None`.

        Parameters:
            self (TestSchwabAuth): The current test case instance.

        Returns:
            None
        """
        self.auth.refresh()
        self.assertIsNotNone(self.auth.token)
        self.assertIsNotNone(self.auth.refresh_token)

    def test_authenticate_with_invalid_credentials(self):
        """
        A method to test the authentication process with invalid credentials by creating a SchwabAuth instance with invalid client ID and client secret, and then attempting to authenticate, expecting a SystemExit.
        """
        auth = SchwabAuth(client_id='invalid', client_secret='invalid')
        with self.assertRaises(SystemExit):
            auth.authenticate()

    def test_refresh_with_invalid_token(self):
        """
        Test the `refresh` method of the `SchwabAuth` class with an invalid token.

        This test case verifies that the `refresh` method of the `SchwabAuth` class
        raises a `SystemExit` exception when the token is invalid. It sets the `token`
        attribute of the `self.auth` instance to an invalid value, and then calls the
        `refresh` method. The test asserts that the `refresh` method raises a `SystemExit`
        exception.

        Parameters:
            self (TestSchwabAuth): The current test case instance.

        Returns:
            None
        """
        self.auth.token = 'invalid'
        with self.assertRaises(SystemExit):
            self.auth.refresh()

if __name__ == '__main__':
    unittest.main()
