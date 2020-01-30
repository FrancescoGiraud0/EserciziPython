"""
Francesco Giraudo
Classe 5^A ROB
Algorithm that calculate Diffie-Hellman private key.
"""

import sys

N = 9973
g = 1567

try:
    sniffed_value = int(sys.argv[1])
except TypeError:
    print('Type Error')

print(f'Sniffed value = {sniffed_value}')

for y in range(0,N):
    if (g**y)%N == sniffed_value:
        private_value = y
        break

print(f'Computed value: {private_value}')
