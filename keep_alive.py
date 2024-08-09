import socket
import time
import logging

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

def keep_alive():
    """
    Keep the service alive by binding it to an open port.
    """
    host = "0.0.0.0"  # Bind to all interfaces
    start_port = 8000  # Start port number
    end_port = 8999  # End port number

    # Scan for open ports
    scan_ports(host, start_port, end_port)

    # Bind the service to an open port
    open_ports = [port for port in range(start_port, end_port + 1) if is_port_open(host, port)]
    if not open_ports:
        logger.critical("No open ports detected. Please bind your service to at least one port.")
        return

    port = open_ports[0]
    logger.info(f"Binding service to port {port}")
    # Bind the service to the selected port (implementation specific)

if __name__ == "__main__":
    keep_alive()
