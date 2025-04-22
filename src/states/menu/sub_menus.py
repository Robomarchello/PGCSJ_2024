import pygame
from pygame.locals import *
from src.engine.gui import GUInterface
from src.engine.asset_manager import AssetManager
import src.engine.config as c


class BaseSubMenu:
    def __init__(self, position: pygame.Vector2):
        self.position = position
        self.interface = GUInterface()

    def draw(self, surface):
        self.interface.draw(surface)

    def update(self, delta):
        self.interface.update(delta)

    def set_enabled(self, enabled: bool):
        self.interface.set_enabled(enabled)

    def set_offset(self, x, y):
        self.interface.set_offset(x, y)

    def handle_event(self, event):
        self.interface.handle_event(event)


class PlayMenu(BaseSubMenu):
    def __init__(self):
        super().__init__(pygame.Vector2(c.SCREEN_W / 2, c.SCREEN_H / 2))

        self.interface.add_label(
            font=AssetManager.fonts['font_24'],
            text='HEYYYY DUDE',
            color=pygame.Color('white'),
            antialias=False,
            anchors={
                'centerx': c.SCREEN_W / 2,
                'top': 50
            }
        )

class SettingsMenu(BaseSubMenu):
    def __init__(self):
        super().__init__(pygame.Vector2(c.SCREEN_W / 2 + 1000, c.SCREEN_H / 2))
        self._position = self.position.copy()
        self.scroll = pygame.Vector2()

        self.interface.add_label(
            font=AssetManager.fonts['font_24'],
            text='SETTINGS HELL YEAH',
            color=pygame.Color('white'),
            antialias=False,
            anchors={
                'centerx': c.SCREEN_W / 2 + 1000,
                'top': 50
            }
        )

    def update(self, delta):
        super().update(delta)
        self.position = self._position + self.scroll

    def handle_event(self, event):
        super().handle_event(event)
        if event.type == MOUSEWHEEL:
            self.scroll.y += -event.y * 25