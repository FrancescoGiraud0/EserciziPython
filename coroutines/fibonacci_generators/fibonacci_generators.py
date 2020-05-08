'''
Giraudo Francesco
Classe 5A ROB

Fibonacci function using generators and yield statement.
'''

def fib(limit):
    a, b = 0, 1

    while a < limit: 
        yield a 
        a, b = b, a + b 

f = fib(50)

fib_list = [next(f) for _ in range(10)]

print(fib_list)

f.close()