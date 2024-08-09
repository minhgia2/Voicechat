import socket
import time
import logging
import platform
from flask import Flask
from threading import Thread

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def scan_ports(host, start_port, end_port):
    """
    Scan for open ports within the specified range.
    """
    for port in range(start_port, end_port + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(2)
                result = sock.connect_ex((host, port))
                if result == 0:
                    logger.info(f"Open port detected: {port}")
                    return port  # Return the open port
                else:
                    logger.debug(f"Port {port} is closed.")
        except socket.error as e:
            logger.error(f"Error scanning port {port}: {e}")

def is_port_open(host, port):
    """
    Check if a port is open on the specified host.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(2)
        result = sock.connect_ex((host, port))
        return result == 0

def keep_alive():
    """
    Keep the service alive by binding it to an open port and running a Flask server.
    """
    # Your code for keeping the service alive
    app = Flask('')

    @app.route('/')
    def main():
        return '<meta http-equiv="refresh" content="0; URL=https://phantom.fr.to/support"/>'

    def run():
        app.run(host="0.0.0.0", port=8080)

    # Scan for an open port and bind the service to it
    open_port = scan_ports("0.0.0.0", 8000, 8999)
    if open_port is None:
        logger.critical("No open ports detected. Please bind your service to at least one port.")
        return

    # Start the Flask server in a separate thread
    server = Thread(target=run)
    server.start()

# Export functions to make them accessible from other modules
__all__ = ["keep_alive", "is_port_open", "scan_ports"]
