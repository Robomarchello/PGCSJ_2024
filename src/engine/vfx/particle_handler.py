import pygame
from pygame.locals import *
from .particles import Particle
from src.engine.constants import SCREENSIZE


# imagine me handling all the particles
class ParticleHandler:
    surface = pygame.Surface(SCREENSIZE, SRCALPHA)
    emitters = []

    @classmethod
    def draw(cls, screen):
        for emitter in cls.emitters:
            emitter.draw(cls.surface)

        screen.blit(cls.surface, (0, 0))

    