import pygame
import os

from .level_base import LevelLoader
from src.engine.save_manager import SaveManager
from src.engine.utils import Debug
from src.engine.camera import Camera
from src.engine.constants import SCREEN_AREA, LEVELS_PATH


class LevelManager:
    def __init__(self, player, controller, physics_handler, transition):
        self.levels = self.get_levels(LEVELS_PATH)

        self.player = player
        self.controller = controller
        self.physics_handler = physics_handler

        self.transition = transition
        self.transition.function = self.next_level

        self.level_index = 0
        self.crnt_level = None

        # think about this
        Camera.focus = pygame.Vector2(SCREEN_AREA.center)
        Camera.offset = pygame.Vector2(SCREEN_AREA.center)

    def draw(self, surface):
        self.crnt_level.draw(surface)

    def update(self, delta):
        self.crnt_level.in_bounds = self.crnt_level.level_bounds.collidepoint(
            self.player.position
        )

        self.crnt_level.update(delta)
        
        Camera.focus.update(self.get_focus())
        Debug.add_text(f'Level: {self.level_index}')

    def get_focus(self):
        # case for small levels
        if self.crnt_level.in_bounds:
            focus = SCREEN_AREA.center

            if self.crnt_level.collided:
                focus = self.player.position
        else:
            focus = self.player.position

        # case for big levels
        ...

        return focus

    def get_levels(self, folder_path):
        levels = []
        files = os.listdir(folder_path)
        files.sort()

        for name in files:
            if name.endswith('.json'):
                levels.append(folder_path + name)
        
        return levels
    
    def start_level(self):
        if self.level_index >= len(self.levels):
            return
        
        if self.crnt_level is not None:
            self.crnt_level.finish_point.completed = False
            self.crnt_level.level_manager = None

        self.crnt_level = LevelLoader.load_level(
            self.levels[self.level_index],
            self.player, self.controller, 
            self.physics_handler, self
            )
        
        self.player.reset()

    def next_level(self):
        SaveManager.data['levels_completed'][self.level_index] = True

        self.level_index += 1        
        self.start_level()

    def transition_next_level(self):
        transition = self.transition
        transition.function = self.next_level
        transition.start(1.5)
