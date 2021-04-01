"""
TFTP Module.
"""

import socket
import sys
import random

########################################################################
#                          COMMON ROUTINES                             #
########################################################################


HOST = "localhost"
PORT = random.randint(50000,60000)
s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s2.bind((HOST,PORT))


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
