import requests
import time
import logging
import base64

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class SchwabAuth:
    """
    Handles OAuth authentication for Schwab API.
    """

    def __init__(self, client_id, client_secret):
        """
        Initializes SchwabAuth with client credentials and performs initial authentication.
        
        :param client_id: Client ID for Schwab API
        :param client_secret: Client Secret for Schwab API
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = 'https://api.schwabapi.com/v1/oauth/token'
        self.token = None
        self.refresh_token = None
        self.token_expiry = None
        self.authenticate()

    def authenticate(self):
        """
        Authenticates with Schwab API using client credentials and retrieves access and refresh tokens.
        """
    
        headers = {
            'Authorization': f"Basic {base64.b64encode(f'{self.client_id}:{self.client_secret}'.encode()).decode()}",
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'grant_type': 'client_credentials'
        }
        try:
            response = requests.post(self.token_url, headers=headers, data=data)
            response.raise_for_status()
            token_info = response.json()
            self.token = token_info['access_token']
            self.refresh_token = token_info['refresh_token']
            self.token_expiry = time.time() + token_info['expires_in']
            logger.info('Successfully authenticated and retrieved tokens')
        except requests.exceptions.HTTPError as http_err:
            logger.error(f'HTTP error occurred during authentication: {http_err}')
            raise SystemExit(f"HTTP error occurred during authentication: {http_err}")
        except Exception as err:
            logger.error(f'An error occurred during authentication: {err}')
            raise SystemExit(f"An error occurred during authentication: {err}")

    def refresh(self):
        """
        Refreshes the access token using the refresh token if the current token is expired.
        """
        if self.token_expiry < time.time():
            headers = {
            'Authorization': f"Basic {base64.b64encode(f'{self.client_id}:{self.client_secret}'.encode()).decode()}",
            'Content-Type': 'application/x-www-form-urlencoded'
            }
            data = {
                'grant_type': 'refresh_token',
                'refresh_token': self.refresh_token
            }
            try:
                response = requests.post(self.token_url, headers=headers, data=data)
                response.raise_for_status()
                token_info = response.json()
                self.token = token_info['access_token']
                self.refresh_token = token_info['refresh_token']
                self.token_expiry = time.time() + token_info['expires_in']
                logger.info('Successfully refreshed token')
            except requests.exceptions.HTTPError as http_err:
                logger.error(f'HTTP error occurred during token refresh: {http_err}')
                raise SystemExit(f"HTTP error occurred during token refresh: {http_err}")
            except Exception as err:
                logger.error(f'An error occurred during token refresh: {err}')
                raise SystemExit(f"An error occurred during token refresh: {err}")

    def get_headers(self):
        """
        Returns the headers required for authenticated API requests.
        
        :return: Dictionary containing authorization and content-type headers
        """
        self.refresh()
        return {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
