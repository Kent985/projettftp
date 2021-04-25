#!/usr/bin/env python3
"TFTP Server Command."


import sys
import os
import argparse
import tftp
import socket
import random
import threading

TIMEOUT = 2
PORT = 6969
HOST = ""

parser = argparse.ArgumentParser(prog='tftp-server')
parser.add_argument('-p', '--port', type=int, default=PORT)
parser.add_argument('-t', '--timeout', type=int, default=TIMEOUT)
parser.add_argument('-c', '--cwd',  type=str, default='')
parser.add_argument('--thread', action='store_true')
argscmd = parser.parse_args()

# change current working directory
if argscmd.cwd != '': os.chdir(args.cwd)

# run main server loop
s1 = tftp.runServer((HOST, argscmd.port), argscmd.timeout, argscmd.thread)

while True:
    print("En attente de demande")
    data, addr = s1.recvfrom(1500)
    sTemp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sTemp.bind(("127.0.0.1", 0))
    print('[{}:{}] client request: {}'.format(addr[0], addr[1], data))
    print('data =',data)
    opcode = data[0:2]
    rest = data[2:]
    print("Reste = ",rest)
    opcode = int.from_bytes(opcode, byteorder='big')
    args = rest.split(b'\x00')
    filename = args[0].decode('ascii')
    print("Adresse = ", addr)
    print("Opcode = ",opcode)
    print("Filename = ",filename)
    print(args)
    print("\n")
    if opcode == 1:
        if (argscmd.thread == True):
            print("Threading activé")
            t1 = threading.Thread(target = tftp.send, args=(addr,data,sTemp,filename))
            t1.start()
        else:
            tftp.send(addr, data, sTemp, filename)
    elif opcode == 2:
        if (argscmd.thread == True):
            print("Threading activé")
            t2 = threading.Thread(target = tftp.recieve, args = (addr,data,sTemp,filename))
            t2.start()
        else:
            tftp.recieve(addr, data, sTemp, filename)
        t1.join()
        t2.join()
    else:
        sys.exit(1)


    
# EOF
