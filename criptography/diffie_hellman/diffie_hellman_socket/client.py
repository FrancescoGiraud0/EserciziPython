"""
Francesco Giraudo
Classe 5^A ROB
Diffie Hellman cipher implementation (Client).
"""

import random
import socket

# Address and listen port of the server
IP_ADDRESS = '192.168.0.104'
PORT = 1984

N = 9973 # This must be a prime number
g = 1567

# socket object instantiation (IPv4, TCP)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connection with the server
s.connect((IP_ADDRESS, PORT))

if __name__ == "__main__":
    b = random.randint(1,N) # Generate a random int from 1 to N
    B = (g**b)%N    # Value to send to the server (public)

    print('Waiting for A value...')
    data_recv = s.recv(4096).decode() # The client wait for A value

    print(f'N = {N} | g = {g} | B = {B} | B = {b}\n')
    
    try:
        A = int(data_recv) # String conversion to number
    except TypeError:
        print('Error: received not a number.')
        A = 0
    
    print(f'Received A = {A}')

    print('\nSending B value...')

    s.sendall(f'{B}'.encode()) # Send B value to the server
    
    key = (A**b)%N # Compute the key

    print(f'\nKEY VALUE = {key}')

    s.close() # Close the socket
