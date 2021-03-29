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

########################################################################
#                             CLIENT SIDE                              #
########################################################################


def put(addr, filename, targetname, blksize, timeout):
    while True:
        data, addr = s2.recvfrom(blksize)
    pass

########################################################################


def get(addr, filename, targetname, blksize, timeout):
    while True:
        data, addr = s2.recvfrom(blksize)
    pass

# EOF
