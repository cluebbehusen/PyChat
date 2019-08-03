# System libraries
import socket
import sys

MAX_CLIENTS = 5
SERVER_PORT = 47774

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
