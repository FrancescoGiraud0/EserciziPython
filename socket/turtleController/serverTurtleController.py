import socket
import turtle

CLOSE_CONNECTION_STRING = 'E'
STEP = 10

commandsDictionary = {'F': turtle.forward,
                      'B': turtle.backward,
                      'R': turtle.right,
                      'L': turtle.left}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(("0.0.0.0", 5432))

s.listen()

connection, clientAddress = s.accept()

print("> Conesso con ", clientAddress)

turtle.speed(1)

while(True):
    # Riceve bytes che converte in stringa di caratteri maiuscoli
    commandString = connection.recv(4096).decode().upper()

    print("> Ricevuto: ", commandString)

    if(commandString == CLOSE_CONNECTION_STRING):
        break

    for commandChar in commandString:
        if commandChar == 'F' or commandChar == 'B':
            try:
                commandsDictionary[commandChar](STEP)
            except KeyError:
                print("\n> '%s' non è un comando definito" % commandChar)
        else:
            try:
                commandsDictionary[commandChar](90)
            except KeyError:
                print("\n> '%s' non è un comando definito" % commandChar)

    coordinateTurtle = '%d, %d' % (turtle.xcor(), turtle.ycor())

    connection.sendall(coordinateTurtle.encode())

connection.close()