import json
import pygame
from pygame.locals import *
from src.states.game import Game
from src.engine import State, AssetManager
from src.engine.constants import *
from src.engine.gui import *
import src.states as states


__all__ = ['Menu']

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
        self.manager.next_state = states.Game()

    def level_selection(self):
        self.manager.next_state = states.LevelSelection()

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

        self.offset = 0
        self.scroll_vel = 0
        self.scroll_acc = 0

        self.bounds = [-100, 250]

        self.level_buttons = []

        if PLATFORM == 'emscripten':
            return

        levels_num = 15
        x_num = 5
        x_offset = 200
        y_offset = 200
        crnt_pos = pygame.Vector2(50, 100)
        
        for lvl_num in range(levels_num):
            if lvl_num % x_num == 0:
                crnt_pos[0] = 50
                crnt_pos[1] += y_offset            
            
            button = LevelButton(str(lvl_num), crnt_pos.copy(), self.selected_level)
            self.level_buttons.append(button)

            crnt_pos[0] += x_offset 

        self.back_button = BackButton(self.to_menu) 
        self.back_button.rect.top = 850 - self.offset      

    def selected_level(self, level):
        game = Game()
        game.level_manager.level_index = int(level)
        game.level_manager.next_level()
        self.manager.next_state = game

    def to_menu(self):
        self.manager.next_state = Menu()

    def draw(self):
        self.surface.fill((0, 0, 0))
        
        if PLATFORM == 'emscripten':
            self.draw_unsupported()

        for button in self.level_buttons:
            button.draw(self.surface)
        self.back_button.draw(self.surface)
        self.draw_title()
        self.draw_hint()

    def draw_title(self):
        font  = AssetManager.fonts['font_72']
        render = font.render('Level Selection', True, 'white')
        rect = render.get_rect()
        rect.centerx = SCREEN_W / 2
        rect.top = 50 - self.offset

        self.surface.blit(render, rect.topleft)

    def draw_hint(self):
        font  = AssetManager.fonts['font_24']
        render = font.render('Use mouse scroll', True, 'grey')
        rect = render.get_rect()
        rect.centerx = SCREEN_W / 2
        rect.top = 175 - self.offset

        self.surface.blit(render, rect.topleft)

    def draw_unsupported(self):
        font  = AssetManager.fonts['font_36']
        render = font.render('level selection for web version \n will be post jam version;)', True, 'white')
        rect = render.get_rect()
        rect.centerx = SCREEN_W / 2
        rect.top = 200 - self.offset

        self.surface.blit(render, rect.topleft)

    def update(self, delta):
        friction = self.scroll_vel * -0.05
        self.scroll_acc += friction

        if self.offset < self.bounds[0]:
            self.scroll_acc += (abs(self.offset) - abs(self.bounds[0])) * 0.02

        if self.offset > self.bounds[1]:
            self.scroll_acc -= (abs(self.offset) - abs(self.bounds[1])) * 0.02

        self.scroll_vel += self.scroll_acc * delta * SPEED_FACTOR
        self.offset += self.scroll_vel * delta * SPEED_FACTOR

        self.scroll_acc = 0 

        for button in self.level_buttons:
            button.update_offset(self.offset)
            button.update()
        
        self.back_button.rect.top = 850 - self.offset
        self.back_button.update()

    def handle_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.manager.next_state = Menu()

        if event.type == MOUSEWHEEL:
            self.scroll_acc -= event.y * 8

        for button in self.level_buttons:
            button.handle_event(event)
        self.back_button.handle_event(event)

    def on_start(self):
        if PLATFORM == 'emscripten':
            return
        
        my_file = Path(SAVE_PATH)
        if not my_file.is_file():
            return
        
        with open(SAVE_PATH, 'r') as file:
            data = json.load(file)

        for i in range(len(self.level_buttons)):
            self.level_buttons[i].finished = data[i]

        print('yea')

        self.progress = data
    
    def on_exit(self):
        print('exit')


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
        