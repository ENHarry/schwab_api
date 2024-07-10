import requests
import time

class SchwabAuth:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = 'https://api.schwabapi.com/v1/oauth/token'
        self.token = None
        self.refresh_token = None
        self.token_expiry = None
        self.authenticate()

    def authenticate(self):
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        response = requests.post(self.token_url, data=data)
        response.raise_for_status()
        token_info = response.json()
        self.token = token_info['access_token']
        self.refresh_token = token_info['refresh_token']
        self.token_expiry = time.time() + token_info['expires_in']

    def refresh(self):
        if self.token_expiry < time.time():
            data = {
                'grant_type': 'refresh_token',
                'refresh_token': self.refresh_token,
                'client_id': self.client_id,
                'client_secret': self.client_secret
            }
            response = requests.post(self.token_url, data=data)
            response.raise_for_status()
            token_info = response.json()
            self.token = token_info['access_token']
            self.refresh_token = token_info['refresh_token']
            self.token_expiry = time.time() + token_info['expires_in']

    def get_headers(self):
        self.refresh()
        return {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
