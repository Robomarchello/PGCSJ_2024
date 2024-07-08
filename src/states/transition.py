from enum import Enum
import pygame
from pygame.locals import BLEND_SUB
#from src.engine.constants import SCREENSIZE
SCREENSIZE = (960, 540)

# Define an enumeration for the two states
class TransitionState(Enum):
    FADING_OUT = 1
    FADING_IN = 2
    TURNED_OFF = 3


class TransitionFade:
    def __init__(self, duration, function=None, *args):
        self.surface = pygame.Surface(SCREENSIZE)
        
        self.duration = duration
        self.half_duration = duration / 2
        
        self.timer = self.half_duration

        self.function = function
        self.args = args

        self.run_action = False
        self.finished = False

        # Initialize the state to FADING_OUT
        self.state = TransitionState.FADING_OUT

    def draw(self, surface):
        alpha = 255 * (self.timer / self.half_duration)
        if self.state == TransitionState.FADING_IN:
            alpha = 255 - alpha
        
        alpha = min(alpha, 255)

        self.surface.fill((125, 125, 125))
        surface.blit(self.surface, (0, 0), special_flags=BLEND_SUB)

    def update(self, delta):
        if self.finished or self.state == TransitionState.TURNED_OFF:
            return  
        
        self.timer -= delta

        if self.timer < 0:
            if self.state == TransitionState.FADING_IN and not self.run_action:
                self.timer = self.half_duration
                self.function(*self.args)
                self.run_action = True
                self.state = TransitionState.FADING_OUT

            elif self.state == TransitionState.FADING_OUT:
                print('finished.')
                self.finished = True
    
    def restart(self):
        self.timer = self.half_duration
        self.run_action = False
        self.finished = False
        self.state = TransitionState.FADING_OUT


if __name__ == '__main__':
    def hello():
        print('piska')

    transition = TransitionFade(2, hello)
    for _ in range(30):
        surf = pygame.Surface((10, 10))
        transition.update(0.1)
        transition.draw(surf)