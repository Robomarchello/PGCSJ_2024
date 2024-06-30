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

        self.mass = 1

        self.freeze = True

    def update(self, delta):
        if not self.freeze:
            self.velocity += self.acceleration * delta * c.SPEED_FACTOR
            self.position += self.velocity * delta * c.SPEED_FACTOR

        ...

        self.acceleration *= 0 

    def draw(self, surface):
        pygame.draw.circle(surface, 'red', self.position, self.radius)


class Controller:
    def __init__(self, player, rect, physics_handler):
        self.player = player
        self.rect = rect

        self.physics_handler = physics_handler

        self.preview_balls = 7

        self.holding = False
        self.difference = pygame.Vector2(0, 0)

        self.launch_force = pygame.Vector2()
        
        self.mouse_pos = pygame.mouse.get_pos()

    def draw(self, surface):
        pygame.draw.rect(surface, 'blue', self.rect)

        if self.holding:
            start_vel = self.launch_force
        else:
            start_vel = self.player.velocity

        prediction = self.physics_handler.predict_player(
            0.016, self.player.position, start_vel, self.player.acceleration, 100
            )
        
        for pos in prediction:
            pygame.draw.circle(surface, 'green', pos, 3)

        start_pos = [self.rect.centerx, self.rect.centery]
        for n in range(self.preview_balls):
            start_pos[0] += self.difference[0] * 0.2
            start_pos[1] += self.difference[1] * 0.2

            #if self.holding:
            #    pygame.draw.circle(surface, 'green', start_pos, 3)

        if self.holding:
            pygame.draw.circle(surface, 'grey', self.mouse_pos, 10)

    def update(self, delta):
        self.mouse_pos = pygame.mouse.get_pos()

        if self.holding:
            self.difference = self.player.position - self.mouse_pos
            norm_diff = self.difference.normalize()
            magnitude = self.difference.magnitude() * 0.03

            self.launch_force = norm_diff * magnitude

        self.rect.center = self.player.position

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if self.rect.collidepoint(self.mouse_pos):
                self.holding = True

        if event.type == MOUSEBUTTONUP:
            if self.holding:
                self.player.velocity += self.launch_force
                self.player.freeze = False

                self.holding = False