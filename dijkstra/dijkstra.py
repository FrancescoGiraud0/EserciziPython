import math

def indexMinimo(lblList, notVisitedList):
    infiniteList = [math.inf]*len(lblList)
    for i in notVisitedList:
        infiniteList[i] = lblList[i]

    minimo = min(infiniteList)
    
    if not minimo==math.inf:
        return infiniteList.index(minimo)
    
    return -1

def dijkstra(currentNode, peso, graph, **other):
    if peso == 0:
        lblList = [math.inf]*len(graph)
        notVisitedList = [a for a in range(0,len(graph))]
    else:
        lblList = other.get("lblList")
        notVisitedList = other.get("notVisitedList")

    lblList[currentNode] = peso
    notVisitedList.remove(currentNode)

    if len(notVisitedList)==0:
        return lblList
    
    for node, weight in enumerate(graph[currentNode]):
        if weight!=0:
            if (node+peso)<lblList[node]:
                lblList[node] = weight+peso

    indexNextNode = indexMinimo(lblList, notVisitedList)

    if not indexNextNode==-1:
        return dijkstra(indexNextNode, lblList[indexNextNode], graph, lblList=lblList, notVisitedList=notVisitedList)
    
    return lblList

        # 0,1,2,3,4,5,6,7
grafo = [[0,1,4,0,0,0,0,0],
         [1,0,0,0,0,2,0,0],
         [4,0,0,5,0,0,0,0],
         [0,0,5,0,1,3,0,0],
         [0,0,0,1,0,0,2,3],
         [0,2,0,3,0,0,0,0],
         [0,0,0,0,2,0,0,4],
         [0,0,0,0,3,0,4,0]]

for i in range(0,len(grafo)):
    print( "Nodo " + str(i) + ": " + str(dijkstra(i,0,grafo)) )