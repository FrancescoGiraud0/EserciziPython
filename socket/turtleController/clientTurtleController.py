import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

CLOSE_CONNECTION_STRING = 'E'
IP = input("> Inserisci indirizzo IP server turle: ")
PORT = int(input("> Inserisci PORTA server turle: "))

s.connect((IP, PORT))

strToSend = ''

while(True):
    commandString = input("\nE. Esci\nF. Avanti\nB. Indietro\nR. Ruota a dx di 90 gradi\nL. Ruota a sx di 90 gradi\n>>> ")

    commandString = commandString.upper()

    s.sendall(commandString.encode())

    if(commandString == CLOSE_CONNECTION_STRING):
        break

    coordinateTurtle = s.recv(4096).decode()

    if(len(coordinateTurtle) > 2):
        coordinate = coordinateTurtle.split(",")
        try:
            xcor = int(coordinate[0])
            ycor = int(coordinate[1])
            print('\n> Server: coordinate turtle (%d, %d)' % (xcor, ycor))
        except ValueError:
            print('\n> Errore conversione coordinate')

s.close()