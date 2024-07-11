import pygame
from pygame.locals import KEYDOWN, K_r
from src.engine import State, Debug, AssetManager
from src.engine.constants import *
from src.engine.player import Player, Controller
from src.engine.objects import ObjectHandler
from src.engine.level import Level, LevelManager
from src.engine.camera import Camera
from src.states.transition import TransitionFade
from src.engine.space import SpaceBackground


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
    
        self.level_manager.next_level()
        self.level = self.level_manager.crnt_level

    def on_start(self):
        print('start')
    
    def on_exit(self):
        print('exit')

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


    def update(self, delta):
        self.level = self.level_manager.crnt_level
        Camera.update(delta)

        self.player.update(delta)
        self.controller.update(delta)
        self.object_handler.update(delta)
        self.level.update(delta)
        self.level_manager.update(delta)

        self.transition.update(delta)

    def handle_event(self, event):
        self.controller.handle_event(event)

        if event.type == KEYDOWN:
            if event.key == K_r:
                self.transition.function = self.level.restart
                self.transition.start(0.5)
