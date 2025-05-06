import pygame
from pygame.locals import *
from src.engine import State, Debug, AssetManager
from src.engine.save_manager import SaveManager
from src.engine.objects.player import Player, Controller
from src.engine.physics_handler import PhysicsHandler
from src.engine.level import LevelManager
from src.engine.camera import Camera
from src.engine.space import SpaceBackground
from src.states.transition import TransitionFade
from src.engine.gui.infobar import InfoBar
from src.engine.message_system import MessageHandler
import src.states as states




class Game(State):
    def __init__(self):
        super().__init__()
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
            restart_func=self.restart_level
        )

        self.level_manager.start_level()
        MessageHandler.init_font()

        self.infobar = InfoBar(self.controller, self.level_manager)

        # update and draw queues
        self.update_queue = [
            Camera,
            self.player,
            self.controller,
            self.physics_handler,
            self.level_manager,
            self.space_backgroud,
            self.infobar,
            MessageHandler,
            self.transition,
        ]
        self.draw_queue = [
            self.space_backgroud,
            self.physics_handler,
            self.level_manager,
            self.controller,
            self.player,
            self.infobar,
            MessageHandler,
            self.transition,
        ]
        self.event_handler_queue = [
            self.level_manager,
            self.controller,
            Camera,
            self.infobar
        ]

    def on_start(self):
        pass
    
    def on_exit(self):
        if self.player.jet_channel is not None:
            self.player.jet_channel.stop()

        SaveManager.save_data()

    def draw(self, surface):
        surface.fill((0, 0, 0))

        for obj in self.draw_queue:
            obj.draw(surface)

        Debug.add_text(self.manager.clock.get_fps())
        Camera.debug_draw()

        if self.level_manager.level_index == len(self.level_manager.levels):
            self.manager.next_state = states.EndScreen()

    def update(self, delta):
        for obj in self.update_queue:
            obj.update(delta)

    def restart_level(self):
        self.transition.function = self.level_manager.start_level
        self.transition.start(0.5)

    def handle_event(self, event):
        for event_handler in self.event_handler_queue:
            event_handler.handle_event(event)

        if event.type == KEYDOWN:
            if event.key == K_r:
                self.restart_level()

            if event.key == K_p:
                if Debug.enabled:
                    SaveManager.erase_data()
                
            if event.key == K_ESCAPE:
                self.manager.next_state = states.Menu()