import requests
import logging

logger = logging.getLogger(__name__)

def handle_response(response):
    try:
        response.raise_for_status()
        logger.info("Success")
    except requests.exceptions.HTTPError as err:
        # Handle specific status codes if needed
        logger.error(f"An error occurred while placing order: {err}")
        raise SystemExit(err)   
    return response.json()
