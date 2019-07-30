import argparse
import select
import socket
import sys
from utils import *

# Parse command line arguments
parser = argparse.ArgumentParser(description='PyChat Server Application')
parser.add_argument('-i', metavar='IP', dest='ip_addr', required=True,
                    help='The IP address of this machine')
parser.add_argument('-p', metavar='PORT', dest='port', required=True,
                    help='The port on which to receive data')
args = parser.parse_args()
ip_address = args.ip_addr
port = int(args.port)

listen_list = []

# Setup the socket
server_socket = create_socket(ip_address, port)
listen_list.append(server_socket)

while True:
    client_list, w_l, x_l = select.select(listen_list, [], [])
    for client in client_list:
        if client is server_socket:
            connection, address = client.accept()
            new_client = Client(connection)
            listen_list.append(new_client)
        else:
            message = client.socket.recv(1024)
