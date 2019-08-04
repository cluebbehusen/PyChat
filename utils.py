# System libraries
import socket
import sys

MAX_CLIENTS = 5
SERVER_PORT = 47774
CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'

def erase_last_lines(n=1):
    for _ in range(n):
        sys.stdout.write(CURSOR_UP_ONE)
        sys.stdout.write(ERASE_LINE)

def create_socket(ip_address, port, server=False):
    """Creates and returns a nonblocking TCP socket"""
    try:
        return_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return_socket.bind((ip_address, port))
        if server:
            return_socket.listen(MAX_CLIENTS)
        return return_socket
    except Exception as e:
        print('[!] An error occurred while setting up the socket.')
        print(e)
        sys.exit(1)

class Client:

    def __init__(self, socket, address):
        self.socket = socket
        self.address = address
        self.name = None

    def get_name(self):
        """Gets the clients name and sends a welcome message"""
        # At this point, the client should be entering their name
        name = self.socket.recv(1024).decode('utf-8')
        name = name.strip()
        self.name = name
        # Upon receiving the name, send a welcome message
        welcome_message = ('Welcome, {}'.format(self.name))
        self.socket.send(bytes(welcome_message, 'utf-8'))
