import unittest
from schwab_api.auth import SchwabAuth
from schwab_api.market_data import MarketData
import pandas as pd

class TestMarketData(unittest.TestCase):

    def setUp(self):
        """
        Set up the test case by creating an instance of the SchwabAuth class with the provided client ID and client secret.
        This method initializes the `self.auth` attribute with an instance of the `SchwabAuth` class.
        It also initializes the `self.market_data` attribute with an instance of the `MarketData` class, using the `self.auth` object.

        Parameters:
            self (TestMarketData): The current test case instance.

        Returns:
            None
        """
        self.auth = SchwabAuth(client_id='your_client_id', client_secret='your_client_secret')
        self.market_data = MarketData(self.auth)

    def test_get_symbol_quotes(self):
        """
        Test the `get_symbol_quotes` method of the `MarketData` class.

        This test case verifies that the `get_symbol_quotes` method of the `MarketData` class returns a `pd.DataFrame` object.

        Parameters:
            self (TestMarketData): The current test case instance.

        Returns:
            None
        """
        quotes = self.market_data.get_symbol_quotes('AAPL')
        self.assertIsInstance(quotes, pd.DataFrame)

    def test_get_quotes(self):
        """
        Test the `get_quotes` method of the `MarketData` class.

        This test case verifies that the `get_quotes` method of the `MarketData` class returns a `pd.DataFrame` object.

        Parameters:
            self (TestMarketData): The current test case instance.

        Returns:
            None
        """
        quotes = self.market_data.get_quotes(['AAPL', 'GOOGL'])
        self.assertIsInstance(quotes, pd.DataFrame)

    def test_get_option_chains(self):
        """
        Test the `get_option_chains` method of the `MarketData` class.

        This test case verifies that the `get_option_chains` method of the `MarketData` class returns a `pd.DataFrame` object.

        Parameters:
            self (TestMarketData): The current test case instance.

        Returns:
            None
        """
        option_chains = self.market_data.get_option_chains('AAPL')
        self.assertIsInstance(option_chains, pd.DataFrame)

    def test_get_option_expiration_chain(self):
        """
        Test the `get_option_expiration_chain` method of the `MarketData` class.

        This test case verifies that the `get_option_expiration_chain` method of the `MarketData` class returns a dictionary.

        Parameters:
            self (TestMarketData): The current test case instance.

        Returns:
            None
        """
        expiration_chain = self.market_data.get_option_expiration_chain('AAPL')
        self.assertIsInstance(expiration_chain, dict)

    def test_get_historical_data(self):
        """
        Test the `get_historical_data` method of the `MarketData` class.

        This test case verifies that the `get_historical_data` method of the `MarketData` class returns a `pd.DataFrame` object.

        Parameters:
            self (TestMarketData): The current test case instance.

        Returns:
            None
        """
        historical_data = self.market_data.get_historical_data('AAPL')
        self.assertIsInstance(historical_data, pd.DataFrame)

    def test_get_active_gainers_losers(self):
        """
        Test the `get_active_gainers_losers` method of the `MarketData` class.

        This test case verifies that the `get_active_gainers_losers` method of the `MarketData` class returns a dictionary.

        Parameters:
            self (TestMarketData): The current test case instance.

        Returns:
            None
        """
        gainers_losers = self.market_data.get_active_gainers_losers()
        self.assertIsInstance(gainers_losers, dict)

    def test_get_symbol_quotes_invalid_symbol(self):
        """
        Test case for the `get_symbol_quotes` method of the `MarketData` class.

        This test case verifies that the `get_symbol_quotes` method raises a `SystemExit` exception when an invalid symbol is provided.

        Parameters:
            self (TestMarketData): The test case instance.

        Returns:
            None
        """
        with self.assertRaises(SystemExit):
            self.market_data.get_symbol_quotes('INVALID')

    def test_get_historical_data_invalid_symbol(self):
        """
        Test case for the `get_historical_data_invalid_symbol` method of the `MarketData` class.

        This test case verifies that the `get_historical_data_invalid_symbol` method raises a `SystemExit` exception when an invalid symbol is provided.

        Parameters:
            self (TestMarketData): The test case instance.

        Returns:
            None
        """
        with self.assertRaises(SystemExit):
            self.market_data.get_historical_data('INVALID')
