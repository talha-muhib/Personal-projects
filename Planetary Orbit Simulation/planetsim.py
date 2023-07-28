#Press the SPACE key to toggle between the inner and outer planets

import pygame
import math
pygame.init()

WIDTH, HEIGHT = 700, 700 #Customize according to your screen size
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) #Set the display window with the specified dimensions
pygame.display.set_caption("Planetary Orbit Simulation (Approximate)") #Title of our window

#Colors we will use
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 150, 255)
RED = (185, 40, 50)
GREY = (80, 80, 80)
WHITE = (200, 200, 140)
BLACK = (0, 0, 0)
TURQUOISE = (0, 255, 210)
DARK_BLUE = (0, 100, 200)
BROWN = (180, 150, 100)
LIGHT_BROWN = (215, 170, 100)

#Font
FONT = pygame.font.SysFont('calibri', 10)

G = 6.67428e-11 #Gravitational constant
AU = 149.6e6 * 1000 #Earth's distance to sun in meters
TIMESTEP = 3600 * 24 #1 day (timestep we'll be doing the simulation on)

#Planet class
class LargeBody:
    SCALE = 200 / AU #1 AU = 100 pixels

    def __init__(self, x, y, radius, color, mass, name):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.name = name

        #Planet's/Sun's velocity
        self.x_vel = 0
        self.y_vel = 0

        self.distance_to_sun = 0 #Distance to sun
        self.sun = False #SInce the planet isn't the sun, we need to draw an orbit for it

        self.orbit = [] #List of points the planet has traveled along

    #Drawing our large body
    def draw(self, win, scale_down):
        #Scale down the position of our planet and start at the center of the window
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        #We need at least 3 points to update our list of positions
        if len(self.orbit) > 2:
            #Make an updated list
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + WIDTH / 2
                updated_points.append((x, y))
                
            #Draw lines between our new points with a thickness of 1 without enclosing them
            pygame.draw.lines(win, self.color, False, updated_points, 1)

        #Draw our large body
        pygame.draw.circle(win, self.color, (x, y), self.radius/scale_down)

        #If the body isn't the sun then display a planet's distance to the sun
        if not self.sun:
            distance_text = FONT.render(f"{self.name}: {round(self.distance_to_sun/100)} km", 1, WHITE)
            win.blit(distance_text, (x - distance_text.get_width()/2, y + distance_text.get_height()))

    #Calculation the attraction between 2 bodies
    def attraction(self, other):
        #Calculating the distance from the other body
        distance_x = other.x - self.x
        distance_y = other.y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        #Save the distance to the sun if the other body is the sun
        if other.sun:
            self.distance_to_sun = distance

        #Law of universal gravitation
        force = G * self.mass * other.mass / distance ** 2

        #Calculate the angle by taking the arctan of the x and y distances
        theta = math.atan2(distance_y, distance_x)

        #Calculate the forces in the x and y directions
        force_x, force_y = math.cos(theta) * force, math.sin(theta) * force
        return force_x, force_y
    
    #Calculate the force of attraction between all the bodies and update the velocity
    def update_position(self, bodies):
        total_fx = total_fy = 0
        for body in bodies:
            if self == body:
                continue

            #Calculate the total force being exerted on the current body
            fx, fy = self.attraction(body)
            total_fx += fx
            total_fy += fy
        
        #Increasing x and y velocities from a = F/m
        self.x_vel += total_fx / self.mass * TIMESTEP
        self.y_vel += total_fy / self.mass * TIMESTEP

        #Update the current position of the body by the velocity
        self.x += self.x_vel * TIMESTEP
        self.y += self.y_vel * TIMESTEP
        self.orbit.append((self.x, self.y)) #Append the x and y position we're currently at

#Main function
def main():
    run = True
    clock = pygame.time.Clock()
    outer = False
    bodies = []
    scale_down = 1

    sun = LargeBody(0, 0, 40, YELLOW, 1.98892 * 10 ** 30, "") # <- mass in kg
    sun.sun = True

    #Terrestrial planets
    mercury = LargeBody(0.387 * AU, 0, 6, GREY, 3.3 * 10 ** 23, "Mercury")
    mercury.y_vel = -47.4 * 1000 #Each planet needs a starting force in the y direction (in km/s)

    venus = LargeBody(0.723 * AU, 0, 11, WHITE, 4.8685 * 10 ** 24, "Venus")
    venus.y_vel = -35.2 * 1000 

    earth = LargeBody(-1 * AU, 0, 12, BLUE, 5.9742 * 10 ** 24, "Earth")
    earth.y_vel = 29.783 * 1000 

    mars = LargeBody(-1.524 * AU, 0, 9, RED, 6.39 * 10 ** 23, "Mars")
    mars.y_vel = 24.077 * 1000 

    #Gas giants
    jupiter = LargeBody(5.2 * AU, 0,30, LIGHT_BROWN, 1.898 * 10 ** 27, "Jupiter")
    jupiter.y_vel = -13.07 * 1000 

    saturn = LargeBody(-9.538 * AU, 0, 25, BROWN, 5.863 * 10 ** 26, "Saturn")
    saturn.y_vel = 9.69 * 1000 

    uranus = LargeBody(19.8 * AU, 0, 20, TURQUOISE, 8.681 * 10 ** 25, "Uranus")
    uranus.y_vel = -6.81 * 1000 

    neptune = LargeBody(-30 * AU, 0, 18, DARK_BLUE, 1.024 * 10 ** 26, "Neptune")
    neptune.y_vel = 5.43 * 1000 

    #Default scale 
    default_scale = earth.SCALE
    smaller_scale = default_scale / 20

    """
    We need the loop to keep running so the display 
    window stays open unless the user closes the screen
    """
    while run:
        clock.tick(60) #maximum 60 frames/second
        WIN.fill(BLACK) #Make the background black

        for event in pygame.event.get():
            if event.type == pygame.QUIT: #When the user hits the close button
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    outer = not outer

        if outer:
            scale_down = 10
            bodies = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]
            for b in bodies:
                b.SCALE = smaller_scale
        else:
            scale_down = 1
            bodies = [sun, mercury, venus, earth, mars]
            for b in bodies:
                b.SCALE = default_scale
        
        #Drawing out our large bodies
        for b in bodies:
            b.update_position(bodies) #Update the position of the bodies
            b.draw(WIN, scale_down)
        pygame.display.update() #Update the display with the last events

    pygame.quit() #Close our window

#Call our main function
main()