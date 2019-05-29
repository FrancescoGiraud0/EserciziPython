import socket as sck

HOST = "localhost"
PORT = 5432
CLOSE_CONNECTION_STRING = 'Close'

s = sck.socket(sck.AF_INET, sck.SOCK_DGRAM)

while True:
    messageString = input("> Inserisci messaggio: ")
    s.sendto(messageString.encode(), (HOST, PORT))

    if(messageString == CLOSE_CONNECTION_STRING):
        break
    
    data, serverAddress = s.recvfrom(4096)

    print('> Server %s ha ricevuto: "%s"' %(serverAddress, data.decode()))

s.close()