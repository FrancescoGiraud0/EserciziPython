import turtle

#definizione numeri sequenza di fibonacci
f1, f2 = 1, 1
#numero di valori della sequenza da calcolare
num = 0

#controllo che numero sia maggiore di 0
while num<=0:
    #input numero di valori da generare
    num = int(input("> Quanti numeri vuoi generare della sequenza? "))

print(f1)
#ripeti per num volte
for i in range(0,num):
    #manda avanti per una distanza f2
    turtle.forward(f2)
    #ruota a sinistra di 90 gradi
    turtle.left(90)
    #stampa su terminale il valore di f2
    print(f2)

    #operazioni per il calcolo della sequenza
    temp = f1   #temp: variabile per temporanea per salvare valore f1
    f1 = f2
    f2 = temp + f1

#NON chiude la finestra alla fine  
turtle.done()