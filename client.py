import argparse

from utils import *

# Parse command line arguments
parser = argparse.ArgumentParser(description='PyChat Client Application')
parser.add_argument('-i', metavar='IP', dest='ip_addr', required=True,
                    help='The IP address of the server')
args = parser.parse_args()
ip_address = args.ip_addr
port = SERVER_PORT
