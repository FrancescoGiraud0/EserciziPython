grafo = [[0,0,1,1,0],[0,0,1,1,1],[1,1,0,1,1],[1,1,1,0,1],[0,1,1,1,0]]

for indexNodo in range(0,len(grafo)):
    for indexCollegamento in range(0,len(grafo[indexNodo])):
        if indexCollegamento == 0:
            print("\nNodo %d:" % indexNodo, end = '')
        if grafo[indexNodo][indexCollegamento] == 1:
            print(" %d" % indexCollegamento, end = '')