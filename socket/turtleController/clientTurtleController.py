import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP = input("> Inserisci indirizzo IP server turle: ")
PORT = int(input("> Inserisci PORTA server turle: "))

s.connect((IP, PORT))

strToSend = ''

while(True):
    commandString = input("\nE. Esci\nF. Avanti\nB. Indietro\nR. Ruota a dx di 90 gradi\nL. Ruota a sx di 90 gradi\n>>> ")

    commandString = commandString.upper()

    s.sendall(commandString.encode())

    if(commandString == 'E'):
        break

    coordinateTurtle = s.recv(4096).decode()

    print('\n> Server: coordinate turtle (%s)' % (coordinateTurtle))

    if(coordinateTurtle == 'E'):
        break

s.close()