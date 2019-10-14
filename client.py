# System libraries
import argparse
import select
import socket
import sys

# Local libraries
from utils import *

# Parse command line arguments
parser = argparse.ArgumentParser(description='PyChat Client Application')
parser.add_argument('-i', metavar='IP', dest='ip_addr', required=False,
                    default=SERVER_IP, help='The IP address of the server')
parser.add_argument('-p', metavar='PORT', dest='port', required=False, type=int,
                    default=SERVER_PORT, help='The port of the server')
args = parser.parse_args()
ip_address = args.ip_addr
port = args.port

# Create a socket to read from the main server and ensure connection is possible
server_connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    server_connection_socket.connect((ip_address, port))
except ConnectionRefusedError:
    print('[!] Error: Failed to connect to server at the specificed IP.')
    sys.exit(1)

# A list for use with the select function
possible_input_streams = [sys.stdin, server_connection_socket]

print('[*] Successfully connected to server: {}:{}\n'.format(ip_address, port))

# Collect the client's name
client_name = input('[*] Enter your name: ')
server_connection_socket.send(bytes(client_name, 'utf-8'))

while True:
    try:
        # Use the select function to read when one of the two possible input
        #     streams are ready to have data read from them
        read_inputs, w_i, e_i = select.select(possible_input_streams, [], [])
        for input in read_inputs:
            if input == server_connection_socket:
                message_from_server = server_connection_socket.recv(1024)
                message_from_server = message_from_server.decode('utf-8')
                print(message_from_server, end='')
            else:
                client_message = sys.stdin.readline()
                server_connection_socket.send(bytes(client_message, 'utf-8'))
                erase_last_lines()
    except KeyboardInterrupt:
        print('[!] Closing connection to server.')
        server_connection_socket.close()
        sys.exit(0)
