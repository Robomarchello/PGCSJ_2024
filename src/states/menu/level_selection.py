import pygame
from pygame.locals import *
from src.engine.asset_manager import AssetManager
from src.engine.gui.menu_buttons import ToPlayMenuButton
import src.engine.config as c
from src.engine.gui.nine_slice import NineSlice
from src.states.menu.sub_menus import BaseSubMenu


class LevelSelectionMenu(BaseSubMenu):
    def __init__(self, manager):
        position = pygame.Vector2(
            c.SCREEN_W / 2 + c.SCREEN_W + 200, 
            c.SCREEN_H / 2
        )
        super().__init__(position, manager)
        self._position = self.position.copy()
        self.scroll = pygame.Vector2()

        self.ui_body = pygame.Rect(0, 0, c.SCREEN_W * 0.8, c.SCREEN_H * 0.8)
        self._update_ui_body()
        self.body_slice = NineSlice(AssetManager.images['body_slice'])
        self.body_slice_surf = self.body_slice.as_surface(self.ui_body)

        self.interface.add_label(
            font=AssetManager.fonts['font_48'],
            text='Level Selection',
            color=pygame.Color('white'),
            antialias=False,
            anchors={
                'centerx': self._position.x,
                'top': 40 * self.reference_scale
            }
        )
        anchors = {
            'left': self.rect.left,
            'centery': c.SCREEN_H / 2
        }
        self.interface.add_button(ToPlayMenuButton(self.manager.to_play_menu, anchors))

    def draw(self, surface):
        surface.blit(self.body_slice_surf, self.ui_body.topleft)
        super().draw(surface)

    def update(self, delta):
        self._update_ui_body()
        super().update(delta)

    def _update_ui_body(self):
        self.position = self._position + self.scroll

        self.ui_body.bottom = self.rect.bottom - 20 * self.reference_scale + self.interface.offset.y
        self.ui_body.centerx = self.position.x + self.interface.offset.x

    def handle_event(self, event):
        super().handle_event(event)
        if event.type == MOUSEWHEEL:
            self.scroll.y += -event.y * 25
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.manager.to_play_menu()