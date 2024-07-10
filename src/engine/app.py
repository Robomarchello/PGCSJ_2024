import asyncio
import pygame
from pygame.locals import *
from .constants import *
from .asset_manager import AssetManager
AssetManager.load_assets(ASSETS_PATH)
AssetManager.load_fonts_json(FONTS_JSON_PATH)
from .state_machine import StateMachine, State
from .screen import Screen
from .utils import Debug


class App(StateMachine):
    def __init__(self, initial_state: State):
        super().__init__(initial_state)

        self.clock = pygame.time.Clock()
        self.screen = Screen(SCREENSIZE, TITLE)        

    async def loop(self):
        while True:
            self.handle_events()
            
            delta = self.get_delta()

            self.update(delta)
            self.draw(self.screen.draw_surface)

            Debug.draw_queue(self.screen.draw_surface)

            self.screen.update_window()
            pygame.display.update()
            self.clock.tick(FPS)

            await asyncio.sleep(0)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                raise SystemExit
            
            #if event.type == WINDOWSIZECHANGED:
            #    self.screen.on_resize((event.x, event.y))

            Debug.handle_event(event)
            self.active_state.handle_event(event)


    def get_delta(self):
        delta_time = self.clock.get_time() / 1000

        return delta_time
