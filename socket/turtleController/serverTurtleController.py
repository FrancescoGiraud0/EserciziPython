import socket
import turtle

STEP = 10

commandsDictionary = {'F':turtle.forward, 'B': turtle.backward, 'R':turtle.right, 'L':turtle.left}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(("0.0.0.0", 5432))

s.listen()

connection, clientAddress = s.accept()

print("> Conesso con ", clientAddress)

turtle.speed(1)

while(True):
    commandString = connection.recv(4096).decode()

    if(commandString == 'E'):
        break

    for commandChar in commandString:
        if commandChar == 'F' or commandChar == 'B':
            commandsDictionary[commandChar](STEP)
        else:
            try:
                commandsDictionary[commandChar](90)
            except:
                print("\n> '%s' non è un comando definito" % commandChar)

    coordinateTurtle = '%f, %f' % (turtle.xcor(), turtle.ycor())

    connection.sendall(coordinateTurtle.encode())

connection.close()