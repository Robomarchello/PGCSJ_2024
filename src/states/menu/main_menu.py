import pygame
from pygame.locals import *

from src.engine import State, AssetManager
from src.engine.config import *
import src.engine.config as c
from src.engine.gui import *
import src.states as states


class Menu(State):
    def __init__(self):
        super().__init__()
        self.surface = pygame.Surface(SCREENSIZE)

        AssetManager.set_volume(c.VOLUME)

        self.play_button = PlayButton(self.to_game)
        self.level_select_button = LevelSelectionButton(self.to_level_selection)
        self.settings_button = SettingsButton(self.to_settings)
        self.exit_button = ExitButton(self.exit_app)

        self.interface = GUInterface()
        self.interface.add_button(self.play_button)
        self.interface.add_button(self.level_select_button)
        self.interface.add_button(self.settings_button)
        self.interface.add_button(self.exit_button)

        self.interface.add_label(
            font=AssetManager.fonts['font_24'],
            text=TITLE,
            color=pygame.Color('white'),
            antialias=False,
            anchors={
                'centerx': SCREEN_W / 2,
                'top': 50
            }
        )

    def on_start(self):
        pass
    
    def on_exit(self):
        pass

    def to_game(self):
        self.manager.next_state = states.Game()

    def to_level_selection(self):
        self.manager.next_state = states.LevelSelection()

    def to_settings(self):
        self.manager.next_state = states.Settings()

    def exit_app(self):
        pygame.quit()
        raise SystemExit

    def draw(self):
        self.surface.fill((0, 0, 0))

        self.interface.draw(self.surface)

    def update(self, delta):
        self.interface.update(delta)

    def handle_event(self, event):
        self.interface.handle_event(event)
