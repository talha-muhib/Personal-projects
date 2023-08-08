"""
PATH FINDING ALGORITHM VISUALIZER

In this project we explore 4 different algorithms and the 
visual differences in their traversals through a graph:
A*
Uniform Cost Search (UCS)
Breadth-First Search (BFS)
Depth-First Search (DFS)

Once you run this file on your local machine, 
a display window of squares should pop up.

You can click on the window to set squares anywhere you want.
You can right-click on a square to remove it.
Pressing the C key resets the whole grid.

The orange square is your starting point.
The turquoise square is your ending point.

The program won't run unless both start and end points are set.

To run an algorithm, press the SPACE key.
To choose which algorithm to run, read below:
A key selects A*
U key selects UCS
B key selects BFS
D key selects DFS

You will see in your terminal which algorithm 
was picked based on which key you pressed down on.

If you want to terminate the algorithm while it runs, press any key.
Then press C again to reset the grid.

Final note: I purposely designed A* to run slightly below par, 
so it will expand a couple more nodes than it ideally should.
Feel free to make it better!

I hope you find this helpful!
"""

import pygame
from util import Queue, Stack, PriorityQueue

#Set up display window
WIDTH = 600 #Customize according to screen size
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Path Finding Algorithms")

#Colors we will use for the squares and grid lines
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (65, 225, 210)

#Building our visualization tool in the form of little squares
class Spot:
    #Initialize our spot class
    def __init__(self, row, col, width, total_rows):
        self.total_rows = total_rows
        self.width = width
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []

    #Position of a spot
    def get_pos(self):
        return self.row, self.col
    
    #Check if spot was already visited
    def is_closed(self):
        return self.color == RED
    
    #Check if this spot is in the data structure
    def is_open(self):
        return self.color == GREEN
    
    #Check if this spot is a barrier
    def is_barrier(self):
        return self.color == BLACK
    
    #Check if spot is starting point
    def is_start(self):
        return self.color == ORANGE
    
    #Check if spot is an end point
    def is_end(self):
        return self.color == TURQUOISE
    
    #Spot was visited
    def make_closed(self):
        self.color = RED
    
    #Spot is now in the queue
    def make_open(self):
        self.color = GREEN
    
    #Make this spot a barrier
    def make_barrier(self):
        self.color = BLACK
    
    #Starting node color
    def make_start(self):
        self.color = ORANGE
    
    #End node color
    def make_end(self):
        self.color = TURQUOISE

    #This spot is on the path to the end node
    def make_path(self):
        self.color = PURPLE

    #Reset a square
    def reset(self):
        self.color = WHITE

    #Draw the square
    def draw(self, win): #(window)
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    #Check if neighboring squares aren't barriers
    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():    #DOWN
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():                      #UP
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():    #RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():                      #LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False

#Making the grid of squares (2D list)
def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
    
    return grid

#Drawing a grid of lines
def draw_grid(win, rows, width): #(window, rows, width)
    gap = width // rows
    for i in range(rows):
        #Drawing a line across (x1, y1) (x2, y2)
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

#Update the neighbors of every spot in the grid
def init_neighbors(grid):
    for row in grid:
        for spot in row:
            spot.update_neighbors(grid)

#Drawing everything in the display window
def draw(win, grid, rows, width):
    win.fill(WHITE) #Fill the entire display window with the color white

    #Draw each spot
    for row in grid:
        for spot in row:
            spot.draw(win)
    
    #Draw grid lines on top of that
    draw_grid(win, rows, width)
    pygame.display.update() #display window updates with whatever was drawn last

#Determining which square to fill in based on where our mouse was clicked
def get_clicked_pos(pos, rows, width):
    gap = width // rows #size of each square (aka gap between them)
    y, x = pos

    #deconstruct the position in terms of row and column
    row = y // gap
    col = x // gap

    return row, col

#Reconstructing a path
def reconstruct_path(paths, curr, draw, expanded_nodes):
    #Keep walking backwards until we run out of nodes for our path
    while curr in paths:
        curr = paths[curr]
        curr.make_path()
        draw()
    print("Number of nodes expanded:", expanded_nodes) #Print out how many nodes were expanded

#Heuristic for A* (Manhattan distance)
def h(p1, p2, incr):
    x1, y1 = p1
    x2, y2 = p2

    if incr == 1:
        return abs(x1 - x2) + abs(y1 - y2)
    return 0 #Return a null heuristic if necessary

#Bit of noise (You can change it aroundand see how it affects the algorithm's behavior)
#If you're curious, remove (cost + (h(p1, p2, 1) / 75)) and see if you notice something about UCS vs. BFS
#Playing with this can make the A* heuristic better or worse, and it can also make UCS better or worse
def noise_cost(cost, p1, p2):
    return cost * 1 #(cost + (h(p1, p2, 1) / 75))

#This function controls the implementation of all 4 algorithms
#(I'll leave it as an exercise for you to understand)
def algorithm(draw, grid, start, end, incr):
    node_paths = {} #Path of the spots from start to end
    visited = set()
    ds = None
    cost = 0
    expanded_nodes = 1

    #Initialize the data structure based on which algorithm we want to use
    if incr == 3:
        ds = Queue()
    elif incr == 4:
        ds = Stack()
    else:
        ds = PriorityQueue()
        cost = 1
    
    #Insert the start node into our data structure
    if incr == 1 or incr == 2:
        ds.push(start, 0)
    else:
        ds.push(start)
    costs = {spot: float("inf") for row in grid for spot in row} #Set cost of every node to infinity
    costs[start] = 0 #Set start node cost to 0
    fn = {spot: float("inf") for row in grid for spot in row} #Set F(n) of every node to infinity
    fn[start] = h(start.get_pos(), end.get_pos(), incr) #Set F(n) of start node to 0 + Heuristic(start)

    while not ds.isEmpty():
        #In case the user wants to close the window or clear the board while the algorithm runs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN: #Press any key to stop the algorithm from running
                print("Algorithm terminated")
                return False

        curr = ds.pop() #Remove the next element from the priority queue

        #If this node hasn't already been visited
        if curr not in visited:
            visited.add(curr)

            #If we are at the end node, then form a path back to the start node
            if curr == end:
                reconstruct_path(node_paths, end, draw, expanded_nodes) #Reconstruct the path taken to get to the end node
                end.make_end() #Keep the end node its original color
                start.make_start() #Keep the start node its original color
                return True
            
            #Check the successors
            for neighbor in curr.neighbors:
                temp_cost = costs[curr] + noise_cost(cost, neighbor.get_pos(), end.get_pos()) #Calculate the cost
                min_cost = min(temp_cost, costs[neighbor]) #See if it's the min cost
                fn[neighbor] = costs[neighbor] = min_cost #Update F(n) and Cost(n)
                fn[neighbor] += h(neighbor.get_pos(), end.get_pos(), incr) #Add the heuristic

                if isinstance(ds, PriorityQueue):
                    ds.push(neighbor, fn[neighbor])
                else:
                    ds.push(neighbor) 

                if neighbor not in visited:
                    neighbor.make_open() #Node is now in the data structure
                    node_paths[neighbor] = curr #Making a potential path
                    expanded_nodes += 1 #Keep track of how many nodes were expanded
        
        if curr != start:
            curr.make_closed() #If the node is already visited (and NOT the start node) then close it off

        draw()
    
    return False

#Main function
def main(win, width):
    ROWS = 50 #Number of rows in our display window (So number of squares is 50^2)
    grid = make_grid(ROWS, width) #Create our grid of squares

    start = None #In the beginning we have no start node
    end = None #We have no end node either
    run = True #We need this to continue letting the display window run
    incr = 1 #Default algorithm is A*
    current_algo = "Currently running A*"

    #While we haven't hit the close button yet
    while run:
        draw(win, grid, ROWS, width) #Update the grid display by drawing again

        #For each event that transpires on the display window
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #If the user clicks the x-button then close the window
                run = False

            #If the left mouse button was pressed
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]

                #If starting spot is not placed yet, choose a different place other than the end spot
                if not start and spot != end:
                    start = spot
                    start.make_start()
                #If ending spot is not placed yet, choose a different place other than the start spot
                elif not end and spot != start:
                    end = spot
                    end.make_end()
                #Otherwise make barriers
                elif spot != end and spot != start:
                    spot.make_barrier()
            
            #If the right mouse button was pressed on a square, remove that square
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None #Reset the start node if you right click was done on it
                if spot == end:
                    end = None #Reset the end node if you right click was done on it
            
            #If key is pushed down
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    incr = 1 #Press a to change to A* algorithm
                    current_algo = "Currently running A*"
                    print("Selected A*")
                if event.key == pygame.K_u:
                    incr = 2 #Press u to change to UCS algorithm
                    current_algo = "Currently running UCS"
                    print("Selected UCS")
                if event.key == pygame.K_b:
                    incr = 3 #Press b to change to BFS algorithm
                    current_algo = "Currently running BFS"
                    print("Selected BFS")
                if event.key == pygame.K_d:
                    incr = 4 #Press d to change to DFS algorithm
                    current_algo = "Currently running DFS"
                    print("Selected DFS")

                #Run the selected algorithm if the space key is pushed
                if event.key == pygame.K_SPACE and start and end:
                    init_neighbors(grid)
                    print(current_algo)
                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end, incr)
                
                #Clear the display window when hitting the c key
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
                    print("Cleared board")
        
    pygame.quit() #If the user hits the x-button, the window closes

main(WIN, WIDTH) #Running main