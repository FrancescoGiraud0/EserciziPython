#GIRAUDO FRANCESCO
#Classe: 4^A ROB
#Data: 15/03/2018
#Gara di turtle
import turtle as t
import random
import time

#Funzione che crea una turtle temporanea per disegnare il traguardo
def disegnaTraguardo():
    #Instanzia turtle
    turtleTraguardo = t.Turtle()
    #Alza la penna
    turtleTraguardo.penup()
    #Vai alla fine del traguardo
    turtleTraguardo.goto(traguardo, DIM_Y/2+20)
    #Abbassa la penna
    turtleTraguardo.pendown()
    #Vai alla fine del traguardo
    turtleTraguardo.goto(traguardo, -(DIM_Y/2+20))
    #Nascondi la turtle
    turtleTraguardo.hideturtle()

#Funzione che in base al valore del contatore passato come parametro posiziona la turtle
#dividendo equamente lo spazio in base al numero di turtle in gara
def posizionaTurtle(i_turtle):
    #Calcolo y posizione turtle (se indice maggiore della metà del numero di turtle calcola in negativo)
    #tutto moltiplicato per il rapporto tra la metà che le turtle andranno ad occupare di spazio equamente
    #divisa in parti uguali in base al numero di turtle/2.
    y = float(turtlesNumber//2 - i_turtle) * (DIM_Y/2) / (turtlesNumber/2)
    #Vai a punto calcolato (x = posizione partenza, y = posizione calcolata)
    turtlesList[i_turtle].goto(-((DIM_X/2)-10), y)

#Massimo numero di turtle
MAX_TURTLES = 20
#Costanti di dimensione finestra
DIM_X, DIM_Y = 600, 600
#Lista in cui memorizzare le turtle in gara
turtlesList = []
#varibile per memorizare il numero di turtle inizializzata a zero
turtlesNumber = 0
#Varibile in cui memorizzare l'indice della turtle vincitrice
vincitore = -1
#Variabile per memorizzare x del traguardo
traguardo = (DIM_X/2)-20

#Inserimento da parte dell'utente del numero di turtle partecipanti con controllo valore
while turtlesNumber<=0 or turtlesNumber>MAX_TURTLES:
    try:
        #Converto il valore in un intero
        turtlesNumber = int(input("\n> Inserire numero di turtle in gara(MAX %d): " % MAX_TURTLES))
    except ValueError:
        #Eccezione per valori inseriti diversi da un numero intero
        print("\n> ERRORE! Devi inserire un valore intero")

#Setta la dimensione della finestra
t.setup(DIM_X, DIM_Y+40)
#Aggiunge la possibilità di utilizzare valore RGB per cambiare i colori 
t.colormode(255)
#Chiamata funzione per disegnare il traguardo
disegnaTraguardo()

#Cicla per il numero di tartarughe in gara
for i in range(0,turtlesNumber):
    #Crea una nuova turtle e aggiungila alla lista
    turtlesList.append(t.Turtle())
    #Genera casualmente tre valori R G B utilizzando random.randrange() in modo da creare un colore casuale
    r = random.randrange(0, 255)
    g = random.randrange(0, 255)
    b = random.randrange(0, 255)
    #Colora la turtle con il colore RGB appena generato
    turtlesList[i].color((b,g,r))
    #Imposta velocità turtle a 0 (il massimo)
    turtlesList[i].speed(0)
    #Alza la penna in modo da non lasciare nessun segno durante lo spostamento per andare in posizione di partenza
    turtlesList[i].penup()
    #Chiama funzione per spostare la turtle in posizione di partenza
    posizionaTurtle(i)
    #Abbassa nuovamente la penna
    turtlesList[i].pendown()
    #Imposta la velocità a 2
    turtlesList[i].speed(2)

#Stampa conto alla rovescia gara
print("\n", end = "\r")
#Cicla per 3 volte assegnando al contatore un valore in ordine decrescente (3, 2, 1)
for timer in reversed(range(1,4)):
    #Stampa il valore del conto alla rovescia per poi ritornare ad inizio riga in modo
    #da cancellarla al prossimo ciclo
    print("> La gara comincia tra %d" %timer, end = "\r")
    #Attendi un secondo
    time.sleep(1)

print("> VIA!                                   ")

#Cicla fino a quando non c'è un vincitore
while vincitore<=-1:
    #Per ogni turtle in gara genera casulamente un numero tra 0 e 20 compresi per determinare
    #il numero di passi in avanti
    for i in range(0, turtlesNumber):
        step = random.randrange(0,21)
        turtlesList[i].forward(step)
        #Se la turtle i supera il traguardo viene salvato il valore i nella varibile vincitore,
        #viene eliminata la turtle dalla turtlesList per evitare che venga cancellata successivamente 
        #ed esce dal ciclo
        if turtlesList[i].xcor() > traguardo:
            vincitore = i
            turtlesList.pop(i)
            break

#Stampa su terminale la turtle vincitrice
print("\n> Ha vinto la turtle numero %d!" % (vincitore+1))
time.sleep(1)

#Ciclo in cui vengono cancellate tutte le turtle perdenti
for perdente in turtlesList:
    perdente.clear()
    perdente.hideturtle()

t.done()