import pygame
from pygame.locals import *

from src.engine.save_manager import SaveManager
from src.engine.utils import get_shake
from src.engine import State, AssetManager
from src.engine.config import *
from src.engine.gui import *
import src.states as states


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
            antialias=False,
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
            antialias=False,
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
        
        game = states.Game()
        game.level_manager.level_index = int(level)
        game.level_manager.start_level()
        self.manager.next_state = game

    def to_menu(self):
        self.manager.next_state = states.Menu()

    def draw(self):
        self.surface.fill((0, 0, 0))
        
        self.interface.draw(self.surface)
        
    def update(self, delta):
        self._scroll_logic(delta)
        self._calculate_shake(delta)

        self.interface.set_offset(self.x_shake, -self.offset)
        self.interface.update(delta)

    def _scroll_logic(self, delta):
        friction = self.scroll_vel * -0.05
        self.scroll_acc += friction

        if self.offset < self.bounds[0]:
            self.scroll_acc += (abs(self.offset) - abs(self.bounds[0])) * 0.03

        elif self.offset > self.bounds[1]:
            self.scroll_acc -= (abs(self.offset) - abs(self.bounds[1])) * 0.03

        self.scroll_vel += self.scroll_acc * delta * SPEED_FACTOR
        self.offset += self.scroll_vel
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
                self.manager.next_state = states.Menu()

        if event.type == MOUSEWHEEL:
            self.scroll_acc -= event.y * 3

        self.interface.handle_event(event)

    def on_start(self):
        for i in range(len(self.level_buttons)):
            self.level_buttons[i].completed = SaveManager.data['levels_completed'][i]

    def on_exit(self):
        pass