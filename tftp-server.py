#!/usr/bin/env python3
"""
TFTP Server Command.
"""

import sys
import os
import argparse
import tftp
import socket

TIMEOUT = 2
PORT = 6969
HOST = "localhost"

data_test = b'Hello2 Hello3 Hello4 Hello5 Hello6 Hello7 Hello8 Hello9 Hello10 Hello11'

parser = argparse.ArgumentParser(prog='tftp-server')
parser.add_argument('-p', '--port', type=int, default=PORT)
parser.add_argument('-t', '--timeout', type=int, default=TIMEOUT)
parser.add_argument('-c', '--cwd',  type=str, default='')
parser.add_argument('--thread', action='store_true')
args = parser.parse_args()

# change current working directory
if args.cwd != '': os.chdir(args.cwd)

# run main server loop
s1 = tftp.runServer((HOST, args.port), args.timeout, args.thread)

while True:
    data, addr = s1.recvfrom(1500)
    print('[{}:{}] client request: {}'.format(addr[0], addr[1], data))
    print('data =',data)
    opcode = data[0:2]
    rest = data[2:]
    opcode = int.from_bytes(opcode, byteorder='big')
    args = rest.split(b'\x00')
    filename = args[0].decode('ascii')
    mode = args[1].decode('ascii')
    print("Adresse = ",addr)
    print("Opcode = ",opcode)
    print("Args = ",args)
    print("Filename = ",filename)
    print("Mode = ",mode)
    if opcode == 1:
        tftp.recieve(addr, data)
    elif opcode == 2:
        tftp.send(addr, data)
    else:
        sys.exit(1)


    
# EOF
