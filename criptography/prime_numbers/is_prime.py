import numpy as np
n = 9

def isPrime(n):
    for p in range(2, int(np.sqrt(n)) + 1):
        if (n % p == 0):
            return False

    return True

print("Numero primo" if isPrime(n) else "Numero non primo")