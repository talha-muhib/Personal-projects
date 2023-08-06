"""
PRIM'S ALGORITHM
Green edges mean included in the tree
Red edges mean not included

KRUSKAL'S ALGORITHM
Purple edges mean included in the tree
Yellow edges mean not included

While the algorithm is running and 
you want to terminate, press any key
"""

#Importing necessary libraries
import pygame
import random
import math
from disjoint_set import UnionFind
from pq import PriorityQueue
pygame.init()

#Set up display window
WIDTH, HEIGHT = 900, 600 #Customize according to screen size
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MST Algorithms (Kruskal vs. Prim)")

#Colors we will use
RED = (195, 0, 0)
GREEN = (0, 195, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
PURPLE = (128, 0, 128)
YELLOW = (175, 175, 0)

#Fonts
FONT = pygame.font.SysFont('calibri', 20)
TITLE_FONT = pygame.font.SysFont('calibri', 40)

#Drawing our nodes
class Node:
    def __init__(self, x, y, color, n, label):
        self.x = x
        self.y = y
        self.color = color
        self.radius = round(150/n) #Shrinking the radius as # of nodes increase
        self.label = label #Node label

    #Setting color of our nodes
    def set_color(self, color):
        self.color = color

    #Drawing our labeled nodes
    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
        label = FONT.render(f"{self.label}", 1, WHITE)
        win.blit(label, (self.x - label.get_width()/2, self.y - label.get_height()/2))

#Drawing our edges
class Edge:
    def __init__(self, color):
        self.color = color

    #Setting color of our edges
    def set_color(self, color):
        self.color = color

    #Drawing our edges with costs
    def draw(self, win, p1, p2, cost):
        pygame.draw.lines(win, self.color, True, [(p1.x, p1.y), (p2.x, p2.y)], 1)
        cost_text = FONT.render(f"{cost}", 1, self.color)
        win.blit(cost_text, (abs(p1.x + p2.x)/2, abs(p1.y + p2.y)/2))

#Create a list of nodes
def make_nodes(n):
    node_list = []
    for i in range(n): #Arranging the nodes in a circle
        x = WIDTH/2 + 200 * math.cos(2 * math.pi * i/n)
        y = HEIGHT/2 + 200 * math.sin(2 * math.pi * i/n)
        node_list.append(Node(x, y, BLUE, n, i))
    
    #Return the list
    return node_list

#Create a list of edges
def make_edges(g):
    edge_dict = dict()
    for i in range(len(g)):
        for j in range(i + 1, len(g)):
            if g[i][j] != 0:
                edge_dict[(i, j)] = Edge(BLUE)
    
    #Return the list
    return edge_dict

#Processing an edge while an algorithm runs
def process_edge(edges, i, j, color):
    if (i, j) in edges:
        edges[(i, j)].set_color(color)
    else:
        edges[(j, i)].set_color(color)

#Generating a graph with edge costs
def generate_graph(n):
    g = []
    for _ in range(n): #Create an empty graph
        g.append([0] * n)

    #Update the edges with random costs
    for i in range(n):
        for j in range(i + 1, n):
            random_val = round(random.random() * 10)
            if math.floor(random_val / 3) != 0: #Adding this to make the graph more sparse
                g[i][j] = g[j][i] = random_val

    #Return our new graph
    return g

#Rendering the nodes and edges on the screen
def draw_graph(win, nodes, edges, g, text):
    win.fill(WHITE) #Add a white background
    #Drawing lines between every pair of nodes
    for e in edges:
        v1, v2 = nodes[e[0]], nodes[e[1]]
        edges[e].draw(win, v1, v2, g[e[0]][e[1]])

    #Render the nodes
    for node in nodes:
        node.draw(win)

    #Render the title
    title = TITLE_FONT.render(f"{text}", 1, BLUE)
    win.blit(title, (WIDTH/2 - title.get_width()/2, 5))

    #Render the options
    options = FONT.render(f"P - Prim | K - Kruskal | C - Clear | SPACE - Run", 1, BLUE)
    win.blit(options, (WIDTH/2 - options.get_width()/2, 45))

    #Update the display screen with the last rendering
    pygame.display.update()

#Prim's Algorithm 
def prim(draw, win, g, nodes, edges):
    pq = PriorityQueue()
    visited = set()

    #Keeping track of minimum cost
    min_cost = 0

    #Add a starting vertex into our priority queue
    pq.push((0, 0), g[0][0])
    nodes[0].set_color(GREEN)

    #Make an empty tree
    t = []
    for _ in range(len(g)):
        t.append([0] * len(g))

    #While the priority queue still has edges
    while not pq.isEmpty():
        #In case the user wants to close or reset the window while the algorithm runs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN: #Press any key to stop the algorithm from running
                print("Algorithm terminated")
                return g

        edge = pq.pop()
        if edge[1] not in visited:
            visited.add(edge[1]) #Mark all visited vertices
            t[edge[0]][edge[1]] = t[edge[1]][edge[0]] = g[edge[0]][edge[1]] #Add the vertex to our tree
            min_cost += g[edge[0]][edge[1]] #Update the min cost

            #Add all neighbors of our current vertex to the priority queue
            for i in range(len(g)):
                if g[edge[1]][i] != 0:
                    #Any vertex that we already visited should have the edge set to red
                    if i in visited:
                        process_edge(edges, edge[1], i, RED)
                        continue
                    pq.push((edge[1], i), g[edge[1]][i])
        
            #Set newly visited vertices and their edges to green
            nodes[edge[1]].set_color(GREEN)
            if not (edge[0] == 0 and edge[1] == 0):
                process_edge(edges, edge[1], edge[0], GREEN)
                print(f"Adding edge ({edge[0]}, {edge[1]})") #Print out the current edge

        #Yield and the display window update
        draw()
        yield True

    #Cost of our MST
    print(f"Cost of our MST is {min_cost}")

    #Return our MST
    return t

#Kruskal's Algorithm
def kruskal(draw, win, g, nodes, edges):
    uf = UnionFind(len(g))
    pq = PriorityQueue()

    #Keeping track of minimum cost
    min_cost = 0

    #Push every edge into the priority queue
    for i in range(len(g)):
        for j in range(i + 1, len(g)):
            if g[i][j] != 0:
                pq.push((i, j, g[i][j]), g[i][j])

    #While the priority queue still has edges
    while not pq.isEmpty():
        #In case the user wants to close or reset the window while the algorithm runs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN: #Press any key to stop the algorithm from running
                print("Algorithm terminated")
                return g

        edge = pq.pop()
        v1 = uf.simple_find(edge[0])
        v2 = uf.simple_find(edge[1])

        #If the endpoints of our edge do not share a set, then add the edge to our tree
        if v1 != v2:
            print(f"Adding edge ({edge[0]}, {edge[1]})") #Print out the current edge
            uf.union(v1, v2)
            g[edge[0]][edge[1]] = g[edge[1]][edge[0]] = edge[2]
            min_cost += edge[2] #Update the min cost

            #If an edge doesn't form a cycle, change the vertices and the edge to purple
            process_edge(edges, edge[0], edge[1], PURPLE)
            nodes[edge[1]].set_color(PURPLE)
            nodes[edge[0]].set_color(PURPLE)
        else:
            process_edge(edges, edge[1], edge[0], YELLOW) #Change to yellow otherwise
        
        #Yield and the display window update
        draw()
        yield True
    
    #Cost of our MST
    print(f"Cost of our MST is {min_cost}")

    #Return our MST
    return g

#Main function
def main():
    #Creating our graph
    n = round(random.random() * 9 + 1)
    n = n + ((n + 1) % 2)
    nodes = make_nodes(n)
    g = generate_graph(n)
    edges = make_edges(g)

    #Running the algorithms
    started = False

    #Generator
    algorithm_generator = None

    #Algorithm Name
    alg_name = "Prim's Algorithm"
    algorithm = prim

    #Variable for keeping the display window open
    run = True

    #pygame's built-in clock function
    clock = pygame.time.Clock()

    #Keep the window open as long as run is true
    while run:
        if started: #If the algorithm is already running
            try:
                clock.tick(1) #maximum 1 frame/second
                next(algorithm_generator) #Continue the algorithm
            except StopIteration: #Until the algorithm terminates
                started = False
                print(f"{alg_name} Terminated")
        else:
            #Update the display window every iteration
            draw_graph(WIN, nodes, edges, g, alg_name)

        #Every event that happens in the display
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #When the user hits the close button
                run = False #Break the loop
            
            #Key events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p and not started: #Selecting Prim's
                    algorithm = prim
                    alg_name = "Prim's Algorithm"
                    print(f"Selected {alg_name}")
                if event.key == pygame.K_k and not started: #Selecting Kruskal's
                    algorithm = kruskal
                    alg_name = "Kruskal's Algorithm"
                    print(f"Selected {alg_name}")
                if event.key == pygame.K_SPACE and started == False: #Starting the algorithm
                    started = True
                    algorithm_generator = algorithm(lambda: draw_graph(WIN, nodes, edges, g, alg_name), WIN, g, nodes, edges)
                    print(f"Running {alg_name}")
                if event.key == pygame.K_c and not started: #Reseting the display window
                    n = round(random.random() * 9 + 1)
                    n = n + ((n + 1) % 2)
                    g = generate_graph(n)
                    nodes = make_nodes(n)
                    edges = make_edges(g)
                    print(f"Graph Reset")
    
    pygame.quit() #Close the window

#Calling main
main()