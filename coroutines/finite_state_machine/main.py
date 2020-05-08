'''
Francesco Giraudo
Classe 5A ROB

Test of FSM class.
'''

from fsm import FSM

str_list = ['abc', 'ab', 'babc',
            'abbc', 'ac', 'abb',
            'abbbbbbc', 'aaaabc']

for s in str_list:
    evalutator = FSM()

    for c in s:
        evalutator.send(c)

    print('{} is {}'.format(s, 'OK' if evalutator.does_match() else 'NOT OK'))