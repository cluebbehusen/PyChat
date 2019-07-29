import socket
import argparse

# Parse command line arguments
parser = argparse.ArgumentParser(description='PyChat Server Application')
parser.add_argument('-i', metavar='IP', dest='ip_addr', required=True,
                    help='The IP address of this machine')
parser.add_argument('-p', metavar='PORT', dest='port', required=True,
                    help='The port on which to receive data')
args = parser.parse_args()
ip_addr = args.ip_addr
port = args.port
