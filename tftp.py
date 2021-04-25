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

def send(addr_dest, data, socket, filename, timeout):  ##get
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
    filename = filename
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
            socket.settimeout(timeout)
            try:
                data_ack, _ = socket.recvfrom(512) #ACK donc a ne pas changer
            except:
                print("Timeout exceeded")
                timeout_error_msg = b'\x00\x05\x00\x05' + bytes("TIMEOUT", 'utf-8') + b'\x00'
                socket.sendto(timeout_error_msg, addr_dest)
                break
            socket.settimeout(None)
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

def recieve(addr_dest,  data, socket, filename, timeout): #Put
    
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
            socket.settimeout(timeout)
            try:
                data, _ = socket.recvfrom(1500)
            except:
                print("Timeout exceeded")
                timeout_error_msg = b'\x00\x05\x00\x05' + bytes("TIMEOUT", 'utf-8') + b'\x00'
                socket.sendto(timeout_error_msg, addr_dest)
                break
            
            socket.settimeout(None)

            if( data[:2] != b'\x00\x03' ):                                           #On vérifie l'opcode du paquet 
                print("Erreur : L'opcode du paquet reçu n'est pas celui attendu")
                sys.exit(1)

            onlyData = data[4:]

            f.write(onlyData)

            socket.sendto(b'\x00\x04' + numPaquet.to_bytes(2, 'big'), addr_dest)    #On envoie un ACK avec le bon numéro de block 

            if( len(onlyData) != blksize ):                      #Si le data reçu est plus petit que blksize, c'est le dernier paquet...                                #... donc on ferme la socket et on break
                break

            numPaquet += 1  
    socket.close()
    pass


########################################################################
#                             CLIENT SIDE                              #
########################################################################


def put(addr, filename, targetname, blksize, timeout):
    
    if( targetname != '' ):
        fileToRead = targetname
    else:
        fileToRead = filename

    isExist = os.path.exists(filename)
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

    ack0_serv, addr_serv = s_client.recvfrom(1500)     #Réception du ACK0 envoyé par le port où envoyer le/les fichiers.

    if(ack0_serv[:2] != b'\x00\x04'):                           #Vérification de l'ACK. 
        print("Erreur : L'opcode du paquet reçu n'est pas celui attendu")
        sys.exit(1)

    f = open(filename, "rb")
    block = 1
    num_paquet = 1

    while True:
        content = f.read(blksize)                                             #On prépare le 'data' du paquet à envoyer. 
        paquetFini = b'\x00\x03'+ block.to_bytes(2, 'big') + content   #On rajoute l'ACK et le 'block'.

        s_client.sendto(paquetFini, addr_serv)                                #On envoie le paquet.
        s_client.settimeout(timeout)
        try:
            rep_ack, _ = s_client.recvfrom(1500)
        except:
            print("Timeout exceeded")
            break
        s_client.settimeout(None)
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
    if (filename != ""):
        filename = targetname
    f = open(filename,"wb") 
    ack = 1
    while True:
        s_client.settimeout(timeout)
        try:
            data_serv, addr_serv = s_client.recvfrom(blksize+4)
        except:
            print("Timeout exceeded")
            break
        s_client.settimeout(None)
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

# EOF
