import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(("0.0.0.0", 65432))

s.listen()

conn, clientAddress = s.accept()

print("> Conesso", conn)

while(True):
    data = conn.recv(4096).decode()

    if(data == '0'):
        break

    print('\n> Client %s: %s' %(clientAddress, data))

    strToSend = input("\n> Stringa da inviare ('0' per uscire): ")

    conn.sendall(strToSend.encode())

    if(strToSend == '0'):
        break

conn.close()