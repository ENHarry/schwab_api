from seleniumwire import webdriver  # Use Selenium Wire instead of Selenium
from urllib.parse import urlparse, parse_qs
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading
import time
import base64
import requests
import webbrowser
from schwab_api.urls import SchwabUrls

class SchwabAuth:
    def __init__(self, client_id, client_secret, redirect_uri='https://127.0.0.1', username='', password='',
                 refresh_token=None, is_paper_account=False): 
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.urls = SchwabUrls()
        self.username = username
        self.password = password
        self.auth_code = None
        self.session_id = None
        self.token = None
        self.token_expires_in = 0
        self.refresh_token = refresh_token
        self.is_paper_account = is_paper_account

    def _get_auth_header(self):
        auth_str = f"{self.client_id}:{self.client_secret}"
        auth_bytes = auth_str.encode('ascii')
        auth_b64 = base64.b64encode(auth_bytes).decode('ascii')
        return f"Basic {auth_b64}"

    def authenticate(self):
        auth_url = self.urls.get_auth_url(self.client_id, self.redirect_uri)
        print("Auth URL:", auth_url)
        if self.refresh_token:
            self.refresh()
        else:
            # Set up Firefox options and Selenium Wire options
            firefox_options = Options()
            firefox_options.add_argument("--headless")
            firefox_options.add_argument("--no-sandbox")
            firefox_options.add_argument("--disable-dev-shm-usage")

            # Set up Selenium Wire to add headers
            wire_options = {
                'custom_headers': {
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
                    'cache-control': 'No-Cache',
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.9",
                    "Accept-Encoding": "gzip, deflate, br, zstd",
                    "Connection": "keep-alive",
                    "Upgrade-Insecure-Requests": "1",
                    "DNT": "1",
                    "Host": "api.schwabapi.com",
                    "Priority": "u=0, i",
                    "Sec-Fetch-Dest": "document",
                    "Sec-Fetch-Mode": "navigate",
                    "Sec-Fetch-Site": "none",
                    "Sec-Fetch-User": "?1",
                    "Sec-GPC": "1",
                }

            }

            # Start Selenium Wire WebDriver
            service = Service(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service, options=firefox_options, seleniumwire_options=wire_options)

            try:
                driver.get(auth_url)
                login_xpath = '//*[@id="btnLogin"]'
                WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, login_xpath)))

                # Fill in username and password
                driver.find_element(By.XPATH, '//*[@id="loginIdInput"]').send_keys(self.username)
                driver.find_element(By.XPATH, '//*[@id="passwordInput"]').send_keys(self.password)
                driver.find_element(By.XPATH, login_xpath).click()

                # Wait for the continue button and accept terms if present
                terms_xpath = '//*[@id="acceptTerms"]'
                if driver.find_elements(By.XPATH, terms_xpath):
                    driver.find_element(By.XPATH, terms_xpath).click()
                continue_xpath = '//button[@id="submit-btn"]'
                if driver.find_elements(By.XPATH, continue_xpath):
                    driver.find_element(By.XPATH, continue_xpath).click()

                # Monitor redirection to extract authorization code and session ID
                WebDriverWait(driver, 10).until(lambda d: d.current_url != auth_url)
                redirected_url = driver.current_url

            except Exception as e:
                webbrowser.open(auth_url)
                redirected_url = input("Enter the URL you were redirected to after completing the login: ")
            finally:
                driver.quit()

            # Parse URL to extract authorization code and session ID
            parsed_url = urlparse(redirected_url)
            query_params = parse_qs(parsed_url.query)
            self.auth_code = query_params.get('code', [None])[0]
            self.session_id = query_params.get('session', [None])[0]

            if not self.auth_code or not self.session_id:
                raise ValueError("Failed to obtain authorization code and session ID.")
            self._exchange_code_for_tokens()

    def _exchange_code_for_tokens(self):
        headers = {
            'Authorization': self._get_auth_header(),
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'grant_type': 'authorization_code',
            'code': self.auth_code,
            'redirect_uri': self.redirect_uri
        }
        response = requests.post(self.urls.get_token_url(), headers=headers, data=data)
        response.raise_for_status()
        token_data = response.json()
        self.token = token_data.get('access_token')
        self.refresh_token = token_data.get('refresh_token', None)
        self.token_expires_in = token_data.get('expires_in', 1800)

    def refresh(self):
        headers = {
            'Authorization': self._get_auth_header(),
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token
        }
        response = requests.post(self.urls.get_token_url(), headers=headers, data=data)
        response.raise_for_status()
        token_data = response.json()
        self.token = token_data.get('access_token')
        self.refresh_token = token_data.get('refresh_token', self.refresh_token)
        self.token_expires_in = token_data.get('expires_in', 1800)

    def get_headers(self):
        if not self.token:
            self.authenticate()
        return {
            'Authorization': f"Bearer {self.token}"
        }
