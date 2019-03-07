#Giraudo Francesco
#Classe: 4^A ROB
#Data: 01/02/2019
#Programma che fa muovere una turtle per un numero determinato di movimenti
#(chiesto in input all'utente prima dell'esecuzione) facendo ruotare quest'ultima
#a destra o a sinistra casualmente utilizzando il modulo random
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