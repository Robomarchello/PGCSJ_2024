import pygame
from pygame.locals import *
from src.engine import State, Debug, AssetManager
from src.engine.save_manager import SaveManager
from src.engine.constants import SCREENSIZE, LEVELS_PATH
from src.engine.objects.player import Player, Controller
from src.engine.physics_handler import PhysicsHandler
from src.engine.level import LevelManager
from src.engine.camera import Camera
from src.engine.space import SpaceBackground
from src.states.transition import TransitionFade
import src.states as states


class Game(State):
    def __init__(self):
        super().__init__()
        self.surface = pygame.Surface(SCREENSIZE)

        # Temporary!!
        self.end_screen = AssetManager.images['end_screen'].convert()

        self.transition = TransitionFade(2)

        self.space_backgroud = SpaceBackground()
        self.player = Player()
        rect = pygame.Rect(0, 0, 150, 150)

        self.physics_handler = PhysicsHandler(self.player, [], [])
        self.controller = Controller(self.player, rect, self.physics_handler)
        
        self.level_manager = LevelManager(
            player=self.player,
            controller=self.controller,
            physics_handler=self.physics_handler,
            transition=self.transition,
        )

        Camera.initialize(self.player)

        self.level_manager.start_level()

        # update and draw queues
        self.update_queue = [
            Camera,
            self.player,
            self.controller,
            self.physics_handler,
            self.level_manager,
            self.space_backgroud,
            self.transition,
        ]
        self.draw_queue = [
            self.space_backgroud,
            self.physics_handler,
            self.level_manager,
            self.controller,
            self.player,
            self.transition,
        ]

    def on_start(self):
        pass
    
    def on_exit(self):
        self.player.jet_channel.stop()

    def draw(self):
        self.surface.fill((0, 0, 0))

        for obj in self.draw_queue:
            obj.draw(self.surface)

        Debug.add_text(self.manager.clock.get_fps())
        Camera.debug_draw()

        # such a temporary thing!! To be removed
        if self.level_manager.level_index == 30:
            self.surface.blit(
                self.end_screen, (0, 0)
            )

    def update(self, delta):
        for obj in self.update_queue:
            obj.update(delta)

    def handle_event(self, event):
        self.controller.handle_event(event)

        if event.type == KEYDOWN:
            if event.key == K_r:
                # Level restart
                self.transition.function = self.level_manager.start_level
                self.transition.start(0.5)

            if event.key == K_p:
                if Debug.enabled:
                    SaveManager.erase_data()
                
            if event.key == K_ESCAPE:
                self.manager.next_state = states.Menu()
                SaveManager.save_data()
