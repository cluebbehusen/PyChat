# System libraries
import argparse
import socket
import sys
from threading import Thread

# Local libraries
from utils import *

# Parse command line arguments
parser = argparse.ArgumentParser(description='PyChat Server Application')
parser.add_argument('-i', metavar='IP', dest='ip_addr', required=True,
                    help='The IP address of this machine')
args = parser.parse_args()
ip_address = args.ip_addr
port = SERVER_PORT

# Initialize a dictionary of client addresses
clients_info = dict()

# Setup the main server socket
server_socket = create_socket(ip_address, port, True)

def handle_client(client):
    name = client.recv(1024).decode('utf-8')
    welcome_message = ('Welcome, {}'.format(name))
    client.send(bytes(welcome_message, 'utf-8'))

if __name__ == '__main__':
    while True:
        new_client, new_client_address = server_socket.accept()
        print(new_client)
        print(type(new_client))
        print('[*] New Client Connected: {}:{}'.format(
              new_client_address[0], new_client_address[1]))
        new_client.send(bytes('Enter your name: ', 'utf-8'))
        clients_info[new_client] = new_client_address
        Thread(target=handle_client, args=(new_client,)).start()
