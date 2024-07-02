import pygame
from pygame.locals import *
pygame.init()

from src.engine.utils import Debug

SPEED_FACTOR = 60
SCREENSIZE = (960, 540)
FPS = 0
GRAVITY_CONST = 40


class Player:
    position = pygame.Vector2(525, 230) #pygame.Vector2(150, 230)
    mass = 1
    velocity = pygame.Vector2(0, 3)
    acceleration = pygame.Vector2(0, 0)

    color = pygame.Color('red')
    radius = 20

    rect = pygame.Rect(0, 0, radius * 2, radius * 2)
    rect.center = position


class Portal1:
    rect = pygame.Rect(300, 190, 50, 70)
    hitrect = pygame.Rect(300, 190, 5, 70)
    color = pygame.Color('orange')
    normal = pygame.Vector2(1, 0)


class Portal2:
    rect = pygame.Rect(500, 400, 70, 50)
    hitrect = pygame.Rect(500, 445, 70, 5)
    color = pygame.Color('blue')
    normal = pygame.Vector2(0, -1)


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
            Player.rect.center = Player.position
            
            Player.acceleration *= 0

            if Player.rect.colliderect(Portal1.hitrect):
                portal_angle = Player.velocity.angle_to(Portal2.normal)
                Player.position = Portal2.rect.center
                Player.velocity.rotate_ip(portal_angle)

            if Player.rect.colliderect(Portal2.hitrect):
                portal_angle = Player.velocity.angle_to(Portal1.normal)
                Player.position = Portal1.rect.center
                Player.velocity.rotate_ip(portal_angle)

            pygame.draw.circle(self.screen, Player.color, Player.position, Player.radius)
            pygame.draw.rect(self.screen, Portal1.color, Portal1.rect)#, 5)
            pygame.draw.rect(self.screen, Portal2.color, Portal2.rect)#, 5)
            
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
