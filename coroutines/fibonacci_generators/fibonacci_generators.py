def fib(limit):
    a, b = 0, 1

    while a < limit: 
        yield a 
        a, b = b, a + b 

x = fib(30)

print(x.__next__())
print(x.__next__())
print(x.__next__())

for i in x:
    print(i)