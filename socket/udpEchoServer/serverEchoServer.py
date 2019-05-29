import socket as sck

HOST = "0.0.0.0"
PORT = 5432
CLOSE_CONNECTION_STRING = 'Close'

s = sck.socket(sck.AF_INET, sck.SOCK_DGRAM)
s.bind((HOST, PORT))

while True:
    data, clientAddress = s.recvfrom(4096)
    
    print('> Client %s : "%s"' %(clientAddress, data.decode()))

    if(data.decode() == CLOSE_CONNECTION_STRING):
        break
    
    s.sendto(data, clientAddress)

s.close()