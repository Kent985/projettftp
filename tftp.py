"""
TFTP Module.
"""

import socket
import sys

########################################################################
#                          COMMON ROUTINES                             #
########################################################################

########################################################################
#                             SERVER SIDE                              #
########################################################################


def runServer(addr, timeout, thread):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(addr)
    print(addr)
    return s

def send(addr, data): #Pour envoyer
    print("requête get vers l'addresse ", addr)
    pass

def recieve(addr, data): #Pour recevoir
    print("requête put vers l'addresse ", addr)
    pass

########################################################################
#                             CLIENT SIDE                              #
########################################################################


def put(addr, filename, targetname, blksize, timeout):
    addr_init = list(addr)
    addr_init[1] = 6969
    addr_init = tuple(addr_init)
    filename_byte = bytes(filename, 'utf-8')
    data = (b'\x00') + (b'\x02') + filename_byte + (b'\x00') + (b'octets\x00')
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(addr)
    s.sendto(data,addr_init)
    while True:
        data, addr = s.recvfrom(1024)
    s.close()

########################################################################


def get(addr, filename, targetname, blksize, timeout):
    addr_init = list(addr)
    addr_init[1] = 6969
    addr_init = tuple(addr_init)
    filename_byte = bytes(filename, 'utf8')
    data = (b'\x00') + (b'\x01') + filename_byte + (b'\x00') + b'octets\x00'                                                        
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(addr)
    s.sendto(data, addr_init)      
    while True:
        data, addr = s.recvfrom(1024)
    s.close()                                             

# EOF
