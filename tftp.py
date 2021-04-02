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

def send(addr_dest,  data, socket): #Pour envoyer
    print("Requête get vers l'adresse de destination = ", addr_dest)
    pass

def recieve(addr_dest,  data, socket): #Pour recevoir
    print("Requête put vers l'adresse de destination = ", addr_dest)
    socket.sendto(b'\x00\x04\x00\x00',addr_dest)
    num_Paquet = 1
    with open(filename, "w") as f:
        while(True):
            data, addr = socket.recvfrom(1500)
            f.write(data)
            socket.sendto(b'\x00\x04' + (x).to_bytes(4, 'big'), addr_dest)
            if (len(data) != 512):
                break
            x += 1        
    pass

########################################################################
#                             CLIENT SIDE                              #
########################################################################


def put(addr, filename, targetname, blksize, timeout):
    filename_byte = bytes(filename, 'utf-8')
    data = b'\x00\x02' + filename_byte + b'\x00octets\x00'
    s_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s_client.bind(localhost, random.randint(50000,60000))
    s_client.sendto(data,addr)
    pass

########################################################################


def get(addr, filename, targetname, blksize, timeout):
    filename_byte = bytes(filename, 'utf8')
    data = b'\x00\x01' + filename_byte + b'\x00octets\x00' 
    print(data)                                                             
    s_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)                     
    s_client.bind(localhost, random.randint(50000,60000))
    s_client.sendto(data, addr)                                                    
    pass

# EOF
