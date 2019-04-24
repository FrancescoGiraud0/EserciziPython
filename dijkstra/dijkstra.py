import math

def indexMin(label_list, notVisited_list):
    infinite_list = [math.inf]*len(label_list)
    for i in notVisited_list:
        infinite_list[i] = label_list[i]

    minimum = min(infinite_list)
    
    if not minimum==math.inf:
        return infinite_list.index(minimum)
    
    return -1

def dijkstra(currentNode, previous_weight, graph, **other):
    if previous_weight == 0:
        label_list = [math.inf]*len(graph)
        notVisited_list = [a for a in range(0,len(graph))]
    else:
        label_list = other.get("label_list")
        notVisited_list = other.get("notVisited_list")

    label_list[currentNode] = previous_weight
    notVisited_list.remove(currentNode)

    if len(notVisited_list)==0:
        return label_list
    
    for node, weight in enumerate(graph[currentNode]):
        if weight!=0:
            if (node+weight)<label_list[node]:
                label_list[node] = previous_weight + weight

    indexNextNode = indexMin(label_list, notVisited_list)

    if not indexNextNode==-1:
        return dijkstra(indexNextNode, label_list[indexNextNode], graph, label_list=label_list, notVisited_list=notVisited_list)
    
    return label_list