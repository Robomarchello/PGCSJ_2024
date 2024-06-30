import pygame
from pygame import Vector2
from pygame.locals import MOUSEBUTTONDOWN, MOUSEBUTTONUP
from src.engine.constants import SCREEN_H
import src.engine.constants as c


class Player:
    radius = 25

    def __init__(self):
        self.position = Vector2(100, SCREEN_H / 2)
        self.velocity = Vector2(0, 0)
        self.acceleration = Vector2(0, 0)

        self.freeze = False

    def update(self, delta):
        if not self.freeze:
            self.velocity += self.acceleration * delta * c.SPEED_FACTOR
            self.position += self.velocity * delta * c.SPEED_FACTOR

        ...

        self.acceleration *= 0 

    def draw(self, surface):
        pygame.draw.circle(surface, 'red', self.position, self.radius)


class Controller:
    def __init__(self, player, rect):
        self.player = player
        self.rect = rect

        self.preview_balls = 7

        self.holding = False
        self.difference = pygame.Vector2(0, 0)
        
        self.mouse_pos = pygame.mouse.get_pos()

    def draw(self, surface):
        pygame.draw.rect(surface, 'blue', self.rect)

        start_pos = [self.rect.centerx, self.rect.centery]
        for n in range(self.preview_balls):
            start_pos[0] += self.difference[0] * 0.2
            start_pos[1] += self.difference[1] * 0.2

            if self.holding:
                pygame.draw.circle(surface, 'green', start_pos, 3)

        if self.holding:
            pygame.draw.circle(surface, 'grey', self.mouse_pos, 10)

    def update(self):
        self.mouse_pos = pygame.mouse.get_pos()

        if self.holding:
            self.difference = self.player.position - self.mouse_pos

        self.rect.center = self.player.position

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if self.rect.collidepoint(self.mouse_pos):
                self.holding = True

        if event.type == MOUSEBUTTONUP:
            if self.holding:
                self.difference = self.player.position - self.mouse_pos
                norm_diff = self.difference.normalize()
                magnitude = self.difference.magnitude() * 0.01

                force = norm_diff * magnitude #** 2)
                self.player.acceleration += force

                self.holding = False