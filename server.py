# System libraries
import argparse
import select
import socket
import sys

# Local libraries
from utils import *

# Parse command line arguments
parser = argparse.ArgumentParser(description='PyChat Server Application')
parser.add_argument('-i', metavar='IP', dest='ip_addr', required=True,
                    help='The IP address of this machine')
args = parser.parse_args()
ip_address = args.ip_addr
port = SERVER_PORT

# Initialize a list to hold all client connections
connection_list = []

# Setup the main server socket
server_socket = create_socket(ip_address, port)
connection_list.append(server_socket)

while True:
    # Use the select library to only listen to sockets that are ready to have
    #     data read from them
    client_list, w_l, x_l = select.select(connection_list, [], [])
    for client in client_list:
        # Check if the connection is new
        if client is server_socket:
            connection, address = client.accept()
            new_client = Client(connection)
            connection_list.append(new_client)
        # If the connection is not new, data has been received, handle it
        else:
            message = client.socket.recv(1024)
            for connection in connection_list:
                if connection is not server_socket:
                    connection.socket.sendall(message)
