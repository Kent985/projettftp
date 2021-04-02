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
    pass

def recieve(addr, data): #Pour recevoir
    pass

########################################################################
#                             CLIENT SIDE                              #
########################################################################


def put(addr, filename, targetname, blksize, timeout): #Faire la même chose que en get (se référer en bas de la feuille de projet techno, ou bien la rfc)
    filename_byte = bytes(filename, 'utf-8')
    data = (b'\x00') + (b'\x02') + filename_byte + (b'\x00') + (b'octets\x00')
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(data,addr)
    pass

########################################################################


def get(addr, filename, targetname, blksize, timeout):
    print(blksize)
    filename_byte = bytes(filename, 'utf8')
    data = (b'\x00') + (b'\x01') + filename_byte + (b'\x00') + b'octets\x00' #J'ai supprimé les boucles, car ces fonctions ne sont que coté client 
    print(data)                                                              # (c'était marqué en haut mais j'avais pas vu, et ces fonctions sont appelés par tftp-client.py)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)                     #J'ai donc fais deux fonctions, send et put, qui (je suis pas sur du tout) 
    s.sendto(data, addr)                                                     #feront les boucles pour envoyer/recevoir des données.
    pass

# EOF
