"""
TFTP Module.
"""

import socket
import sys
import random

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

def send(addr_dest,  data, socket): #Pour envoyer
    print("Requête get vers l'adresse de destination = ", addr)
    pass

def recieve(addr_dest,  data, socket): #Pour recevoir
    print("Requête put vers l'adresse de destination = ", addr_dest)
    pass

########################################################################
#                             CLIENT SIDE                              #
########################################################################


def put(addr, filename, targetname, blksize, timeout):
    filename_byte = bytes(filename, 'utf-8')
    data = (b'\x00') + (b'\x02') + filename_byte + (b'\x00') + (b'octets\x00')
    s_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Requête put vers l'adresse ", addr, " avec comme premier paquet ",data)
    s_client.sendto(data, addr)   
    while True:
        data, addr = s_client.recvfrom(1024)
    s_client.close()

########################################################################


def get(addr, filename, targetname, blksize, timeout):
    filename_byte = bytes(filename, 'utf8')
    data = (b'\x00') + (b'\x01') + filename_byte + (b'\x00') + b'octets\x00'                                                        
    s_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Requête get vers l'adresse ", addr, " avec comme premier paquet ",data)
    s_client.sendto(data, addr)      
    while True:
        data, addr = s_client.recvfrom(1024)
    s_client.close()                                             

# EOF
