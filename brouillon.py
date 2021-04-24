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


BLKSIZE = 512 # Temporaire à changer

def printError(message_bytes):
    opcode = message_bytes[2:4]
    opcode = int.from_bytes(opcode, byteorder='big')
    message = message_bytes[4:]
    message = message.decode()
    print("ERROR NB", opcode, ": ",message)




########################################################################
#                             SERVER SIDE                              #
########################################################################


def runServer(addr, timeout, thread):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(addr)
    print(addr)
    return s

def send(addr_dest, data, socket, filename):  ##get
    print("Requête get du fichier ",filename," vers l'adresse de destination = ", addr_dest)
    ack = 1
    print(filename)
    isExist = os.path.exists(filename)
    print(isExist)
    if (not isExist):
        print("Le fichier n'existe pas")
        ack_error_msg = b'\x00\x05\x00\x11' + bytes("FILE NOT FOUND", 'utf-8') + b'\x00'
        socket.sendto(ack_error_msg, addr_dest)
        socket.close()
        return
    with open(filename, mode='r') as f:
        while True:
            data_to_send = f.read(BLKSIZE)
            data_bytes = bytes(data_to_send, 'utf-8')
            data_paquet = b'\x00\x03' + ack.to_bytes(2,'big') + data_bytes
            print("Envoi du paquet",data_paquet)
            socket.sendto(data_paquet, addr_dest)
            data_ack, addr_ack = socket.recvfrom(BLKSIZE)
            ack_msg = (b'\x00\x08') + ack.to_bytes(2,byteorder='big')
            if (ack_msg != data_ack):
                print("Le ACK attendu ne correspond pas au ACK reçu")
                ack_error_msg = b'\x00\x05\x00\x10' + bytes("ACK ERR", 'utf-8') + b'\x00'
                socket.sendto(ack_error_msg, addr_dest)
                break
            ack+=1
            if (len(data_paquet) < BLKSIZE):
                print("Fin de l'envoi")
                f.close() 
                socket.close()
                break
        f.close()
        socket.close()
        print("Requête get du fichier ", filename, "terminé")

def recieve(addr_dest,  data, socket, filename): #Put
    socket.sendto(b'\x00\x04\x00\x00',addr_dest)
    numPaquet = 1
    with open(filename, "w") as f:
        while(True):
            data, addr = socket.recvfrom(1500)
            onlyData = data[4:]
            f.write(onlyData.decode())
            socket.sendto(b'\x00\x04' + numPaquet.to_bytes(2, 'big'), addr_dest)
            if (len(onlyData) < 512):
                socket.close()
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

    ack0_serv, addr_serv = s_client.recvfrom(1500)
    f = open(filename, "r")
    block = 1
    num_paquet = 1
    while True:
        content = f.read(BLKSIZE)
        print(content)
        content_bytes = bytes(content,'utf-8')
        paquetFini = b'\x00\x03'+ block.to_bytes(2, 'big') + content_bytes
        s_client.sendto(paquetFini, addr_serv)
        rep_ack, _ = s_client.recvfrom(1500)
        ack_attendu = b'\x00\x04' + num_paquet.to_bytes(2, 'big')
        num_paquet += 1
        block += 1
        if content == '':
            break
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
        print()
        if (data_serv[0:2] == b'\x00\x05'):
            printError(data_serv)
            sys.exit(1)
        data_to_write_bytes = data_serv[4:]
        data_to_write = data_to_write_bytes.decode()
        f.write(data_to_write)
        print("Ecriture de ", data_to_write)
        ack_msg = (b'\x00\x04') + ack.to_bytes(2,byteorder='big')
        ack+=1
        s_client.sendto(ack_msg,addr_serv)
        if data_serv == b'' or len(data_serv) < BLKSIZE:  
            break
    s_client.close()

# EOF
