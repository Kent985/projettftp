"""
TFTP Module.
"""

import socket
import sys
import random
import os


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
    print(addr)
    return s

def send(addr_dest, data, socket, filename):  ##get
    print("Requête get du fichier ",filename," vers l'adresse de destination = ", addr_dest)
    ack = 1
    file_path = filename
    with open(file_path, mode='r') as f:
        while True:
            data_to_send = f.read(BLKSIZE)
            data_bytes = bytes(data_to_send, 'utf-8')
            data_paquet = b'\x03\x00' + ack.to_bytes(2,'big') + data_bytes
            print("Envoi du paquet",data_paquet)
            socket.sendto(data_paquet, addr_dest)
            if (len(data_paquet) < BLKSIZE):
                print("Fin de l'envoi")
                f.close() 
                socket.close()
                break
            data_ack, addr_ack = socket.recvfrom(BLKSIZE)
            ack+=1
        f.close()
        socket.close()
        print("Requête get du fichier ", filename, "terminé")

def recieve(addr_dest,  data, socket, filename): #put
    print("Requête put vers l'adresse de destination = ", addr_dest)
    socket.sendto(b'\x00\x04\x00\x00',addr_dest)
    numPaquet = 1
    filename_path = "server_files/" + filename
    with open(filename_path, "w") as f:
        while(True):
            data, addr = socket.recvfrom(1500)
            f.write(data.decode())
            socket.sendto(b'\x00\x04' + numPaquet.to_bytes(2, 'big'), addr_dest)
            if (len(data) != BLKSIZE):
                break
            numPaquet += 1        
    pass

########################################################################
#                             CLIENT SIDE                              #
########################################################################


def put(addr, filename, targetname, blksize, timeout):
    filename_byte = bytes(filename, 'utf-8')
    data = b'\x00\x02' + filename_byte + b'\x00octet\x00'
    s_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s_client.bind(('localhost', random.randint(50000,60000)))
    s_client.sendto(data,addr)
    data_serv, addr_serv = s_client.recvfrom(1500)
    if(data_serv != b'\x00\x04\x00\x00'):
        print("1 le paquet reçu n'a pas l'ack attendu !")
        return
    f = open(filename, "r")
    num_paquet = 1
    while True:
        content = f.read(BLKSIZE)
        print(content)
        if content == '':
            break
        content_bytes = bytes(content,'utf-8')
        s_client.sendto(content_bytes, addr_serv)
        rep_ack, _ = s_client.recvfrom(1500)
        
        ack_attendu = b'\x00\x04' + num_paquet.to_bytes(2, 'big')
        if(rep_ack != ack_attendu):
            print("2 le paquet reçu n'a pas l'ack attendu !")
            return
        num_paquet += 1
    f.close()
    s_client.close()

########################################################################


def get(addr, filename, targetname, blksize, timeout):
    filename_byte = bytes(filename, 'utf8')
    data = (b'\x00\x01') + filename_byte + (b'\x00octet\x00')                                                           
    s_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)                     
    s_client.bind(('localhost', random.randint(50000,60000)))
    s_client.sendto(data, addr)
    print("Paquet envoyé")
    f = open(filename,"w+") 
    ack = 1
    while True:
        data_serv, addr_serv = s_client.recvfrom(blksize)
        print("Reception du paquet", data_serv)
        data_to_write_bytes = data_serv[4:]
        data_to_write = data_to_write_bytes.decode()
        f.write(data_to_write)
        print("Ecriture de ", data_to_write)
        if data_serv == b'' or len(data_serv) < BLKSIZE:  
            ack_msg = (b'\x00\x04') + ack.to_bytes(2,byteorder='big')
            break
        ack_msg = (b'\x00\x04') + ack.to_bytes(2,byteorder='big')
        ack+=1
        s_client.sendto(ack_msg,addr_serv)
    s_client.close()

# EOF
