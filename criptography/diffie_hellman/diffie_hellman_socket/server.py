"""
Francesco Giraudo
Classe 5^A ROB
Diffie Hellman cipher implementation (Server).
"""

import random
import socket

N = 9973 # This must be a prime number
g = 1567

def client_connection():
    """
    Function that manage client connections.
    It returns socket and connection object.
    """
    # Socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind
    s.bind(("0.0.0.0", 1984))
    # Listening for clients
    s.listen()

    conn, client_address = s.accept()

    print(f'> {client_address[0]} successfully connected')

    return s, conn

if __name__ == "__main__":
    s, conn = client_connection()
    
    a = random.randint(1,N) # Generate a random int from 1 to N
    A = (g**a)%N            # Value to send to the client (public)

    print(f'N = {N} | g = {g} | A = {A} | a = {a}\n\nSending A value...')

    conn.sendall(f'{A}'.encode()) # Send A value

    print('Waiting B value...')
    data_recv = conn.recv(4096).decode() # Receive B value
    
    try:
        B = int(data_recv)
    except TypeError:
        print('Error: received not a number.')
        B = 0
    
    print(f'Received B = {B}')
    
    key = (B**a)%N # Compute the key

    print(f'\nKEY VALUE: {key}')

    conn.close() # Close connection
    s.close()   # Close socket
