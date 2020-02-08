"""
Francesco Giraudo
Classe 5^A ROB
Algorithm that compute Diffie-Hellman possible private keys.
"""

import sys
import argparse # Python module to manage command line arguments

def compute_values(N, g, sniffed_value):
    """
    Function that do a brute force computation of the discrete logarithm
    (log_g(A) mod N = y), print and return all possible values.
    """
    print(f'Sniffed value: {sniffed_value}')
    print('Computed values:')

    results_list = [] # List where possible values will be saved in

    for y in range(0,N):    # For every number in the range from 0 to N
        if (g**y)%N == sniffed_value:   # If y it's a possbile value
            print(y)                    # Print the value
            results_list.append(y)      # Append it to the results_list

    return results_list

def compute_keys(N, B, results_list):
    """
    Function that compute all possible cryptographic keys on the base of sniffed
    values and possbible results returned by compute_values().
    """
    possible_keys = []  # List where possible keys will be saved in
    for r in results_list:      # For every elements in rasults_list
        k = (B**r)%N            # It calculates the key value
        possible_keys.append(k) # And append it to possible_keys list

    return possible_keys


def main():
    parser = argparse.ArgumentParser()
    # N public value (default value is only for debug)
    parser.add_argument('--N', type=int, default=9973,
                        help='What is the N public value?')
    # g public value (default value is only for debug)
    parser.add_argument('--g', type=int, default=1567,
                        help='What is the g public value?')
    # A is the first sniffed value
    parser.add_argument('--A', type=int, default=0,
                        help='What is the first number sniffed?')
    # B is the second sniffed value
    parser.add_argument('--B', type=int, default=0,
                        help='What is the second number sniffed?')

    args = parser.parse_args()

    sniffed_values = []

    if args.A != 0:
        sniffed_values.append(args.A)

    if args.B != 0:
        sniffed_values.append(args.B)
    
    # Check if the user inserted almost one sniffed value different from 0
    if len(sniffed_values) < 1:
        print('\nError: please define almost a sniffed value (--A or --B).')

    N = args.N
    g = args.g
    
    # Computes possible values (possible results of the discrete logarithm)
    results_list = compute_values(N,g,sniffed_values[0])

    if len(sniffed_values)>0:
        possible_keys = compute_keys(N, sniffed_values[1], results_list)
        print(f'Possible keys: {possible_keys}')

if __name__=='__main__':
    main()