import time
import requests
import os
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

API_ENDPOINT = "https://canary.discord.com/api/v9/users/@me/channels"

def validate_token(token):
    headers = {"Authorization": token, "Content-Type": "application/json"}
    response = requests.get(API_ENDPOINT, headers=headers)
    return response.status_code == 200

def keep_alive():
    """
    Keep the Discord bot alive by periodically sending a GET request to the API endpoint.
    """
    token = os.getenv("TOKEN")
    if not token:
        logger.critical("TOKEN environment variable not set. Please provide a valid token.")
        return

    if not validate_token(token):
        logger.critical("Invalid token provided. Please check your token.")
        return

    while True:
        try:
            headers = {"Authorization": token, "Content-Type": "application/json"}
            response = requests.get(API_ENDPOINT, headers=headers)
            response.raise_for_status()  # Raise an exception for non-200 status codes

            logger.info("Successfully kept alive.")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error occurred while keeping alive: {e}")
        except Exception as e:
            logger.critical(f"Unexpected error: {e}")

        time.sleep(60)  # Sleep for 60 seconds

if __name__ == "__main__":
    keep_alive()
