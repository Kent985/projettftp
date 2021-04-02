"""
TFTP Module.
"""

import socket
import sys
import random


########################################################################
#                          COMMON ROUTINES                             #
########################################################################


BLKSIZE = 10 # Temporaire à changer


########################################################################
#                             SERVER SIDE                              #
########################################################################


def runServer(addr, timeout, thread):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(addr)
    print(addr)
    return s

def send(addr_dest,  data, socket, filename): #Pour envoyer
    print("Requête get du fichier ",filename," vers l'adresse de destination = ", addr_dest)
    with open(filename, mode='r') as f:
        while True:
            data_to_send = f.read(BLKSIZE)
            if not data_to_send:
                socket.sendto(b'over', addr_dest)
                break
            data_bytes = bytes(data_to_send, 'utf-8')
            socket.sendto(data_bytes, addr_dest)
            ## Requêtes ACK a faire.
        f.close()
        socket.close()
        print("Requête get du fichier ", filename, "terminé")


def recieve(addr_dest,  data, socket): #Pour recevoir
    print("Requête put du fichier", filename," vers l'adresse de destination = ", addr_dest)

########################################################################
#                             CLIENT SIDE                              #
########################################################################


def put(addr, filename, targetname, blksize, timeout):
    filename_byte = bytes(filename, 'utf-8')
    data = (b'\x00') + (b'\x02') + filename_byte + (b'\x00') + (b'octets\x00')
    s_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s_client.bind(('localhost', random.randint(50000,60000)))
    s_client.sendto(data,addr)
    data_serv, addr_serv = s_client.recvfrom(blksize)
    while True:
        data_serv, addr_serv = s_client.recvfrom(blksize)
        print(data_serv.decode())
    s_client.close()

########################################################################


def get(addr, filename, targetname, blksize, timeout):
    filename_byte = bytes(filename, 'utf8')
    data = (b'\x00') + (b'\x01') + filename_byte + (b'\x00') + b'octets\x00'                                                           
    s_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)                     
    s_client.bind(('localhost', random.randint(50000,60000)))
    s_client.sendto(data, addr)
    f = open("file_res","w+") # Nom du fichier à changer.
    while True:
        data_serv, addr_serv = s_client.recvfrom(blksize)
        print(data_serv.decode())
        if data_serv == b'over': # Temporaire, a changer par ACK.
            break
        f.write(data_serv.decode())
    s_client.close()

# EOF
