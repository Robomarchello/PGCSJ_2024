from enum import Enum
import pygame
from pygame.locals import BLEND_SUB
from src.engine.constants import SCREENSIZE


# Define an enumeration for the two states
class TransitionState(Enum):
    FADING_IN = 1
    FADING_OUT = 2
    TURNED_OFF = 3


class Transition:
    def __init__(self, duration, function=None, *args):
        self.surface = pygame.Surface(SCREENSIZE)
        
        self.duration = duration
        self.half_duration = duration / 2
        
        self.timer = 0

        self.function = function
        self.args = args

        self.run_action = False

        self.state = TransitionState.TURNED_OFF

    def draw(self, surface):
        raise NotImplementedError("Subclasses must implement this method")

    def update(self, delta):
        if self.state == TransitionState.TURNED_OFF:
            return  
        
        self.timer -= delta

        if self.timer < 0:
            if self.state == TransitionState.FADING_IN and not self.run_action:
                self.timer = self.half_duration
                self.function(*self.args)
                self.run_action = True
                self.state = TransitionState.FADING_OUT

            elif self.state == TransitionState.FADING_OUT:
                self.state = TransitionState.TURNED_OFF
    
    def start(self, duration=None):
        if duration is not None:
            self.duration = duration
            self.half_duration = duration / 2

        self.timer = self.half_duration
        self.run_action = False
        self.state = TransitionState.FADING_IN



class TransitionFade(Transition):
    def __init__(self, duration, function=None, *args):
        super().__init__(duration, function, *args)

    def draw(self, surface):
        alpha = 255 * (self.timer / self.half_duration)
        if self.state == TransitionState.FADING_IN:
            alpha = 255 - alpha
        
        alpha = int(min(alpha, 255))
        alpha = max(0, alpha)

        self.surface.fill((alpha, alpha, alpha))
        surface.blit(self.surface, (0, 0), special_flags=BLEND_SUB)

