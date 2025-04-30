import pygame
from pygame.locals import *

import src.engine.config as c
from src.engine import AssetManager
from src.engine.gui import *
from src.states.menu.base_submenu import BaseSubMenu


class PlayMenu(BaseSubMenu):
    def __init__(self, manager):
        position = pygame.Vector2(c.SCREEN_AREA.center)
        super().__init__(position, manager)

        self.clickable_area = pygame.Rect(0, 0, c.SCREEN_W * 0.8, c.SCREEN_H)
        self.clickable_area.center = self.position

        self.interface.add_label(
            font=AssetManager.fonts['font_48'],
            text='Mediocre Game with Golf-Like',
            color=pygame.Color('white'),
            antialias=False,
            anchors={
                'centerx': c.SCREEN_W / 2,
                'top': 50 * self.reference_scale
            }
        )
        self.interface.add_label(
            font=AssetManager.fonts['font_48'],
            text='Gameplay In Space!',
            color=pygame.Color('white'),
            antialias=False,
            anchors={
                'centerx': c.SCREEN_W / 2,
                'top': 110 * self.reference_scale
            }
        )
        self.interface.add_label(
            font=AssetManager.fonts['font_42'],
            text='Click anywhere to play',
            color=pygame.Color('white'),
            antialias=False,
            anchors={
                'centerx': c.SCREEN_W / 2,
                'top': c.SCREEN_H - 120 * self.reference_scale
            }
        )
        # buttons are added in Menu class
        self.interface.add_button(ToSettingsButton(self.manager.to_settings))
        self.interface.add_button(ToLevelSelectionButton(self.manager.to_level_selection))

    def update(self, delta):
        super().update(delta)
        self._update_clickable_area()
    
    def _update_clickable_area(self):
        self.clickable_area.center = self.position + self.interface.offset

    def handle_event(self, event):
        super().handle_event(event)
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                raise SystemExit
            else:
                self.manager.to_game()

        if event.type == MOUSEBUTTONDOWN:
            mp = pygame.mouse.get_pos()
            if self.clickable_area.collidepoint(mp):
                self.manager.to_game()
