# System libraries
import argparse
import select
import sys

# Local libraries
from utils import *

# Parse command line arguments
parser = argparse.ArgumentParser(description='PyChat Client Application')
parser.add_argument('-i', metavar='IP', dest='ip_addr', required=True,
                    help='The IP address of the server')
args = parser.parse_args()
ip_address = args.ip_addr
port = SERVER_PORT

server_connection_socket = create_socket(ip_address, port)

print('[*] Successfully connected to server.')
print('[*] Type messages at any point')

while True:
    ready_connections, w_l, x_l = select.select(connection_list, [], [])
    for connection in ready_connections:
        if connection is server_connection_socket:
            message = server_connection_socket.recv(1024)
            print(message.decode())
        else:
            pass
            message = input('Enter your message: ')
            server_connection_socket.sendall(message.encode())
