import turtle
import random

#lista di funzioni
directions = [turtle.left, turtle.right]
#numero di movimenti della turtle
nMovimenti = input(">Inserire numero di movimenti: ")

#cicla fino alla chiusura della finestra
for i in range(0,int(nMovimenti)):
    #vai avanti di 10 passi
    turtle.forward(10)
    #genera casualmente una direzione della lista directions e chiama funzione
    random.choice(directions)(90)

turtle.done()