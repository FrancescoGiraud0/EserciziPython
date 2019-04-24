import networkx as nx
import matplotlib.pyplot as plt
import math

WEIGHT_EDGE = 1

#this function return a list of lists that define the floor of a room
def floorMatrixCreator(dim, objectCoord_list):
    #floor dim x dim list of lists of None
    floor_mat = [[None for col in range(0,dim)] for row in range(0,dim)]

    #for every obstacle's coordinate pair assign the corresponding tile
    #in the floor_mat
    for row,col in objectCoord_list:
        floor_mat[row][col] = "X"

    freeTileCounter = 0

    #assign a numeber to every free tile
    for row in range(0,dim):
        for col in range(0,dim):
            #check if the tile is free
            if floor_mat[row][col] != "X":
                floor_mat[row][col] = freeTileCounter
                freeTileCounter += 1
    
    return floor_mat

#from the floor matrix generate an adjacency dictionary
def adjDictCreator(floor_mat):
    adj_dict = {}

    #for every tile in floor_mat create a list of neighbors
    for row in range(0,len(floor_mat)):
        for col in range(0, len(floor_mat[row])):
            #check if the tile is not occupied by an obstacle
            if not floor_mat[row][col] == "X":
                #the tile number is now a key of the adjacency dictionary
                adj_dict[floor_mat[row][col]] = neighborsListCreator(floor_mat, row, col)

    return adj_dict

#function that return a list of neighbors of a specific tile in input
def neighborsListCreator(floor_mat, row, col):
    neighbors_list = []
    #save the dimension of the list of lists in dim variable
    dim = len(floor_mat)

    #up
    if row>0:
        if floor_mat[row-1][col]!="X":
            neighbors_list.append(floor_mat[row-1][col])

    #left
    if col>0:
        if floor_mat[row][col-1]!="X":
            neighbors_list.append(floor_mat[row][col-1])

    #right
    if col<dim-1:
        if floor_mat[row][col+1]!="X":
            neighbors_list.append(floor_mat[row][col+1])

    #down
    if row<dim-1:
        if floor_mat[row+1][col]!="X":
            neighbors_list.append(floor_mat[row+1][col])

    return neighbors_list

#function to convert an adjacency dictionary in a adjacency matrix (list of lists)
def convertToAdjMatrix(adj_dict):
    #list dimension calculation from the number of nodes
    dim = len(adj_dict)
    #inizializzo matrice di adiacenza dim x dim di zeri
    adj_mat = [[0 for col in range(0,dim)] for row in range(0,dim)]

    #for every item of the dict save the key and the value in row_list
    for key, neighbors_list in adj_dict.items():
        #for every node in neighbors_list
        for node in neighbors_list:
            #assign the edge weight value in the matrix
            adj_mat[key][node] = WEIGHT_EDGE

    return adj_mat

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

floor_dim = 4 #int(input("> Inserire dimensione pavimento: "))

obs_list = [(0,0),(0,1),(0,2),(0,3),(1,0),(1,3),(2,1),(3,3)]
floor_mat = floorMatrixCreator(floor_dim, obs_list)

print("\n")

adj_dict = adjDictCreator(floor_mat)
print("Adjacency dictionary: " + str(adj_dict))
adj_mat = convertToAdjMatrix(adj_dict)

#create a networkx.Graph() from a dict of lists
graph = nx.convert.from_dict_of_lists(adj_dict)

start_tile = int(input("\n> Start tile: "))
target_tile = int(input("\n> Target tile: "))

dist_list = dijkstra(start_tile, 0, adj_mat)

print("\n> Shortest paths from %d to others tile: " %start_tile, dist_list)
print("\n> Shortest path from %d to %d: %d" %(start_tile, target_tile, dist_list[target_tile]))

#create a position dictionary for graph draw
pos_dict = {}

for row,tile_list in enumerate(floor_mat):
    for col,tile in enumerate(tile_list):
        if tile != "X":
            pos_dict[tile] = (col, floor_dim-row)

_, path_list = nx.algorithms.shortest_paths.weighted.single_source_dijkstra(graph, start_tile, target_tile)

nx.draw(graph, pos=pos_dict, with_labels=True)
nx.draw(graph, pos=pos_dict, nodelist=path_list, node_color="yellow", with_labels=True)
nx.draw_networkx_nodes(graph, pos=pos_dict, nodelist=[start_tile], node_color="green", node_shape="D")
nx.draw_networkx_nodes(graph, pos=pos_dict, nodelist=[target_tile], node_color="red", node_shape="D")
plt.show()
