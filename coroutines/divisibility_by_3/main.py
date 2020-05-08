'''
Francesco Giraudo
Classe 5A ROB

Test of FSM to check divisibility by 3 of a number.
'''

from div_3 import DivisibleByThree_FSM

def is_divisible(n):
    digits = []

    evalutator = DivisibleByThree_FSM()

    # Creation of the list of digits
    x = n
    while x>0:
        digits.append(x%10)
        x //= 10

    for d in digits:
        evalutator.send(d)
    
    return evalutator.divisible()
    
test_values = [0, 1, 3, 6, 9, 39, 
               54, 53, 32, 214,
               1024, 256, 64, 10,
               3333, 346, 22, 612]

for t in test_values:
    print('{} {} divisible by 3\n'.format(t, 'IS' if is_divisible(t) else 'IS NOT'))
