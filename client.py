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

try:
    server_connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_connection_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_connection_socket.connect((ip_address, port))
except Exception as e:
    print('[!] Error: Failed to set up server connection')
    print(e)
    sys.exit(1)

print('Successfully connected to server.')
print('Type messages at any point')

connection_list = []

connection_list.append(sys.stdin)
connection_list.append(server_connection_socket)

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
