import pygame
from pygame.locals import BLEND_SUB
import src.engine.config as c
from src.engine.enums import TransitionState
from src.engine.base import Base
from src.engine.utils import clamp, ease_in_cubic, ease_out_cubic


class Transition(Base):
    def __init__(self, duration, function=None, *args):
        self.surface = pygame.Surface(c.SCREENSIZE)
        
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
        if self.state == TransitionState.INACTIVE:
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





class TransitionClose(Transition):
    def __init__(self, duration, function=None, *args):
        super().__init__(duration, function, *args)

        self.rect_top = pygame.Rect(0, 0, c.SCREEN_W, 0)
        self.rect_bottom = pygame.Rect(0, 0, c.SCREEN_W, 0)

        self.max_height = c.SCREEN_H * 0.55

    def draw(self, surface):
        progress = self.timer / self.half_duration
        height = 0
        if self.state == TransitionState.FADE_IN:
            height = self.max_height * ease_out_cubic(1 - progress)

        elif self.state == TransitionState.FADE_OUT:
            height = self.max_height * ease_in_cubic(progress)
        
        self.rect_top.height = height
        self.rect_bottom.height = height
        self.rect_bottom.bottom = c.SCREEN_H

        pygame.draw.rect(surface, (0, 0, 0), self.rect_top)
        pygame.draw.rect(surface, (0, 0, 0), self.rect_bottom)        