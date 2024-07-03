import pygame
from src.engine.objects import *


class Level:
    def __init__(self, player, object_handler):
        objects = []
        objects.append(BlackHole((250, 384), 50))
        objects.append(BlackHole((500, 384), 50))
        objects.append(ForceZone((0, 0.3), (300, 200, 300, 300)))

        portal_1 = Portal(
            pygame.Rect(300, 190, 50, 70), 
            pygame.Rect(345, 190, 5, 70), 
            pygame.Vector2(1, 0), pygame.Color('yellow')
        )
        portal_2 = Portal(
            pygame.Rect(500, 400, 70, 50), 
            pygame.Rect(500, 445, 70, 5), 
            pygame.Vector2(0, -1), pygame.Color('blue')
        )
        objects.append(PortalPair(portal_1, portal_2))
        obstacles = []
        obstacles.append(Asteroid((500, 280), pygame.Vector2(4.3, 0), 20, 15))
        obstacles.append(Asteroid((500, 488), pygame.Vector2(-4.3, 0), 20, 15))
        

        self.player = player
        self.object_handler = object_handler

        self.object_handler.objects = objects
        self.object_handler.obstacles = obstacles

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