#!/usr/bin/env python3
"""
TFTP Server Command.
"""

import sys
import os
import argparse
import tftp
import socket
import random

TIMEOUT = 2
PORT = 6969
HOST = "localhost"

parser = argparse.ArgumentParser(prog='tftp-server')
parser.add_argument('-p', '--port', type=int, default=PORT)
parser.add_argument('-t', '--timeout', type=int, default=TIMEOUT)
parser.add_argument('-c', '--cwd',  type=str, default='')
parser.add_argument('--thread', action='store_true')
args = parser.parse_args()

# change current working directory
if args.cwd != '': os.chdir(args.cwd)

# run main server loop
s = tftp.runServer((HOST, args.port), args.timeout, args.thread)

while True:
    data, addr = s.recvfrom(1500)
    
    sTemp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sTemp.bind(("localhost", random.randint(50000,60000)))
    
    print('[{}:{}] client request: {}'.format(addr[0], addr[1], data))
    print('data =',data)
    tftp.put(addr, "", "", 0, 0)
    opcode = data[0:2]
    rest = data[2:]
    opcode = int.from_bytes(opcode, byteorder='big')
    args = rest.split(b'\x00')
    filename = args[0].decode('ascii')
    print("Opcode = ",opcode)
    print("Args = ",args)
    print("Filename = ",filename)
    print("Mode = ",mode)
    
# EOF
