# System libraries
import argparse
import select
import socket
import sys
import tkinter

# Local libaries
from utils import *

# Parse command line arguments
parser = argparse.ArgumentParser(description='PyChat GUI Client Application')
parser.add_argument('-i', metavar='IP', dest='ip_addr', required=False,
                    default=SERVER_IP, help='The IP address of the server')
parser.add_argument('-p', metavar='PORT', dest='port', required=False,
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

# Create the tkinter window
main_window = tkinter.Tk()
main_window.title('PyChat Client')
entry_label = tkinter.Label(main_window, text='Enter text here').pack()
main_window.mainloop()
