import pygame
from pygame.locals import *
from src.engine.asset_manager import AssetManager
from src.engine.gui.menu_buttons import NewLevelButton, ToPlayMenuButton
import src.engine.config as c
from src.engine.gui.nine_slice import NineSlice
from src.engine.save_manager import SaveManager
from src.engine.utils import clamp
from src.states.game import Game
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

        self.bounds = [-100, 1000]

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

        self.add_buttons()

    def add_buttons(self):
        self.interface.buttons = []
        anchors = {
            'left': self.rect.left,
            'centery': c.SCREEN_H / 2
        }
        self.interface.add_button(ToPlayMenuButton(self.manager.to_play_menu, anchors))

        self.generate_levels()

    def generate_levels(self):
        SaveManager.get_save()

        padding_left = 30 * self.reference_scale
        padding_top = 30 * self.reference_scale
        for lvl_i, completed in enumerate(SaveManager.data['levels_completed']):
            x = lvl_i % 5
            y = (lvl_i // 5)

            x_pos = self.ui_body.x + padding_left + x * (c.SCREEN_W * 0.15)
            y_pos = self.ui_body.y + padding_top + y * (c.SCREEN_H * 0.17)

            button = NewLevelButton(lvl_i, (x_pos, y_pos), self.level_button_func)
            button.completed = completed
            self.interface.add_button(button)

        self.ui_body.height = y_pos - self.ui_body.y + (c.SCREEN_H * 0.17) + 15
        self.body_slice_surf = self.body_slice.as_surface(self.ui_body)
        self.bounds[1] = y_pos - c.SCREEN_H * 0.7

    def level_button_func(self, level, completed):
        if completed:
            game_state = Game()
            game_state.level_manager.level_index = level
            game_state.level_manager.start_level()
            # this is crazy...
            self.manager.manager.next_state = game_state
        else:
            # shake screen
            # play sound
            pass

    def draw(self, surface):
        surface.blit(self.body_slice_surf, self.ui_body.topleft)
        super().draw(surface)

    def update(self, delta):
        self.scroll.y = clamp(self.scroll.y, self.bounds[0], self.bounds[1])
        self._update_ui_body()
        super().update(delta)

    def _update_ui_body(self):
        self.position = self._position + self.scroll

        self.ui_body.top = self.rect.top + 130 * self.reference_scale + self.interface.offset.y
        self.ui_body.centerx = self.position.x + self.interface.offset.x

    def handle_event(self, event):
        super().handle_event(event)
        if event.type == MOUSEWHEEL:
            self.scroll.y += -event.y * 25
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.manager.to_play_menu()