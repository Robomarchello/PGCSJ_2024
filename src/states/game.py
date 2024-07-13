import pygame
from pygame.locals import *
from src.engine import State, Debug, AssetManager
from src.engine.constants import *
from src.engine.player import Player, Controller
from src.engine.objects import ObjectHandler
from src.engine.level import Level, LevelManager
from src.engine.camera import Camera
from src.engine.space import SpaceBackground
from src.states.transition import TransitionFade
import src.states as states


class Game(State):
    def __init__(self):
        super().__init__()
        self.surface = pygame.Surface(SCREENSIZE)

        self.player = Player()
        rect = pygame.Rect(0, 0, 150, 150)
        rect.center = self.player.position

        self.space_backgroud = SpaceBackground(50)

        Camera.initialize(self.player)

        self.transition = TransitionFade(2)

        self.object_handler = ObjectHandler(self.player, [], [])
        self.controller = Controller(self.player, rect, self.object_handler)
        # self.level = Level(self.player, self.controller, self.object_handler)
        self.level_manager = LevelManager(
            LEVELS_PATH, self.player, self.controller, 
            self.object_handler, self.transition
        )

        self.level_manager.progress_init('src/assets/other/save.json')
    
        self.level_manager.next_level()
        self.level = self.level_manager.crnt_level

    def on_start(self):
        pass
    
    def on_exit(self):
        self.player.jet_channel.stop()

    def draw(self):
        self.surface.fill((0, 0, 0))

        self.space_backgroud.draw(self.surface)

        self.object_handler.draw(self.surface)
        self.level.draw(self.surface)

        self.controller.draw(self.surface)
        self.player.draw(self.surface)

        self.transition.draw(self.surface)

        Debug.add_text(self.manager.clock.get_fps())
        Camera.debug_draw()

        if self.level_manager.level_index == 31:
            self.surface.blit(
                AssetManager.images['end_screen'], (0, 0)
            )

    def update(self, delta):
        self.level = self.level_manager.crnt_level
        Camera.update(delta)

        self.player.update(delta)
        self.controller.update(delta)
        self.object_handler.update(delta)
        self.level.update(delta)
        self.level_manager.update(delta)

        self.space_backgroud.update(delta)

        self.transition.update(delta)

    def handle_event(self, event):
        self.controller.handle_event(event)

        if event.type == KEYDOWN:
            if event.key == K_r:
                self.transition.function = self.level.restart
                self.transition.start(0.5)

            if event.key == K_ESCAPE:
                self.manager.next_state = states.Menu()
