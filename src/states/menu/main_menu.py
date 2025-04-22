import pygame
from pygame.locals import *

from src.engine import State, AssetManager
import src.engine.config as c
from src.engine.gui import *
import src.states as states
from src.engine.space import SpaceBackground
from src.engine.camera import Camera
from .sub_menus import LevelSelectionMenu, PlayMenu, SettingsMenu


class Menu(State):
    def __init__(self):
        super().__init__()
        self.surface = pygame.Surface(c.SCREENSIZE)

        AssetManager.set_volume(c.VOLUME)

        self.space_background = SpaceBackground()

        self.play_menu = PlayMenu(self)
        self.settings_menu = SettingsMenu(self)
        self.level_selection_menu = LevelSelectionMenu(self)
        self.crnt_menu = self.play_menu
        self.next_menu = None
        
        Camera.focus = pygame.Vector2(c.SCREEN_W / 2, c.SCREEN_H / 2)

    def draw(self):
        self.space_background.draw(self.surface)

        self.crnt_menu.draw(self.surface)

        if self.next_menu is not None:
            self.next_menu.draw(self.surface)

    def update(self, delta):
        Camera.update(delta)
        self.space_background.update(delta)
        
        if self.next_menu is not None:
            Camera.focus = self.next_menu.position

            self.next_menu.set_offset(-Camera.pos[0], -Camera.pos[1])
            self.next_menu.update(delta)

            distance = (Camera.displacement - self.next_menu.position).length()
            if distance <= 100:
                self.crnt_menu.set_enabled(True)
                self.crnt_menu = self.next_menu
                self.next_menu = None
        else:
            Camera.focus = self.crnt_menu.position

        self.crnt_menu.set_offset(-Camera.pos[0], -Camera.pos[1])
        self.crnt_menu.update(delta)

    def on_start(self):
        pass
    
    def on_exit(self):
        pass

    def to_game(self):
        self.manager.next_state = states.Game()

    def to_level_selection(self):
        self.next_menu = self.level_selection_menu
        self.crnt_menu.set_enabled(False)
        self.next_menu.set_enabled(False)

    def to_settings(self):
        self.next_menu = self.settings_menu
        self.crnt_menu.set_enabled(False)
        self.next_menu.set_enabled(False)

    def to_play_menu(self):
        self.next_menu = self.play_menu
        self.crnt_menu.set_enabled(False)
        self.next_menu.set_enabled(False)

    def exit_app(self):
        pygame.quit()
        raise SystemExit

    def handle_event(self, event):
        self.crnt_menu.handle_event(event)
