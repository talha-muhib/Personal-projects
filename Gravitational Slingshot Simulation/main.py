import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravitational Slingshot Simulation")

G = 5
PLANET_MASS = 100
SHIP_MASS = 5
FPS = 60
PLANET_RADIUS = 50
OBJECT_SIZE = 5
VELOCITY_SCALE = 100

BG = pygame.transform.scale(pygame.image.load("background.jpg"), (WIDTH, HEIGHT + 50))
JUPITER = pygame.transform.scale(pygame.image.load("jupiter.png"), (PLANET_RADIUS * 2, PLANET_RADIUS * 2))

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class Planet:
    def __init__(self, x, y, mass) -> None:
        self.x = x
        self.y = y
        self.mass = mass
    
    def draw(self):
        win.blit(JUPITER, (self.x - PLANET_RADIUS, self.y - PLANET_RADIUS))

class Spacecraft:
    def __init__(self, x, y, vel_x, vel_y, mass) -> None:
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.mass = mass
    
    def draw(self):
        pygame.draw.circle(win, RED, (int(self.x), int(self.y)), OBJECT_SIZE)

    def move(self, planet=None):
        distance = math.sqrt((self.x - planet.x)**2 + (self.y - planet.y)**2)
        force = (G * self.mass * planet.mass) / distance**2
        acceleration = force / self.mass
        angle = math.atan2(planet.y - self.y, planet.x - self.x)
        acceleration_x = acceleration * math.cos(angle)
        acceleration_y = acceleration * math.sin(angle)

        self.vel_x += acceleration_x
        self.vel_y += acceleration_y
        self.x += self.vel_x
        self.y += self.vel_y

def create_ship(location, mouse):
    tx, ty = location
    mx, my = mouse
    vel_x = (mx - tx) / VELOCITY_SCALE
    vel_y = (my - ty) / VELOCITY_SCALE
    obj = Spacecraft(tx, ty, vel_x, vel_y, SHIP_MASS)
    return obj

def main():
    running = True
    clock = pygame.time.Clock()
    objects = []
    temp_obj_pos = None
    planet = Planet(WIDTH // 2, HEIGHT // 2, PLANET_MASS)

    while running:
        clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if temp_obj_pos:
                    obj = create_ship(temp_obj_pos, mouse_pos)
                    objects.append(obj)
                    temp_obj_pos = None
                else:
                    temp_obj_pos = mouse_pos
        
        win.blit(BG, (0, 0))
        if temp_obj_pos:
            pygame.draw.line(win, WHITE, temp_obj_pos, mouse_pos, 2)
            pygame.draw.circle(win, RED, temp_obj_pos, OBJECT_SIZE)

        for obj in objects[:]:
            obj.draw()
            obj.move(planet)
            off_screen = obj.x < 0 or obj.y > WIDTH or obj.y < 0 or obj.y > HEIGHT
            collided = math.sqrt((obj.x - planet.x)**2 + (obj.y - planet.y)**2) <= PLANET_RADIUS

            if off_screen or collided:
                objects.remove(obj)

        planet.draw()
        pygame.display.update()
    
    pygame.quit()

if __name__ == "__main__":
    main()