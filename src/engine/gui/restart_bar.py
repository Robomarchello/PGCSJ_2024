import pygame
from pygame.locals import *
import src.engine.config as c
from src.engine.message_system import MessageHandler
from src.engine.objects.player import Controller
from . import GUInterface, IconButton, NineSlice
from src.engine.asset_manager import AssetManager


class RestartButton(IconButton):
    def __init__(self, func):
        rect = pygame.Rect(0, 0, 128, 128)

        base_slice = NineSlice(AssetManager.images['button_slice'])
        base_slice_hover = NineSlice(AssetManager.images['button_slice_hover'])

        icon = AssetManager.images['restart_icon'].convert_alpha()
        super().__init__(
            rect=rect,
            base=base_slice,
            base_hover=base_slice_hover,
            icon=icon,
            func=func,
            func_args=())

                    
class RestartBar:
    def __init__(self, controller: Controller, level_manager, restart_func):
        self.interface = GUInterface()

        self.controller = controller

        self.rect = pygame.FRect(0, c.SCREEN_H, c.SCREEN_W, 150)

        self.restart_button = RestartButton(func=restart_func)
        self.interface.add_button(self.restart_button)
        
        self.level_manager = level_manager
        self.level_label = self.interface.add_label(
            AssetManager.fonts['font_24'],
            'Press R To Restart',
            (245, 232, 200)
        )

        self.revealed = False
        self.reveal_y = {
            False: c.SCREEN_H,
            True: c.SCREEN_H - self.rect.height
        }

    def draw(self, surface):
        self.interface.draw(surface)

    def update(self, delta):
        self.interface.update(delta)
        
        speed = delta * c.SPEED_FACTOR * 0.1
        change = (self.reveal_y[self.revealed] - self.rect.top) * speed
        self.rect.top += change

        self._update_anchors()

    def _update_anchors(self):
        self.restart_button.anchors = {'left': 30, 'centery': self.rect.centery}
        self.level_label.anchors = {'center': self.rect.center}
        self.interface.update_anchors()

    def handle_event(self, event):
        self.interface.handle_event(event)