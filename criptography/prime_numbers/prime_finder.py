import numpy as np

def isPrime(n):
    for p in range(2, int(np.sqrt(n)) + 1):
        if (n % p == 0):
            return False

    return True


def nthPrime(n):
    n = int(abs(n))

    if n > 0:
        prime_counter, prime_number = 1, 2
        next_number = 1

        while prime_counter < n:

            next_number += 2

            if isPrime(next_number):
                prime_counter += 1
                prime_number = next_number

        return prime_number

    return None

if __name__ == "__main__":
    n = 11
    print(nthPrime(n))
