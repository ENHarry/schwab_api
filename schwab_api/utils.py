import requests

def handle_response(response):
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        # Handle specific status codes if needed
        raise SystemExit(err)
    return response.json()
