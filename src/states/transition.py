import pygame
from pygame.locals import BLEND_SUB
from src.engine.constants import SCREENSIZE
from src.engine.enums import TransitionState
from src.engine.base import Base
from src.engine.utils import clamp


class Transition(Base):
    def __init__(self, duration, function=None, *args):
        self.surface = pygame.Surface(SCREENSIZE)
        
        self.duration = duration
        self.half_duration = duration / 2
        
        self.timer = 0

        self.function = function
        self.args = args

        self.state = TransitionState.INACTIVE

    def draw(self, surface):
        raise NotImplementedError("Subclasses must implement this method")

    def update(self, delta):
        if self.state == TransitionState.INACTIVE:
            return  
        
        self.timer -= delta

        if self.timer < 0:
            if self.state == TransitionState.FADE_IN:
                self._change_state(TransitionState.EXECUTING)

            elif self.state == TransitionState.FADE_OUT:
                self._change_state(TransitionState.INACTIVE)

    def _change_state(self, new_state):
        '''Handles switching states.'''
        if self.state != new_state:
            self.state = new_state

            if new_state == TransitionState.EXECUTING:
                if self.function:
                    self.function(*self.args)

                self.timer = self.half_duration
                self.state = TransitionState.FADE_OUT
    
    def start(self, duration):
        '''Starts transition'''
        self.duration = duration
        self.half_duration = duration / 2
        self.timer = self.half_duration

        self._change_state(TransitionState.FADE_IN)


class TransitionFade(Transition):
    def __init__(self, duration, function=None, *args):
        super().__init__(duration, function, *args)

    def draw(self, surface):
        alpha = 255 * (self.timer / self.half_duration)
        if self.state == TransitionState.FADE_IN:
            alpha = 255 - alpha
        
        alpha = clamp(alpha, 0, 255)

        self.surface.fill((alpha, alpha, alpha))
        surface.blit(self.surface, (0, 0), special_flags=BLEND_SUB)