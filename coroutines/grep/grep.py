'''
Giraudo Francesco
Classe 5A ROB

Grep function using coroutines used to search all occurencies
of a word in a file.

To test it: python3 grep.py dolor sample.txt
'''

from sys import argv

def grep(substr):
    row_cnt = 0
    while True:
        line = yield
        if substr in line:
            print(f"Found {substr} at line {row_cnt}.")
        row_cnt += 1

if len(argv)>2:
    substr = argv[1]

    g = grep(substr)

    next(g)

    file_name = argv[2]
    f = open(file_name, 'r')

    lines = f.readlines()

    f.close()

    while len(lines):
        g.send(lines.pop())

    g.close()
else:
    print('Error: No arguments.')
