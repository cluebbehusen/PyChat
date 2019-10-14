# System libraries
import argparse
import socket
import sys
from threading import Thread

# Local libraries
from utils import *

# Parse command line arguments
parser = argparse.ArgumentParser(description='PyChat Server Application')
parser.add_argument('-i', metavar='IP', dest='ip_addr', required=False,
                    default=SERVER_IP, help='The IP address of this machine')
parser.add_argument('-p', metavar='PORT', dest='port', required=False, type=int,
                    default=SERVER_PORT, help='The port of the server')
args = parser.parse_args()
ip_address = args.ip_addr
port = args.port

# Initialize a dictionary of client addresses
client_info = dict()

# Setup the main server socket
server_socket = create_socket(ip_address, port, True)

def handle_client(client):
    client.get_name()
    socket_active = True
    while socket_active:
        try:
            client_message = client.socket.recv(1024)
            if client_message:
                message = client_message.decode('utf-8')
                broadcast(message, client)
            else:
                print('[!] Lost connection to {}:{}'.format(
                      client.address[0], client.address[1]))
                socket_active = False
        except OSError:
            socket_active = False
    client.socket.close()

def broadcast(message, client):
    send_message = ('[{}]: {}'.format(client.name, message))
    for available_client in client_info:
        try:
            client_info[available_client].socket.send(bytes(send_message,
                                                            'utf-8'))
        except BrokenPipeError:
            print('[!] Lost connection to: {}:{}'.format(
                  client_info[available_client].address[0],
                  client_info[available_client].address[1]))
            available_client.close()
            client_info[available_client].thread.join()

if __name__ == '__main__':
    print('[*] Server Started: {}:{}\n'.format(ip_address, port))
    print('[*] Awaiting Connections...')
    while True:
        client_socket, client_address = server_socket.accept()
        print('[*] New Client Connected: {}:{}'.format(
              client_address[0], client_address[1]))
        client = Client(client_socket, client_address)
        client_thread = Thread(target=handle_client, args=(client,))
        client.thread = client_thread
        client.thread.start()
        client_info[client_socket] = client
