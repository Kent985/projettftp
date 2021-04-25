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
    print("\n")
    print("Requête get du fichier ",filename," vers l'adresse de destination = ", addr_dest)
    data = data.decode()
    data = data.split("\x00")
    try:
        blksize = data[4]
        blksize = int(blksize)
    except:
        blksize = 512
    print(blksize)
    ack = 1
    filename = "server_files/" + filename
    isExist = os.path.exists(filename)
    if (not isExist):
        print("Le fichier n'existe pas")
        ack_error_msg = b'\x00\x05\x00\x11' + bytes("FILE NOT FOUND", 'utf-8') + b'\x00'
        socket.sendto(ack_error_msg, addr_dest)
        socket.close()
        return
    with open(filename, mode='rb') as f:
        while True:
            data_bytes = f.read(blksize)
            print('data_bytes=',data_bytes)
            data_paquet = b'\x00\x03' + ack.to_bytes(2,'big') + data_bytes
            print("Envoi du paquet",data_paquet)
            socket.sendto(data_paquet, addr_dest)
<<<<<<< HEAD
            s_client.settimeout(timeout)
=======
>>>>>>> 0805ec0c9c3c90e8e7d8c00fdcc1bcefd60b67b3
            data_ack, addr_ack = socket.recvfrom(512) #ACK donc a ne pas changer
            print("Reception ACK:", data_ack)
            ack_msg = (b'\x00\x04') + ack.to_bytes(2,byteorder='big')
            if (ack_msg != data_ack):
                print("Le ACK attendu ne correspond pas au ACK reçu")
                ack_error_msg = b'\x00\x05\x00\x10' + bytes("ACK ERR", 'utf-8') + b'\x00'
                socket.sendto(ack_error_msg, addr_dest)
                break
            ack+=1
            if (len(data_bytes) < blksize):
                print("Fin de l'envoi")
                f.close() 
                socket.close()
                break
        f.close()
        socket.close()
        print("Requête get du fichier ", filename, "terminé")

def recieve(addr_dest,  data, socket, filename): #Put
    
    data = data.decode()                                                           #
    data = data.split("\x00")
    try:
        blksize = data[4]
        blksize = int(blksize)
    except:
        blksize = 512

    socket.sendto(b'\x00\x04\x00\x00',addr_dest)                                    #On envoie l'ACK0 

    numPaquet = 1

    with open(filename, "wb") as f:                                                 #On ouvre un fichier dans lequel écrire les dats qu'on reÃ§oit 
        while(True):

            data, addr = socket.recvfrom(1500)

            if( data[:2] != b'\x00\x03' ):                                           #On vérifie l'opcode du paquet 
                print("Erreur : L'opcode du paquet reçu n'est pas celui attendu")
                sys.exit(1)

            onlyData = data[4:]

            f.write(onlyData)

            socket.sendto(b'\x00\x04' + numPaquet.to_bytes(2, 'big'), addr_dest)    #On envoie un ACK avec le bon numéro de block 

            if( len(onlyData) != blksize ):                      #Si le data reçu est plus petit que blksize, c'est le dernier paquet... 
                socket.close()                                   #... donc on ferme la socket et on break
                break

            numPaquet += 1    
    pass


########################################################################
#                             CLIENT SIDE                              #
########################################################################


def put(addr, filename, targetname, blksize, timeout):
    
    if( targetname != '' ):
        fileToRead = targetname
    else:
        fileToRead = filename

    isExist = os.path.exists(fileToRead)
    if (not isExist):                                           #On vÃ©rifie que le fichier spÃ©cifiÃ© existe
        print("Le fichier n'existe pas")                         
        return
    
    filename_byte = bytes(fileToRead, 'utf-8')
    data = b'\x00\x02' + filename_byte + b'\x00octet\x00'       #Préparation du 'data' de WRQ 

    if (blksize != 512):                                        #Si 'blksize' != de la taille standard, ...
        blksize = str(blksize)
        data = data + b'blksize' + b'\x00' + blksize.encode('utf-8') + b'\x00'           #... On met le nouveau 'blksize' dans 'data'.
        blksize = int(blksize)

    s_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #On créé la 'socket' client 
    s_client.bind(('localhost', random.randint(50000,60000)))
    
    s_client.sendto(data,addr)                                  #Envoi de la demande WRQ.

    ack0_serv, addr_serv = s_client.recvfrom(1500)              #Réception du ACK0 envoyé par le port où envoyer le/les fichiers.

    if(ack0_serv[:2] != b'\x00\x04'):                           #Vérification de l'ACK. 
        print("Erreur : L'opcode du paquet reçu n'est pas celui attendu")
        sys.exit(1)

    f = open(fileToRead, "rb")
    block = 1
    num_paquet = 1

    while True:
        content = f.read(blksize)                                             #On prépare le 'data' du paquet à envoyer. 
        paquetFini = b'\x00\x03'+ block.to_bytes(2, 'big') + content   #On rajoute l'ACK et le 'block'.

        s_client.sendto(paquetFini, addr_serv)                                #On envoie le paquet.

        rep_ack, _ = s_client.recvfrom(1500)                                  #On reçoit l'ACK.
        ack_attendu = b'\x00\x04' + num_paquet.to_bytes(2, 'big')

        if(ack_attendu != rep_ack):                                           #On vérifie que l'ACK reçu est le même que l'ACK attendu (n° de block). 
            print("Erreur : L'opcode du paquet reçu n'est pas celui attendu")
            sys.exit(1)

        num_paquet += 1
        block += 1

        if( len(content) != blksize ):                                        #Si 'content' n'est pas plein (si c'est le dernier paquet), 
            break                                                             #on break à la fin du 'while'... 

    f.close()                                                                 #... Et on ferme le fichier et la 'socket' 
    s_client.close()

########################################################################


def get(addr, filename, targetname, blksize, timeout):
    filename_byte = bytes(filename, 'utf8')
    print("Blksize = ", blksize)
    data = (b'\x00\x01') + filename_byte + (b'\x00octet\x00')
    if (blksize != 512):                                        #Si 'blksize' != de la taille standard, ...
        blksize = str(blksize)
        data = data + b'blksize' + b'\x00' + blksize.encode('utf-8') + b'\x00'           #... On met le nouveau 'blksize' dans 'data'.
        blksize = int(blksize)                                                         
    s_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)                     
    s_client.bind(('localhost', random.randint(50000,60000)))
    s_client.sendto(data, addr)
    print("Paquet envoyé")
    if (targetname != ''):
        filename = targetname
    f = open(filename,"wb") 
    ack = 1
    while True:
        s_client.settimeout(timeout)
        data_serv, addr_serv = s_client.recvfrom(blksize+4)
        print("Reception du paquet", data_serv)
        if (data_serv[0:2] == b'\x00\x05'):
            printError(data_serv)
            sys.exit(1)
        data_to_write_bytes = data_serv[4:]
        f.write(data_to_write_bytes)
        print("Ecriture de ", data_to_write_bytes)
        ack_msg = (b'\x00\x04') + ack.to_bytes(2,byteorder='big')
        ack+=1
        s_client.sendto(ack_msg,addr_serv)
        if data_serv == b'' or len(data_serv) < blksize+4:  
            break
    f.close()
    s_client.close()
##########################################
#!/usr/bin/env python3
"TFTP Server Command."


import sys
import os
import argparse
import tftp
import socket
import random
import threading

TIMEOUT = 2
PORT = 6969
HOST = ""

parser = argparse.ArgumentParser(prog='tftp-server')
parser.add_argument('-p', '--port', type=int, default=PORT)
parser.add_argument('-t', '--timeout', type=int, default=TIMEOUT)
parser.add_argument('-c', '--cwd',  type=str, default='')
parser.add_argument('--thread', action='store_true')
args = parser.parse_args()

# change current working directory
if args.cwd != '': os.chdir(args.cwd)

# run main server loop
s1 = tftp.runServer((HOST, args.port), args.timeout, args.thread)

while True:
    print("En attente de demande")
    data, addr = s1.recvfrom(1500)
    sTemp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sTemp.bind(("127.0.0.1", 0))
    print('[{}:{}] client request: {}'.format(addr[0], addr[1], data))
    print('data =',data)
    opcode = data[0:2]
    rest = data[2:]
    print("Reste = ",rest)
    opcode = int.from_bytes(opcode, byteorder='big')
    args1 = rest.split(b'\x00')
    filename = args1[0].decode('ascii')
    print("Adresse = ", addr)
    print("Opcode = ",opcode)
    print("Filename = ",filename)
    print(args1)
    print("\n")
    if opcode == 1:
        if (args.thread == True):
            t1 = threading.Thread(target = tftp.send, args=(addr,data,sTemp,filename))
            t1.start()
        else:
            tftp.send(addr, data, sTemp, filename)
    elif opcode == 2:
        if (args.thread == True):
            t2 = threading.Thread(target = tftp.recieve, args = (addr,data,sTemp,filename))
            t2.start()
        else:
            tftp.recieve(addr, data, sTemp, filename)
        t1.join()
        t2.join()
    else:
        sys.exit(1)


    
# EOF


# EOF
