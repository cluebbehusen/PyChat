# System libraries
import argparse
import select
import socket
import sys

# Local libraries
from utils import *

# Parse command line arguments
parser = argparse.ArgumentParser(description='PyChat Client Application')
parser.add_argument('-i', metavar='IP', dest='ip_addr', required=True,
                    help='The IP address of the server')
parser.add_argument('-p', metavar='PORT', dest='port', required=False,
                    default=SERVER_PORT, help='The port of the server')
args = parser.parse_args()
ip_address = args.ip_addr
port = args.port

server_connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    server_connection_socket.connect((ip_address, port))
except ConnectionRefusedError:
    print('[!] Error: Failed to connect to server at the specificed IP.')
    sys.exit(1)

possible_input_streams = [sys.stdin, server_connection_socket]

print('[*] Successfully connected to server: {}:{}\n'.format(ip_address, port))

client_name = input('[*] Enter your name: ')
server_connection_socket.send(bytes(client_name, 'utf-8'))

while True:
    read_inputs, w_i, e_i = select.select(possible_input_streams, [], [])
    for input in read_inputs:
        if input == server_connection_socket:
            message_from_server = server_connection_socket.recv(1024)
            message_from_server = message_from_server.decode('utf-8')
            print(message_from_server, end='')
        else:
            client_message = sys.stdin.readline()
            sys.stdout.flush()
            server_connection_socket.send(bytes(client_message, 'utf-8'))
            sys.stdout.flush()
            erase_last_lines()
