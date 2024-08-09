import sys
import signal
import atexit
import logging

logger = logging.getLogger(__name__)

# Set the default timeout to 3600 seconds (1 hour)
DEFAULT_TIMEOUT = 3600

# Global variable to track the keep-alive timer
keep_alive_timer = None

def keep_alive(url=None, path="/", port=80, timeout=DEFAULT_TIMEOUT):
    """
    Keep the service alive by sending a GET request to the specified URL at regular intervals.

    Args:
        url (str): The URL to send the keep-alive request to.
        path (str): The path to append to the URL.
        port (int): The port number to use for the request.
        timeout (int): The interval in seconds between keep-alive requests.
    """
    global keep_alive_timer

    # Validate the timeout value
    if timeout <= 0:
        logger.warning("Timeout value must be greater than 0. Using default value.")
        timeout = DEFAULT_TIMEOUT

    # Define the request headers
    headers = {
        "User-Agent": "Keep-Alive/1.0",
        "Content-Type": "application/json",
    }

    # Define the request data
    data = {"status": "online"}

    # Define the request method
    method = "GET"

    # Define the request function
    def request():
        try:
            response = requests.request(method, url + path, headers=headers, data=json.dumps(data))
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send keep-alive request: {e}")

    # Define the keep-alive function
    def keep_alive_func():
        nonlocal keep_alive_timer
        while True:
            try:
                request()
            except Exception as e:
                logger.error(f"Keep-alive request failed: {e}")
            finally:
                keep_alive_timer = timer(timeout, keep_alive_func)

    # Register the keep-alive function to run on exit
    atexit.register(keep_alive_func)

    # Start the keep-alive function
    keep_alive_func()

def stop_keep_alive():
    """
    Stop the keep-alive timer and requests.
    """
    global keep_alive_timer
    if keep_alive_timer:
        keep_alive_timer.cancel()
        keep_alive_timer = None

# Register a signal handler to stop the keep-alive timer when the process receives a SIGTERM signal
def signal_handler(sig, frame):
    stop_keep_alive()
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)

# Import the Timer class from the threading module
try:
    from threading import Timer
except ImportError:
    logger.error("threading.Timer is not available in this Python version.")
else:
    timer = Timer.start_new_thread
