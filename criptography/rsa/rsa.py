""" Giraudo Francesco
    Classe 5^A ROB
    Github @FrancescoGiraud0
    RSA algorithm implementation. """

import numpy as np
import sys

# Increasing the recursion limit because it's 
# necessary for the implemention of 
# Extended Euclide Algorithm -> extended_mcd()
sys.setrecursionlimit(1000000)

def mcd(a, b):
    """ Function that return the gratest common divisor
        between two numbers a and b. It is based on the 
        Euclide algorithm."""
    
    if b > a:       # If b is greater than a switch their values
        a,b = b,a
    
    while b:            # While b is not 0 (so while it's not finished)
        a,b = b, a%b    # Compute the next b value and save the past value in a

    return a    # Return the last value before 0

def mcm(a,b):
    """ Function tha return the least common multiple
        between two numbers a and b."""
    return (a*b) // mcd(a,b)

def is_prime(n):
    """ Function that check if a number is prime.
        It return True if n is prime, False if not."""

    if n%2 == 0 and n>2:                        # Check if n is even and greater it's not 2  
        return False

    for p in range(3, int(np.sqrt(n)) + 1):     # For every odd value p in range 3 to sqrt(n)+1
        if (n % p == 0):                        # check if n is divisible by p
            return False                        # if it's divisble it isn't prime so it returns False

    return True                                 # If it pass the for loop or it's 2, return True

def extended_euclide_algorithm(c, m):
    """
    This recursive function return a tuple (g, x, y)
    such that c*x + m*y = g = gcd(c, m).
    """
    if c == 0:
        return (m, 0, 1)
    else:
        g, x, y = extended_euclide_algorithm(m % c, c)
        return (g, y - (m // c) * x, x)

def rsa_create_keys(p,q):
    """
    This function get two prime numbers (p,q) and returns a tuple (n,c,m,d).
    """
    if (not is_prime(p)) or (not is_prime(q)):                     # If almost one number is not prime
        raise ValueError('Both numbers must be prime.')        # raise ValueError exception.
    elif p==q:                                                 # If p and q are equals 
        raise ValueError('Numbers (p and q) cannot be equal.') # raise ValueError exception.
    
    n = p * q

    m = mcm(p-1,q-1)

    # Searching the greatest prime value c
    # in range 1<c<m that mcd(c,m)=1
    for c in range(int(np.sqrt(m))+1,1,-1):         # For value c in range from sqrt(m)+1 to 1
        if mcd(c,m) == 1 and is_prime(c):           # If the mcd between c and m is 1 and c is prime
            break                                   # save c value and exit from the loop

    _,d,_ = extended_euclide_algorithm(c,m)         # Computing d value using extended_euclide_algorithm

    d = d%n                                         # d value could be negative

    return (n,c,m,d)

def rsa_encode(encoded_string,c,n):
    """
    This function get a ascii byte string and c,n public keys in order
    to return a list of numbers encoded in RSA.
    """
    return list(map(lambda x: (x**c)%n, encoded_string))

def rsa_decode(byte_list,d,n):
    """
    This function get a list of numbers encoded in RSA, apply 
    the operations to decode every single number, convert every
    number in an ASCII character and then return the decoded string.
    """
    decoded_char_list = list(map(lambda x: chr((x**d) % n), byte_list))
    return ''.join(decoded_char_list)


if __name__ == "__main__":
    try:
        n,c,m,d = rsa_create_keys(37,47) # Compute public and private keys from p and q
        print(f'Public keys: n -> {n} | c -> {c}\nPrivate keys: m -> {m} | d -> {d}')

        msg = input('\nInsert your string (only ASCII characters).\n> ') # Message input

        # Encoding in ASCII the string replecing with '?' not supported characters 
        msg = msg.encode('ascii', errors='replace')
        
        encrypted_byte_list= rsa_encode(msg,c,n)
        print(f'Byte list encrypted: {encrypted_byte_list}')

        decrypted_msg = rsa_decode(encrypted_byte_list,d,n)
        print(f'Decrypted message: {decrypted_msg}')

    except ValueError as error_info:
        print(f'Unexpected error: {error_info}')
