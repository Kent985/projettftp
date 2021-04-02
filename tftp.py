"""
TFTP Module.
"""

import socket
import sys


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
            data_to_send = f.read(BLKSIZE) # BLKSIZE définit dans la section common routines (read prend en paramètre des bytes donc pas de conversion à faire)
            if not data_to_send:
                socket.sendto(b'over', addr_dest) #Temporaire, juste pour indiquer la fin de l'envoi 
                break
            data_bytes = bytes(data_to_send, 'utf-8') 
            socket.sendto(data_bytes, addr_dest) 
            ## Requêtes ACK a faire.
        f.close()
        socket.close()
        print("Requête get du fichier ", filename, "terminé")

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
    data_serv, addr_serv = s_client.recvfrom(blksize)
    while True:
        data_serv, addr_serv = s_client.recvfrom(blksize)
        print(data_serv.decode())
    s_client.close()

########################################################################


def get(addr, filename, targetname, blksize, timeout):
    filename_byte = bytes(filename, 'utf8')
    data = (b'\x00\x01') + filename_byte + (b'\x00octets\x00')                                                           
    s_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)                     
    s_client.bind(('localhost', random.randint(50000,60000)))
    s_client.sendto(data, addr)
    f = open("file_res","w+") # Nom du fichier à changer.
    while True:
        data_serv, addr_serv = s_client.recvfrom(blksize)
        print(data_serv.decode())
        if data_serv == b'over': # Temporaire, a changer.
            break
        f.write(data_serv.decode()) #Pour écrire dans le fichier 
    s_client.close()

# EOF
