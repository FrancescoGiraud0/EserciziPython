# Giraudo Francesco
# Telefono senza fili
# Esercizio in cui bisogna trasmettere una parola da un host iniziale ad
# uno finale passando attraverso più host intermedi utilizzando il modulo
# socket di python.

import socket
import sys

PORT = 8080
NEXT_IP = "192.168.178.131"
CLOSE_CONNECTION_WORD = "EXIT"

# Instanzio server e client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def server_connection(server, port):
    """
    Funzione che data un'istanza di socket ed una porta
    crea un server, rimane in ascolto di un client e restituisce 
    l'oggetto connessione e l'indirizzo ip del client connesso.
    """
    server.bind(("0.0.0.0", port))
    server.listen()

    connection, ip_client = server.accept()

    return connection, ip_client

# Prende come attributo da terminale la modalità:
# c -> (client) solo client, quindi solo invio
# s -> (server) solo server, quindi solo ricezione
# a-> (actor) server e client, quindi prima riceve poi invia
mode = sys.argv[1]

server_connected = False
client_connected = False

while True:

    if mode == "s" or mode == "a":
        if not server_connected:
            connection, ip_client = server_connection(server, PORT) # Ascolto su porta PORT
            print("Stabilita connessione con %s" %ip_client[0])
            server_connected = True
        message_received = connection.recv(4096).decode()   # Ricezione messaggio e decodifica in stringa
        print("> %s : '%s'" %(ip_client, message_received))

        # Assegnazione alla variabile del messaggio da inviare per distinguere dalla
        # modalità "c" di solo invio dalla modalità "a" di ricezione ed invio
        message_toSend = message_received

    elif mode == "c":
        message_toSend = input("Inserire messaggio da inviare: ")
    else:
        print("Modalità %s non disponibile." %mode)
        break
    
    if mode == "c" or mode == "a":
        if not client_connected:
            print("Tentativo di connessione con %s sulla porta %s..." %(NEXT_IP,PORT))
            client.connect((NEXT_IP, PORT)) # Connessione con il server
            print("Connessione effetuata con successo.")
            client_connected = True
        print("Trasmissione messaggio a %s..." %NEXT_IP)
        client.sendall(message_toSend.encode())   # Invio del messaggio codificato in byte
        print("Messaggio inviato.\n")

    # Se il messaggio ricevuto / inviato contiene la CLOSE_CONNECTION_WORD chiudi connessione
    # ed esci dal ciclo
    if CLOSE_CONNECTION_WORD in message_toSend :
        print("Chiusura connessione...")
        break

server.close()
client.close()
