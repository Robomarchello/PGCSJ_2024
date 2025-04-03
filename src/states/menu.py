import pygame
from pygame.locals import *

from src.engine.save_manager import SaveManager
from src.states.game import Game
from src.engine.utils import get_shake, clamp
from src.engine import State, AssetManager
from src.engine.constants import *
import src.engine.constants as c
from src.engine.gui import *
from src.engine.gui.interface import GUInterface
import src.states as states

__all__ = ['Menu']


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
        self.manager.next_state = Settings()

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


class LevelSelection(State):
    def __init__(self):
        super().__init__()
        self.surface = pygame.Surface(SCREENSIZE)

        self.x_shake = 0
        self.shake_timer = 0.0

        self.no_sound = AssetManager.sounds['no']

        self.offset = 0
        self.scroll_vel = 0
        self.scroll_acc = 0

        self.interface = GUInterface()

        self.bounds = [-100, 550]

        # level buttons
        self.level_buttons = []

        levels_num = SaveManager._get_level_count()
        x_num = 5  # count of buttons horizontally
        x_offset = 200
        y_offset = 140
        crnt_pos = pygame.Vector2(50, 100)
        for lvl_num in range(levels_num):
            if lvl_num % x_num == 0:
                crnt_pos[0] = 50
                crnt_pos[1] += y_offset            
            
            button = LevelButton(str(lvl_num), crnt_pos.copy(), self.selected_level)
            self.level_buttons.append(button)
            self.interface.add_button(button)

            crnt_pos[0] += x_offset 

        # Back button
        self.back_button = BackButton(self.to_menu) 
        self.back_button._rect.top = crnt_pos[1] + y_offset
        self.interface.add_button(self.back_button)

        # Title
        self.interface.add_label(
            font=AssetManager.fonts['font_72'],
            text='Level Selection',
            color=pygame.Color('white'),
            antialias=True,
            anchors={
                'centerx': SCREEN_W / 2,
                'top': 50
            }
        )

        # Subtitle
        self.interface.add_label(
            font=AssetManager.fonts['font_24'],
            text='Use mouse scroll',
            color=pygame.Color('grey'),
            antialias=True,
            anchors={
                'centerx': SCREEN_W / 2,
                'top': 175
            }
        )

    def selected_level(self, level, locked=False):
        '''
        Function for level buttons. 
        If the level is locked, do nothing else start the level
        '''
        if locked:
            self.no_sound.play()
            self.shake_timer = 0.2
        
            return
        
        game = Game()
        game.level_manager.level_index = int(level)
        game.level_manager.start_level()
        self.manager.next_state = game

    def to_menu(self):
        self.manager.next_state = Menu()

    def draw(self):
        self.surface.fill((0, 0, 0))
        
        self.interface.draw(self.surface)
        
    def update(self, delta):
        self._scroll_logic(delta)
        self._calculate_shake(delta)

        self.interface.set_offset_all(self.x_shake, -self.offset)
        self.interface.update(delta)

    def _scroll_logic(self, delta):
        friction = self.scroll_vel * -0.05
        self.scroll_acc += friction

        if self.offset < self.bounds[0]:
            self.scroll_acc += (abs(self.offset) - abs(self.bounds[0])) * 0.03

        elif self.offset > self.bounds[1]:
            self.scroll_acc -= (abs(self.offset) - abs(self.bounds[1])) * 0.03

        self.scroll_vel += self.scroll_acc * delta * SPEED_FACTOR
        self.offset += self.scroll_vel * delta * SPEED_FACTOR

        self.scroll_acc = 0 

    def _calculate_shake(self, delta):
        if self.shake_timer > 0:
            self.shake_timer -= delta

            self.x_shake = get_shake(5)[0]
        else:
            self.x_shake = 0

    def handle_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.manager.next_state = Menu()

        if event.type == MOUSEWHEEL:
            self.scroll_acc -= event.y * 8

        self.interface.handle_event(event)

    def on_start(self):
        for i in range(len(self.level_buttons)):
            self.level_buttons[i].completed = SaveManager.data['levels_completed'][i]

    def on_exit(self):
        pass


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
            antialias=True,
            anchors={
                'centerx': SCREEN_W / 2,
                'top': 50
            }
        )

        self.volume_label = self.interface.add_label(
            font=AssetManager.fonts['font_36'],
            text=f'Volume: {round(c.VOLUME, 3)}',
            color=pygame.Color('white'),
            antialias=True,
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
        self.manager.next_state = Menu()

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