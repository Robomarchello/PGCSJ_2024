import pygame
from pygame.locals import *

from src.engine import State, AssetManager
from src.engine.utils import clamp
from src.engine.constants import *
import src.engine.constants as c
from src.engine.gui import *
import src.states as states


class Settings(State):
    def __init__(self):
        super().__init__()
        self.surface = pygame.Surface(SCREENSIZE)

        self.interface = GUInterface()

        back_button = BackButton(self.to_menu)
        back_button._rect.top = SCREEN_H - 150
        add_vol_btn = ChangeVolButton((200, 300), '<', self.change_volume, -0.1)
        sub_vol_btn = ChangeVolButton((1024-300, 300), '>', self.change_volume, 0.1)

        self.interface.add_button(back_button)
        self.interface.add_button(add_vol_btn)
        self.interface.add_button(sub_vol_btn)

        self.interface.add_label(
            font=AssetManager.fonts['font_72'],
            text='Settings',
            color=pygame.Color('white'),
            antialias=False,
            anchors={
                'centerx': SCREEN_W / 2,
                'top': 50
            }
        )

        self.volume_label = self.interface.add_label(
            font=AssetManager.fonts['font_36'],
            text=f'Volume: {round(c.VOLUME, 3)}',
            color=pygame.Color('white'),
            antialias=False,
            anchors={
                'centerx': SCREEN_W / 2,
                'top': 315
            }
        )

    def change_volume(self, value):
        c.VOLUME = clamp(c.VOLUME + value, 0.0, 1.0)
        AssetManager.set_volume(c.VOLUME)
        AssetManager.sounds['no_vol_check'].play()

        self.volume_label.set_text(f'Volume: {round(c.VOLUME, 3)}')

    def to_menu(self):
        self.manager.next_state = states.Menu()

    def update(self, delta):
        self.interface.update(delta)

    def draw(self):
        self.surface.fill((0, 0, 0))

        self.interface.draw(self.surface)

    def handle_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.to_menu()
        
        self.interface.handle_event(event)

    def on_start(self):
        pass
    
    def on_exit(self):
        pass