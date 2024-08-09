import socket
import time
import logging
import platform  # Import the platform module

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
    Keep the service alive by binding it to an open port.
    """
    # Your code for keeping the service alive
    pass

# Export functions to make them accessible from other modules
__all__ = ["keep_alive", "is_port_open", "scan_ports"]
