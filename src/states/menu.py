import pygame
from pygame.locals import *
from src.states.game import Game
from src.engine import State, AssetManager
from src.engine.constants import *
from src.engine.gui import Button, PlayButton, LevelSelectionButton


class Menu(State):
    def __init__(self):
        super().__init__()
        self.surface = pygame.Surface(SCREENSIZE)

        self.play_button = PlayButton(self.play)
        self.level_select_button = LevelSelectionButton(self.level_selection)

    def on_start(self):
        print('start')
    
    def on_exit(self):
        print('exit')

    def play(self):
        self.manager.next_state = Game()

    def level_selection(self):
        self.manager.next_state = LevelSelection()

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

        self.play_button.draw(self.surface)
        self.level_select_button.draw(self.surface)

    def update(self, delta):
        self.play_button.update()
        self.level_select_button.update()

    def handle_event(self, event):
        self.play_button.handle_event(event)
        self.level_select_button.handle_event(event)



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