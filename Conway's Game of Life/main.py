#Import the necessary libraries
import pygame
import random

#Initialize Pygame
pygame.init()

#Just some colors we need for the screen (in RGB format)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
YELLOW = (255, 255, 0)

#Dimensions of the screen
WIDTH, HEIGHT = 600, 600

#Calculating the size of individual tiles and the total # of tiles
TILE_SIZE = 20
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE

#Frames per second when simulation starts
FPS = 60

#Setting up our screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

#This clock will be used for our FPS
clock = pygame.time.Clock()

#Generate a set of random positions for our live tiles
def gen(num):
    return set([(random.randrange(0, GRID_WIDTH), random.randrange(0, GRID_HEIGHT)) for _ in range(num)])

#Drawing the grid of tiles
def draw_grid(positions):
    #Looping through all the live positions and drawing tiles at those positions
    for position in positions:
        col, row = position
        top_left = (col * TILE_SIZE, row * TILE_SIZE)
        pygame.draw.rect(screen, YELLOW, (*top_left, TILE_SIZE, TILE_SIZE))

    #Drawing the horizontal grid lines
    for row in range(GRID_HEIGHT):
        pygame.draw.line(screen, BLACK, (0, row * TILE_SIZE), (WIDTH, row * TILE_SIZE))

    #Drawing the vertical grid lines
    for col in range(GRID_WIDTH):
        pygame.draw.line(screen, BLACK, (col * TILE_SIZE, 0), (col * TILE_SIZE, HEIGHT))

#Adjusting the grid for when a certain # of cells are gathered in one region
def adjust_grid(positions):
    #Set for containing all neighbors of our live cells
    all_neighbors = set()

    #Set for containing new cell positions once grid is adjusted
    new_positions = set()

    #Go through our current positions
    for position in positions:
        #Get all neighbors (dead or alive) surrounding a cell
        neighbors = get_neighbors(position)
        
        #Add our new neighbors to all_neighbors
        all_neighbors.update(neighbors)

        #Filter out all dead neighbors because we only want the live cells
        neighbors = list(filter(lambda x: x in positions, neighbors))

        #Check if we have enough live neighbors to keep the current live cell
        if len(neighbors) in [2, 3]:
            new_positions.add(position)
    
    #Go through all the neighbors we ollected
    for position in all_neighbors:
        #Retrieve the neighbors of the current position
        neighbors = get_neighbors(position)

        #Filter out neighbors that are still alive
        neighbors = list(filter(lambda x: x in positions, neighbors))

        #If we have 3 live neighbors then create another live cell
        if len(neighbors) == 3:
            new_positions.add(position)
    
    #Return the new set of live tile positions
    return new_positions

#Get all neighbors of a current position
def get_neighbors(pos):
    #Deconstruct the position into its (x, y) components
    x, y = pos

    #Create an empty list for our neighbors
    neighbors = []

    #Look at x-coordinates one behind and one forward
    for dx in [-1, 0, 1]:
        #Skip if position is off the screen
        if x + dx < 0 or x + dx > GRID_WIDTH:
                continue
        
        #Look at y-coordinates one above and one below
        for dy in [-1, 0, 1]:
            #Skip if position is off the screen
            if y + dy < 0 or y + dy > GRID_HEIGHT:
                continue

            #Skip if (dx, dy) = (x, y)
            if dx == 0 and dy == 0:
                continue

            #Otherwise add the neighbor
            neighbors.append((x + dx, y + dy))
    
    #Return list of neighbors
    return neighbors

#Main function
def main():
    #Variable to keep the screen open
    running = True

    #Check if simulation started
    playing = False

    #Empty set of positions
    positions = set()

    #Frequency of adjusting the board
    count = 0
    update_frequency = 60

    #Program keeps running indefinitely
    while running:
        clock.tick(FPS) #Program will only run at 60 FPS

        #If simulation is running, then update the count
        if playing:
            count += 1
        
        #If the count passes the threshold then update the grid positions
        if count > update_frequency:
            count = 0
            positions = adjust_grid(positions)

        #Title of the screen
        pygame.display.set_caption("Conway's Game of Life - Playing" if playing else "Conway's Game of Life - Paused")

        #For every event that happens while the program runs
        for event in pygame.event.get():
            #If the user hits the 'X' button then stop the program
            if event.type == pygame.QUIT:
                running = False
            
            #If the user presses down on the screen
            if event.type == pygame.MOUSEBUTTONDOWN:
                #Deconstruct the cursor's position on screen into its (x, y) components
                x, y = pygame.mouse.get_pos()

                #Calculate which row and column a tile will be placed in based on (x, y)
                col = x // TILE_SIZE
                row = y // TILE_SIZE

                #Tuple of (column, row)
                pos = (col, row)

                #If the position is already live, you can remove it
                if pos in positions:
                    positions.remove(pos)
                #Otherwise mmake it live
                else:
                    positions.add(pos)
            
            #If the user presses a key on the keyboard
            if event.type == pygame.KEYDOWN:
                #Hit the space key to pause/play the simulation
                if event.key == pygame.K_SPACE:
                    playing = not playing
                
                #Hit the C key to clear the board and reset
                if event.key == pygame.K_c:
                    positions = set()
                    playing = False
                    count = 0
                
                #Hit the G key to randomly generate a set of live cells
                if event.key == pygame.K_g:
                    positions = gen(random.randrange(2, 5) * GRID_WIDTH)

        #Color the screen grey
        screen.fill(GREY)

        #Draw our grid with our live cells
        draw_grid(positions)

        #Update the screen display every iteration
        pygame.display.update()
    
    #Close the program
    pygame.quit()

#Call the main function if this file is run directly
if __name__ == "__main__":
    main()