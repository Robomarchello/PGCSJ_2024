import asyncio
import pygame
from pygame.locals import *

from src.engine.config import *
from src.engine.state_machine import StateMachine, State
from src.engine.screen import Screen
from src.engine.utils import Debug


class App(StateMachine):
    def __init__(self, initial_state: State):
        super().__init__(initial_state)

        self.clock = pygame.time.Clock()
        self.screen = Screen(SCREENSIZE, TITLE) 
        
    async def loop(self):
        while True:
            self.handle_events()
            
            delta = self.clock.get_time() / 1000

            self.update(delta)
            self.draw(self.screen.draw_surface)

            Debug.draw_queue(self.screen.draw_surface)

            pygame.display.update()
            self.clock.tick(FPS)

            await asyncio.sleep(0)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                raise SystemExit
            

            Debug.handle_event(event)
            self.active_state.handle_event(event)