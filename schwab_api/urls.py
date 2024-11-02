class SchwabUrls:
    BASE_URL = "://api.schwabapi.com"

#/--------------------------- Authentication ---------------------------/
    @classmethod
    def get_auth_base_url(cls):
        """Returns the base URL for the OAuth authorization flow.

        Returns
        -------
        str
        """
        return f"https{cls.BASE_URL}/v1/oauth"
    
    @classmethod
    def get_auth_url(cls, client_id, redirect_uri):
        """Returns the URL to initiate the OAuth authorization flow.

        Parameters
        ----------
        client_id : str
            The Client ID for the application.
        redirect_uri : str
            The URL that the browser will redirect to after authorization.

        Returns
        -------
        str
            The URL to initiate the OAuth authorization flow.
        """
        url = cls.get_auth_base_url()
        return f"{url}/authorize?client_id={client_id}&redirect_uri={redirect_uri}"


#/--------------------------- Accounts ---------------------------/
    @classmethod
    def get_account_url(cls):
        return f"https{cls.BASE_URL}/accounts"

    @classmethod
    def get_transactions_url(cls):
        return f"https{cls.BASE_URL}/transactions"
    
    @classmethod
    def get_order_url(cls):
        return f"https{cls.BASE_URL}/orders"

#/--------------------------- Market Data ---------------------------/
    @classmethod
    def get_market_data_url(cls, livestream=False):
        if livestream:
            return f"wss{cls.BASE_URL}/marketdata/v1/stream"
        return f"https{cls.BASE_URL}/marketdata/v1"
    
    @classmethod
    def get_symbol_quote_url(cls, symbol):
        url = cls.get_market_data_url()
        return f"{url}/{symbol}quotes"
    
    @classmethod
    def get_quotes_url(cls):
        url = cls.get_market_data_url()
        return f"{url}/quotes"
    
    @classmethod
    def get_optionchains_url(cls):
        url = cls.get_market_data_url()
        return f"{url}/chains"
    
    @classmethod
    def get_optionchain_expiry_url(cls, livestream=False):
        url = cls.get_optionchains_url(livestream)
        return f"{url}/expirationchain"
    
    @classmethod
    def get_pricehistory_url(cls):
        url = cls.get_market_data_url()
        return f"{url}/pricehistory"
    
    @classmethod
    def get_movers_url(cls, index_symbol):
        url = cls.get_market_data_url()
        return f"{url}/movers/{index_symbol}"
    
    @classmethod
    def get_livedata_url(cls):
        url = cls.get_market_data_url()
        return f'{url}/stream'
    
    @classmethod
    async def get_livestream_url(cls):
        return cls.get_market_data_url(livestream=True)
    
    @classmethod
    def get_markethours_url(cls):
        url = cls.get_market_data_url()
        return f"{url}/markets"
    
    @classmethod
    def get_instruments_url(cls):
        url = cls.get_market_data_url()
        return f"{url}/instruments" 

