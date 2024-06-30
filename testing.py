import pygame
from pygame.locals import *
pygame.init()

from src.engine.utils import Debug

SPEED_FACTOR = 60
SCREENSIZE = (960, 540)
FPS = 0
GRAVITY_CONST = 40


class BlackHole:
    position = pygame.Vector2(150, 270 + 10)
    mass = 40

    color = pygame.Color('white')
    radius = 20


class Player:
    position = pygame.Vector2(150, 230)
    mass = 1
    velocity = pygame.Vector2(6, 0)
    acceleration = pygame.Vector2(0, 0)

    color = pygame.Color('red')
    radius = 10


class App():
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(SCREENSIZE)


    def loop(self):
        while True:
            self.handle_events()            
            delta = self.get_delta()

            self.screen.fill('black')    
            
            Player.velocity += Player.acceleration * delta * SPEED_FACTOR
            Player.position += Player.velocity * delta * SPEED_FACTOR
            
            Player.acceleration *= 0

            diff = BlackHole.position - Player.position
            norm_vec = diff.normalize()
            distance = diff.magnitude()
            gravity_force = (GRAVITY_CONST * Player.mass * BlackHole.mass) / distance ** 2
            
            Player.acceleration += norm_vec * gravity_force
            

            pygame.draw.circle(self.screen, Player.color, Player.position, Player.radius)
            pygame.draw.circle(self.screen, BlackHole.color, BlackHole.position, BlackHole.radius)
            
            pygame.display.update()
            self.clock.tick(FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                raise SystemExit
            
            if event.type == MOUSEWHEEL:
                SPEED_FACTOR += event.y
                
            Debug.handle_event(event)

    def get_delta(self):
        delta = self.clock.get_time() / 1000

        if delta > 0.1:
            delta = 0.1

        return delta


if __name__ == '__main__':
    App().loop()
