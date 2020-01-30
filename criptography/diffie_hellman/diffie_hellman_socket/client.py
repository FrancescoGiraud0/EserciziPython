"""
Francesco Giraudo
Classe 5^A ROB
Diffie Hellman cipher implementation (Client).
"""

import random
import socket

IP_ADDRESS = 'localhost'
PORT = 1984
N = 9973 #N.B. N deve essere primo
g = 1567

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP_ADDRESS, PORT))

if __name__ == "__main__":
    b = random.randint(1,N)
    B = (g**b)%N

    print('Attending A value...')
    data_recv = s.recv(4096).decode()

    print(f'N = {N} | g = {g} | B = {B} | B = {b}\n')
    
    try:
        A = int(data_recv)
    except TypeError:
        print('Error: received not a number')
        A = 0
    
    print(f'Received A = {A}')

    print('\nSending B value...')

    s.sendall(f'{B}'.encode())
    
    key = (A**b)%N

    print(f'\nKEY VALUE: {key}')

    s.close()
