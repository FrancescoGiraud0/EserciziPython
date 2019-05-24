import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP = input("> Inserisci indirizzo IP server: ")

s.connect((IP, 65432))

strToSend = ''

while(True):
    strToSend = input("\n> Stringa da inviare ('0' per uscire): ")

    s.sendall(strToSend.encode())

    if(strToSend == '0'):
        break

    data = s.recv(4096).decode()

    print('\n> Server: "%s"' % (data))

    if(data == '0'):
        break

s.close()