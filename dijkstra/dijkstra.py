import math

def indexMinimo(distanceList, notVisitedList):
    distanceNotVisited = [math.inf]*len(distanceList)
    for i in notVisitedList:
        distanceNotVisited[i] = distanceList[i]

    minimo = min(distanceNotVisited)
    
    return distanceNotVisited.index(minimo)

def dijkstra(indexNodoMin, peso, matGrafo, **other):
    if peso == 0:
        distanceList = [math.inf]*len(matGrafo)
        notVisitedList = [a for a in range(0,len(matGrafo))]
    else:
        distanceList = other.get("distanceList")
        notVisitedList = other.get("notVisitedList")

    distanceList[indexNodoMin] = peso
    notVisitedList.remove(indexNodoMin)

    if len(notVisitedList)==0:
        return distanceList
        
    for i_nodo in notVisitedList:
        if matGrafo[indexNodoMin][i_nodo]!=0:
            if (matGrafo[indexNodoMin][i_nodo]+peso)<distanceList[i_nodo]:
                distanceList[i_nodo] = matGrafo[indexNodoMin][i_nodo]+peso

    indexNextNode = indexMinimo(distanceList, notVisitedList)

    #print(indexNextNode, distanceList[indexNextNode], distanceList, notVisitedList)

    return dijkstra(indexNextNode, distanceList[indexNextNode], matGrafo, distanceList=distanceList, notVisitedList=notVisitedList)
         #0,1,2,3,4,5,6,7
grafo = [[0,1,4,0,0,0,0,0],
         [1,0,0,0,0,2,0,0],
         [4,0,0,5,0,0,0,0],
         [0,0,5,0,1,3,0,0],
         [0,0,0,1,0,0,2,3],
         [0,2,0,3,0,0,0,0],
         [0,0,0,0,2,0,0,4],
         [0,0,0,0,3,0,4,0]]

for i in range(0,len(grafo)):
    print(i,dijkstra(i,0,grafo))