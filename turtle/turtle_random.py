import turtle
import random

#lista di funzioni
directions = [turtle.left, turtle.right]

#cicla fino alla chiusura della finestra
while True:
    #vai avanti di 10 passi
    turtle.forward(10)
    #genera casualmente una direzione della lista directions e chiama funzione
    random.choice(directions)(90)

turtle.done()