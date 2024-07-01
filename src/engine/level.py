import pygame
from src.engine.objects import *


class Level:
    def __init__(self, player, physics_handler):
        objects = []
        objects.append(BlackHole((250, 384), 50))
        objects.append(BlackHole((500, 384), 50))
        objects.append(ForceZone((0, 0.3), (300, 200, 300, 300)))
        obstacles = []
        obstacles.append(Asteroid((500, 280), pygame.Vector2(4.3, 0), 20, 15))
        obstacles.append(Asteroid((500, 488), pygame.Vector2(-4.3, 0), 20, 15))

        self.player = player
        self.physics_handler = physics_handler

        self.physics_handler.objects = objects
        self.physics_handler.obstacles = obstacles

        self.collectibles = []
        self.collectibles.append(
            Collectible((300, 50))
            )
    
    def update(self, delta):
        # physics handler part of game or level? I have to answer this myself
        for collectible in self.collectibles:
            if self.player.rect.colliderect(collectible.rect):
                if not collectible.picked_up:
                    collectible.picked_up = True

    def draw(self, surface):
        for collectible in self.collectibles:
            collectible.draw(surface)

    def load_level(self):
        pass