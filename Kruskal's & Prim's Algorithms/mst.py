import pygame
import random
from disjoint_set import UnionFind
from pq import PriorityQueue
pygame.init()

#Drawing our graph
class Graph:
    pass

#Prim's Algorithm 
def prim(g):
    pq = PriorityQueue()
    visited = set()

    #Add a starting vertex into our priority queue
    pq.push((0, 0), g[0][0])

    #Make an empty tree
    t = []
    for _ in range(len(g)):
        t.append([0] * len(g))

    #While the priority queue still has edges
    while not pq.isEmpty():
        edge = pq.pop()
        if edge[1] not in visited:
            visited.add(edge[1]) #Mark all visited vertices
            t[edge[0]][edge[1]] = t[edge[1]][edge[0]] = g[edge[0]][edge[1]] #Add the vertex to our tree

            #Add all neighbors of our current vertex to the priority queue
            for i in range(len(g[edge[1]])):
                if g[edge[1]][i] != 0:
                    pq.push((edge[1], i), g[edge[1]][i])

    #Return our MST
    return t

#Kruskal's Algorithm
def kruskal(g):
    uf = UnionFind(len(g))
    pq = PriorityQueue()

    #Push every edge into the priority queue
    for i in range(len(g)):
        for j in range(len(g)):
            if g[i][j] != 0:
                pq.push((i, j, g[i][j]), g[i][j])
                g[j][i] = g[i][j] = 0

    #While the priority queue still has edges
    while not pq.isEmpty():
        edge = pq.pop()
        v1 = uf.simple_find(edge[0])
        v2 = uf.simple_find(edge[1])

        #If the endpoints of our edge do not share a set, then add the edge to our tree
        if v1 != v2:
            uf.union(v1, v2)
            g[edge[0]][edge[1]] = g[edge[1]][edge[0]] = edge[2]
    
    #Return our MST
    return g

#Main function
def main():
    n = round(random.random() * 20)
    g = [
        [0, 1, 2],
        [1, 0, 3],
        [2, 3, 0]
    ]

    print("G =", g)
    print("After running Kruskal's Algorithm, T =", kruskal(g))
    print("After running Prim's Algorithm, T =", prim(g))

#Calling main
main()