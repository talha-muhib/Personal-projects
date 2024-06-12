import pygame
import neat
import time
import os
import random

pygame.font.init()

WIDTH, HEIGHT = 500, 600

BG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))
BIRD1 = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png")))
BIRD2 = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png")))
BIRD3 = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))
PIPE = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BIRD_IMGS = [BIRD1, BIRD2, BIRD3]

STAT_FONT = pygame.font.SysFont("comicsans", 30)

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird AI")


class Flappy:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]
    
    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1
        d = self.vel * self.tick_count + 1.5 * self.tick_count**2

        if d >= 16:
            d = 16
        if d < 0:
            d -= 2
        
        self.y += d
        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL
    
    def draw(self, win):
        self.img_count += 1
        img_arc = -2

        for i in range(1, 6):
            if self.img_count < self.ANIMATION_TIME * i:
                self.img = self.IMGS[2 - abs(img_arc)]
                if i == 5: self.img_count = 0
                break
            img_arc += 1
        
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2
        
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)
    
class Pipe:
    GAP = 200
    VEL = 5

    def __init__(self, x) -> None:
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE, False, True)
        self.PIPE_BOTTOM = PIPE
        self.passed = False
        self.set_height()
    
    def set_height(self):
        self.height = random.randrange(50, 350)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP
    
    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        t_point = bird_mask.overlap(top_mask, top_offset)
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)

        if t_point or b_point:
            return True
        
        return False
    
class Base:
    VEL = 5
    WIDTH = BASE.get_width()
    IMG = BASE
    
    def __init__(self, y) -> None:
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH
    
    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


def draw_window(win, birds, pipes, base, score):
    win.blit(BG, (0, -250))

    for pipe in pipes:
        pipe.draw(win)
    base.draw(win)

    for bird in birds:
        bird.draw(win)

    text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(text, (WIDTH - 10 - text.get_width(), 10))

    pygame.display.update()

def main(genomes, config):
    flappies = []
    nets = []
    ge = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        flappies.append(Flappy(150, 300))
        g.fitness = 0
        ge.append(g)

    base = Base(530)
    pipes = [Pipe(550)]
    run = True
    score = 0
    clock = pygame.time.Clock()

    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
        
        pipe_ind = 0
        if len(flappies) > 0:
            if len(pipes) > 0 and flappies[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1
        else:
            run = False
            break

        for x, flappy in enumerate(flappies):
            flappy.move()
            ge[x].fitness += 0.1

            output = nets[x].activate((flappy.y,
                                       abs(flappy.y - pipes[pipe_ind].height),
                                       abs(flappy.y - pipes[pipe_ind].bottom)))
            
            if output[0] > 0.5:
                flappy.jump()

        rem = []
        add_pipe = False
        for pipe in pipes:
            for x, flappy in enumerate(flappies):
                if pipe.collide(flappy):
                    ge[x].fitness -= 1
                    flappies.pop(x)
                    nets.pop(x)
                    ge.pop(x)
                
                if not pipe.passed and pipe.x < flappy.x:
                    pipe.passed = True
                    add_pipe = True
            
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            pipe.move()

        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(550))

        for r in rem:
            pipes.remove(r)

        for x, flappy in enumerate(flappies):
            if flappy.y + flappy.img.get_height() > 530 or flappy.y < 0:
                flappies.pop(x)
                nets.pop(x)
                ge.pop(x)

        base.move()

        draw_window(win, flappies, pipes, base, score)


def run(config_path):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    p.add_reporter(neat.StatisticsReporter())
    winner = p.run(main, 50)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)