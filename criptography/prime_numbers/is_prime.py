import numpy as np

def isPrime(n):
    for p in range(2, int(np.sqrt(n)) + 1, 2):
        if (n % p == 0):
            return False

    return True

if __name__ == "__main__":
    n = 9
    print("Numero primo" if isPrime(n) else "Numero non primo")