import pygame
from pygame.locals import *
from src.states.game import Game
from src.engine import State, AssetManager
from src.engine.constants import *
from src.engine.gui import *


class Menu(State):
    def __init__(self):
        super().__init__()
        self.surface = pygame.Surface(SCREENSIZE)

        self.play_button = PlayButton(self.play)
        self.level_select_button = LevelSelectionButton(self.level_selection)
        self.settings_button = SettingsButton(self.to_settings)
        self.exit_button = ExitButton(self.exit_app)

        self.buttons = [
            self.play_button,
            self.level_select_button,
            self.settings_button,
            self.exit_button,
        ]

    def on_start(self):
        print('start')
    
    def on_exit(self):
        print('exit')

    def play(self):
        self.manager.next_state = Game()

    def level_selection(self):
        self.manager.next_state = LevelSelection()

    def to_settings(self):
        self.manager.next_state = Settings()

    def exit_app(self):
        pygame.quit()
        raise SystemExit
    
    def draw_title(self):
        font  = AssetManager.fonts['font_72']
        render = font.render(TITLE, True, 'white')
        rect = render.get_rect()
        rect.centerx = SCREEN_W / 2
        rect.top = 50

        self.surface.blit(render, rect.topleft)

    def draw(self):
        self.surface.fill((0, 0, 0))

        self.draw_title()

        for button in self.buttons:
            button.draw(self.surface)

    def update(self, delta):
        for button in self.buttons:
            button.update()

    def handle_event(self, event):
        for button in self.buttons:
            button.handle_event(event)


class LevelSelection(State):
    def __init__(self):
        super().__init__()
        self.surface = pygame.Surface(SCREENSIZE)

    def on_start(self):
        print('start')
    
    def on_exit(self):
        print('exit')

    def draw(self):
        self.surface.fill((0, 0, 0))

        self.draw_title()

    def draw_title(self):
        font  = AssetManager.fonts['font_72']
        render = font.render('Level Selection', True, 'white')
        rect = render.get_rect()
        rect.centerx = SCREEN_W / 2
        rect.top = 50

        self.surface.blit(render, rect.topleft)

    def handle_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.manager.next_state = Menu()


class Settings(State):
    def __init__(self):
        super().__init__()
        self.surface = pygame.Surface(SCREENSIZE)

        self.back_button = BackButton(self.to_menu)

        self.buttons = [
            self.back_button,
        ]

    def on_start(self):
        print('start')
    
    def on_exit(self):
        print('exit')

    def to_menu(self):
        self.manager.next_state = Menu()

        for button in self.buttons:
            button.draw(self.surface)

    def update(self, delta):
        for button in self.buttons:
            button.update()

    def draw(self):
        self.surface.fill((0, 0, 0))

        for button in self.buttons:
            button.draw(self.surface)

        self.draw_title()

    def draw_title(self):
        font  = AssetManager.fonts['font_72']
        render = font.render('Settings', True, 'white')
        rect = render.get_rect()
        rect.centerx = SCREEN_W / 2
        rect.top = 50

        self.surface.blit(render, rect.topleft)

    def handle_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.to_menu()
        
        for button in self.buttons:
            button.handle_event(event)
        