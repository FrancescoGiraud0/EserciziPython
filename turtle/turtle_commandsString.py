#Giraudo Francesco
#Classe: 4^A ROB
#Data: 07/02/2019
#Programma che fa muovere una turtle data una sequenza di comandi
#costituita da una stringa (commandsString)
import turtle

#Imposta velocità turtle
turtle.speed(1)

#Dizionario in cui sono definite le funzioni di movimento della turtle
#N.B. se si usano le parentesi all'interno del dizionario le funzioni verranno chiamate
commandsDictionary = {"f":turtle.forward, "b": turtle.backward, "r":turtle.right, "l":turtle.left}

#Stringa che raccoglie i comandi che dovrà effettuare la turtle
#In questo caso la turtle disegnerà la lettera "F"
#'G' 'h' '!' '6' sono inseriti per provare la gestione degli errori
commandsString = "FFBbfFFrfRfflfLfrfrflffrfrfffffGh!6"

#Trasformo la stringa in caratteri minuscoli
commandsString = commandsString.lower()

#Ciclo per ogni lettera della stringa
for letter in commandsString:
    #Utilizzo una if per differenziare le funzioni di forward e backward da right e left
    #perchè utilizzano attributi diversi
    if letter == "f" or letter == "b":
        #Chiamata funzioni di movimento avanti o indietro di 50 unità
        commandsDictionary[letter](50)
    else:
        #Verifica che la chiave inserita esista nel dizionario
        try:
            #Chiamata di funzioni di rotazione
            #Rotazione a sinistra o a destra di 90 gradi
            commandsDictionary[letter](90)
        #Gestione dell'eccezione(carattere key non definito nel dizionario)
        except KeyError:
            #Stampa errore
            print("> '%s' non è un comando definito" %letter)

turtle.done()