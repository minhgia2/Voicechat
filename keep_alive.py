import time
import requests
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

API_ENDPOINT = "https://canary.discord.com/api/v9/users/@me/channels"

def keep_alive():
    while True:
        try:
            headers = {"Authorization": os.getenv("TOKEN"), "Content-Type": "application/json"}
            response = requests.get(API_ENDPOINT, headers=headers)
            response.raise_for_status()  # Raise an exception for non-200 status codes

            logger.info("Successfully kept alive.")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error occurred while keeping alive: {e}")
        except KeyError:
            logger.error("TOKEN environment variable not set. Please provide a valid token.")

        time.sleep(600)

if __name__ == "__main__":
    keep_alive()
