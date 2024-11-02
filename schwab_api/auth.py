import requests
#import logging
import base64
import time
import threading
import webbrowser
from loguru import logger
from selenium import webdriver
from urllib.parse import urlparse, parse_qs
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SchwabAuth:
    def __init__(self, client_id, client_secret, redirect_uri='https://127.0.0.1', username='', password='',
                 refresh_token=None, is_paper_account=False): 
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.username = username
        self.password = password
        self.auth_code = None
        self.session_id = None
        self.token = None
        self.token_expires_in = 0
        self.base_url = 'https://api.schwabapi.com/v1/oauth'
        self.refresh_token = refresh_token
        self.is_paper_account = is_paper_account
        

    def get_accType(self):
        return self.is_paper_account
    
    def _get_auth_header(self):
        auth_str = f"{self.client_id}:{self.client_secret}"
        auth_bytes = auth_str.encode('ascii')
        auth_b64 = base64.b64encode(auth_bytes).decode('ascii')
        return f"Basic {auth_b64}"

    def authenticate(self):
        auth_url = f"{self.base_url}/authorize?client_id={self.client_id}&redirect_uri={self.redirect_uri}"
        print("Auth URL:")
        print(auth_url)
        print("------------------------------------------------")

        # if a separate session has been run with a refresh token, use that one
        if self.refresh_token:
            self.refresh()
        else:
        
            # Set up Firefox options
            firefox_options = Options()
            #firefox_options.add_argument("--headless")  # Run in headless mode
            firefox_options.add_argument("--no-sandbox")
            firefox_options.add_argument("--disable-dev-shm-usage")
            
            # Start the Firefox WebDriver
            service = Service(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service, options=firefox_options)
            
            try:
                driver.get(auth_url)

                # Wait for the login button to be clickable
                # login_xpath = '//button[@id="btnLogin"]'
                login_xpath = '//*[@id="btnLogin"]'  #'//lms-app-root/section/div[1]/div/section/lms-login-one-step-container/lms-login-one-step/section/div[1]/div[4]/button'
                WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, login_xpath)))
                login_url = driver.current_url
                print('Expected Login URL: https://sws-gateway.schwab.com/ui/host/#/login-one-step')
                print("Login URL:")
                print(login_url)
                print("------------------------------------------------")

                # Set XPath for username and password fields
                # usr_xpath = '//input[@id="loginIdInput"]' 
                usr_xpath = '//*[@id="loginIdInput"]' #'//lms-app-root/section/div[1]/div/section/lms-login-one-step-container/lms-login-one-step/section/div[1]/div[2]/div/div/input' 
                # pswd_xpath = '//input[@id="passwordInput"]'
                pswd_xpath = '//*[@id="passwordInput"]' #'//lms-app-root/section/div[1]/div/section/lms-login-one-step-container/lms-login-one-step/section/div[1]/div[3]/div/input'

                # Automatically fill in the login form
                driver.find_element(By.XPATH, usr_xpath).send_keys(self.username)
                driver.find_element(By.XPATH, pswd_xpath).send_keys(self.password)
                driver.find_element(By.XPATH, login_xpath).click()

                # Monitor for page load after login
                WebDriverWait(driver, 20).until(lambda d: d.execute_script('return document.readyState') == 'complete')
                
                # store the step process url
                process_url = driver.current_url
                print('Expected Process URL 1: https://sws-gateway.schwab.com/ui/host/#/third-party-auth/cag')
                print("Process URL 1:")
                print(process_url)
                print("------------------------------------------------")

                # Accept the terms and conditions if prompted and click the continue button
                # //input[@id="acceptTerms"]
                terms_xpath = '//*[@id="acceptTerms"]' #'//lms-app-root/section/div[1]/div[1]/section/lms-cag-container[1]/lms-cag[1]/div[1]/form/div[1]/input[1]'
                if driver.find_elements(By.XPATH, terms_xpath):
                    driver.find_element(By.XPATH, terms_xpath).click()
                    print("Accepted Terms")
                else:
                    print("Terms Not Found")

                # Wait for the continue button to be clickable 
                # //button[@id="submit-btn"]
                continue_xpath = '//lms-app-root/section/div[1]/div[1]/section/lms-cag-container[1]/lms-cag[1]/div[1]/form/div[2]/button[2]'
                
                if driver.find_element(By.XPATH, continue_xpath):
                    driver.find_element(By.XPATH, continue_xpath).click()
                    print("Continue Clicked")
                else:
                    print("Continue Not Found")

                # Accept the alert if it pops up
                # /html[1]/body[1]/div[1]/lms-app-root/section/div[1]/div[1]/section/lms-cag-container/lms-cag/div[1]/sdps-modal/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/button[2]
                driver.switch_to.alert.accept()

                # store the step process url
                process_url = driver.current_url
                print('Expected Process URL 2: https://sws-gateway.schwab.com/ui/host/#/third-party-auth/cag')
                print("Process URL 2:")
                print(process_url)
                print("------------------------------------------------")
                
                #for individual accounts with only one account, it is checked by default
                #for multiple accounts, it is not checked by default but not yet implemented in this package
                # '//button[@id="submit-btn"]' 

                selectAccount_xpath = '//lms-app-root[1]/section[1]/div[1]/div[1]/section[1]/lms-cag-account-container[1]/lms-cag-account[1]/div[1]/form/div[2]/button[2]'

                # Wait for the submit button to be clickable
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, selectAccount_xpath)))
            
                if driver.find_elements(By.XPATH, selectAccount_xpath):
                    driver.find_element(By.XPATH, selectAccount_xpath).click()

                # update stored step process url
                process_url = driver.current_url
                print("Expected Process URL 3: https://sws-gateway.schwab.com/ui/host/#/third-party-auth/cag")
                print("Updated Process URL:")
                print(process_url)
                print("------------------------------------------------")

                # Wait for the "Done" button to be clickable 
                # '/html[1]/body[1]/div[1]/lms-app-root[1]/section[1]/div[1]/div[1]/section[1]/lms-cag-confirmation-container[1]/lms-cag-confirmation[1]/div[1]/div[1]/button[1]'
                done_xpath = '//button[@id="cancel-btn"]'
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, done_xpath)))
                if driver.find_elements(By.XPATH, done_xpath):
                    driver.find_element(By.XPATH, done_xpath).click()

                # Wait for the redirect to complete and the URL to change
                WebDriverWait(driver, 10).until(lambda d: d.current_url != auth_url and d.current_url != process_url)

                # Grab the current URL which should contain the authorization code and session ID
                redirected_url = driver.current_url
                print("Expected Redirected URL:https://127.0.0.1/?code=C0.b2F1dGgyLmJkYy5zY2h3YWIuY29t.Dg8lTcdJvLN3xaCAbcqswWXkZk_aOfAQn90zWFg1JaY%40&session=c4ca5237-0354-41ad-b689-bead833aed25")
                print("Redirected URL:")
                print(redirected_url)
                print("------------------------------------------------")

            except Exception as e:
                logger.info("Failed to login automatically to obtain authorization code and session ID. Please manually complete authentication process.")
                logger.info("To complete authentication manually, visit the following AUTH URL:")
                webbrowser.open(auth_url)
                logger.info("After completing authentication, you'll be redirected to an error page.") 
                logger.info("Copy the of the error page, paste and enter it below.")
                logger.info("------------------------------------------------")
                redirected_url = input("Please enter the URL you were redirected to when you completed the manual authentication: ")
            finally:
                driver.quit()

            # Parse the URL to extract authorization code and session ID
            parsed_url = urlparse(redirected_url)
            print("Parsed URL:")
            print(parsed_url)
            print("------------------------------------------------")
            query_params = parse_qs(parsed_url.query)
            print("Query Parameters:")
            print(query_params)
            self.auth_code = query_params.get('code', [None])[0]
            self.session_id = query_params.get('session', [None])[0]

            # Validate the authorization code and session ID
            if not self.auth_code or not self.session_id:
                raise ValueError("Failed to obtain authorization code and session ID.")

            self._exchange_code_for_tokens()

    def _exchange_code_for_tokens(self):
        """
        Step 2: Access Token Creation - Exchange authorization code for access and refresh tokens.
        """
        headers = {
            'Authorization': self._get_auth_header(),
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'grant_type': 'authorization_code',
            'code': self.auth_code,  # Ensure the code is URL decoded
            'redirect_uri': self.redirect_uri
        }
        response = requests.post(f"{self.base_url}/token", headers=headers, data=data)
        response.raise_for_status()
        token_data = response.json()
        self.token = token_data.get('access_token')
        self.refresh_token = token_data.get('refresh_token', None)
        self.token_expires_in = token_data.get('expires_in', 1800)  # Default to 30 minutes if not provided
        
        if not self.token:
            raise ValueError("Failed to exchange authorization code for access token.")

        self._start_auto_refresh()

    def refresh(self):
        """
        Step 4: Refresh Access Token - Automatically refresh the access token using the refresh token.
        """
        if not self.refresh_token:
            raise SystemExit("No refresh token available. Please authenticate first.")

        headers = {
            'Authorization': self._get_auth_header(),
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token
        }
        response = requests.post(f"{self.base_url}/token", headers=headers, data=data)
        response.raise_for_status()
        token_data = response.json()
        self.token = token_data.get('access_token')
        self.refresh_token = token_data.get('refresh_token', self.refresh_token)
        self.token_expires_in = token_data.get('expires_in', 1800)

        self._start_auto_refresh()

    def get_headers(self):
        """
        Step 3: Make an API Call - Get the authorization headers for API requests.
        """
        if not self.token:
            self.authenticate()
        return {
            'Authorization': f"Bearer {self.token}"
        }

    def _start_auto_refresh(self):
        """
        Automatically refresh the token before it expires.
        """
        def refresh_token():
            while True:
                time.sleep(max(self.token_expires_in - 30, 0))  # Refresh 30 seconds before expiry
                self.refresh()

        refresh_thread = threading.Thread(target=refresh_token, daemon=True)
        refresh_thread.start()

    