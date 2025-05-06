import pygame
from pygame.locals import *
import src.engine.config as c
from src.engine.level.level_manager import LevelManager
from src.engine.message_system import MessageHandler
from src.engine.objects.player import Controller
from . import GUInterface, IconButton, NineSlice
from src.engine.asset_manager import AssetManager


class ArrowButton(IconButton):
    def __init__(self, func):
        rect = pygame.Rect(0, 0, 50, 50)
        icon = AssetManager.images['arrow_up']
        self.angle = 0
        super().__init__(
            rect=rect,
            base=None,
            base_hover=None,
            icon=icon,
            func=func,
            func_args=())
        
        # self.hover_sound = 
        
    def _draw_icon(self, surface):
        icon_rotated = pygame.transform.rotate(self.icon, self.angle)
        icon_rect = icon_rotated.get_rect(center=self.rect.center)

        surface.blit(icon_rotated, icon_rect.topleft)


class HintButton(IconButton):
    def __init__(self, func):
        rect = pygame.Rect(0, 0, 50, 50)

        self.locked = True
        self.icon_locked = AssetManager.images['hint_locked'].convert_alpha()
        self.icon_unlocked = AssetManager.images['hint_unlocked'].convert_alpha()
        self.angle = 0
        super().__init__(
            rect=rect,
            base=None,
            base_hover=None,
            icon=self.icon_locked,
            func=func,
            func_args=())
        
    def _update_icon(self):
        self.icon = self.icon_locked if self.locked else self.icon_unlocked
            
    def update(self, delta):
        self._update_icon()
        return super().update(delta)
    
    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.hovered:
                    self.func(self.locked)

                    
class InfoBar:
    def __init__(self, controller: Controller, level_manager: LevelManager):
        self.interface = GUInterface()

        self.controller = controller

        self.rect = pygame.FRect(0, c.SCREEN_H - 50, 100, 250)
        self.rect.right = c.SCREEN_W - 20
        self.body_slice = NineSlice(AssetManager.images['button_slice'])
        self.body_surf = self.body_slice.as_surface(self.rect)

        self.arrow_button = ArrowButton(func=self.toggle_reveal)
        self.interface.add_button(self.arrow_button)

        self.hint_button = HintButton(self.hint_reveal)
        self.interface.add_button(self.hint_button)

        self.level_manager = level_manager
        self.level_index = self.level_manager.level_index
        self.levels_total = len(self.level_manager.levels)
        
        self.level_label = self.interface.add_label(
            AssetManager.fonts['font_24'],
            f'{self.level_index}/{self.levels_total}',
            (245, 232, 200)
        )

        self.index_last = self.level_manager.level_index
        self.launch_last = None
        self.launches = 0
        self.launch_threshold = 5

        self.revealed = False
        self.reveal_y = {
            False: c.SCREEN_H - 50,
            True: c.SCREEN_H - 220
        }
        self.reveal_angle = {
            False: 0,
            True: 180
        }

        self.processing_sound = AssetManager.sounds['reject']
        self.success_sound = AssetManager.sounds['success']

    def hint_reveal(self, locked):
        if locked:
            launches_left = self.launch_threshold - self.launches
            MessageHandler.post(f'Processing... Hint unlocks in {launches_left} launches.', sound=self.processing_sound)
        else:
            MessageHandler.post('Hint activated!', sound=self.success_sound)

            launch_point = self.controller.launch_point
            if launch_point is not None:
                launch_point.solution_revealed = True

    def toggle_reveal(self):
        self.revealed = not self.revealed

    def draw(self, surface):
        surface.blit(self.body_surf, self.rect.topleft)
        self.interface.draw(surface)

    def update(self, delta):
        self.interface.update(delta)
        
        speed = delta * c.SPEED_FACTOR * 0.1
        change = (self.reveal_y[self.revealed] - self.rect.top) * speed
        self.rect.top += change

        target_angle = self.reveal_angle[self.revealed]
        angle_diff = target_angle - self.arrow_button.angle
        angle_step = (angle_diff) * speed
        self.arrow_button.angle += angle_step

        self._update_hint_state()
        self._update_level_index()
        self._update_anchors()

    def _update_hint_state(self):
        if (self.controller.launch_point is None and
            self.launch_last is not None): 
            self.launches += 1
        self.launch_last = self.controller.launch_point
        if self.launches >= self.launch_threshold:
            self.hint_button.locked = False
        else:
            self.hint_button.locked = True

        if self.index_last != self.level_manager.level_index:
            self.index_last = self.level_manager.level_index
            self.launches = 0

    def _update_level_index(self):
        if self.level_index != self.level_manager.level_index:
            self.level_index = self.level_manager.level_index
            self.level_label.set_text(f'{self.level_index}/{self.levels_total}')

    def _update_anchors(self):
        self.arrow_button.anchors = {'top': self.rect.top, 'centerx': self.rect.centerx}
        self.hint_button.anchors = {'top': self.rect.top+80, 'centerx': self.rect.centerx}
        self.level_label.anchors = {'top': self.rect.top+180, 'centerx': self.rect.centerx}
        self.interface.update_anchors()

    def handle_event(self, event):
        self.interface.handle_event(event)