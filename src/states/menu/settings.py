import pygame
from pygame.locals import *

import src.engine.config as c
from src.engine import AssetManager
from src.engine.utils import clamp
from src.engine.config import *
from src.engine.gui import *
from src.states.menu.base_submenu import BaseSubMenu


class SettingsMenu(BaseSubMenu):
    def __init__(self, manager):
        position = pygame.Vector2(
            c.SCREEN_W / 2 - c.SCREEN_W - 200, 
            c.SCREEN_H / 2
        )
        super().__init__(position, manager)


        self.ui_body = pygame.Rect(0, 0, c.SCREEN_W * 0.7, c.SCREEN_H * 0.8)
        self._update_ui_body()
        self.body_slice = NineSlice(AssetManager.images['body_slice'])
        self.body_slice_surf = self.body_slice.as_surface(self.ui_body)
        
        # title
        self.interface.add_label(
            font=AssetManager.fonts['font_48'],
            text='Settings',
            color=pygame.Color('white'),
            antialias=False,
            anchors={
                'centerx': self.position.x,
                'top': 50 * self.reference_scale
            }
        )
        # Back to play menu button
        to_play_button = ToPlayMenuButton(
            func=self.manager.to_play_menu, 
            anchors= {'right': self.rect.right, 'centery': c.SCREEN_H / 2}
        )
        self.interface.add_button(to_play_button)

        padding_left = 50 * self.reference_scale
        padding_top = 40 * self.reference_scale
        # fullscreen option
        self.interface.add_label(
            font=AssetManager.fonts['font_42'],
            text='SFX Volume',
            color=pygame.Color(220, 220, 220),
            antialias=False,
            anchors={
                'left': self.ui_body.left + padding_left,
                'top': self.ui_body.top + padding_top
            }
        )
        
        self.interface.add_slider(
            length=300,
            start_value=0.5,
            value_range=(0, 1),
            anchors={
                'right': self.ui_body.right - padding_left,
                'top': self.ui_body.top + padding_top + 20 * self.reference_scale
            },
            step=0.05,
            on_change=self.master_volume_update,
        )
        # --- Music Volume
        self.interface.add_label(
            font=AssetManager.fonts['font_42'],
            text='Music Volume',
            color=pygame.Color(220, 220, 220),
            antialias=False,
            anchors={
                'left': self.ui_body.left + padding_left,
                'top': self.ui_body.top + padding_top + 100 * self.reference_scale
            }
        )        
        self.interface.add_slider(
            length=300,
            start_value=c.MUSIC_VOLUME,
            value_range=(0, 0.7),
            anchors={
                'right': self.ui_body.right - padding_left,
                'top': self.ui_body.top + padding_top + 120 * self.reference_scale
            },
            step=0.025,
            on_change=self.music_volume_update,
        )
        AssetManager.set_music_volume(c.MUSIC_VOLUME)

        self.clack_channel = pygame.mixer.Channel(0)

        asteroid_img = AssetManager.images['asteroid_menu'].convert()
        asteroid_img.set_colorkey((255, 0, 0))
        self.asteroid_image = UIImage(
            asteroid_img,
            anchors={
                'left': self.rect.left + 50 * self.reference_scale, 
                'top': self.rect.top + 50 * self.reference_scale
                },
            )
        self.interface.add_image(self.asteroid_image)

    def master_volume_update(self, volume):
        if not self.clack_channel.get_busy():
            self.clack_channel.play(AssetManager.sounds['clack'])
        AssetManager.set_volume(volume)

    def music_volume_update(self, volume):
        if not self.clack_channel.get_busy():
            self.clack_channel.play(AssetManager.sounds['clack'])
        c.MUSIC_VOLUME = volume
        AssetManager.set_music_volume(volume)

    def draw(self, surface):
        surface.blit(self.body_slice_surf, self.ui_body.topleft)
        super().draw(surface)
        # pygame.draw.rect(surface, (255, 0, 0), self.ui_body, width=1)

    def update(self, delta):
        self._update_ui_body()
        super().update(delta)

    def _update_ui_body(self):
        self.ui_body.bottom = self.rect.bottom - 20 * self.reference_scale + self.interface.offset.y
        self.ui_body.centerx = self.position.x + self.interface.offset.x

    def handle_event(self, event):
        super().handle_event(event)
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.manager.to_play_menu()