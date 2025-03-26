import os

from .level_base import LevelLoader
from src.engine.save_manager import SaveManager
from src.engine.utils import Debug
from src.engine.camera import Camera
from src.engine.constants import *


class LevelManager:
    def __init__(self, levels_folder, player, controller, object_handler, transition):
        self.levels = self.get_levels(levels_folder)
        self.level_count = len(self.levels)

        self.progress = [False] * self.level_count
        self.progress[0] = True

        self.levels_folder = levels_folder
        self.player = player
        self.controller = controller
        self.object_handler = object_handler

        self.transition = transition
        self.transition.function = self.next_level

        self.level_index = 0

        self.crnt_level = None

        # think about this
        Camera.focus = pygame.Vector2(SCREEN_AREA.center)
        Camera.offset = pygame.Vector2(SCREEN_AREA.center)

    def update(self, delta):
        self.crnt_level.in_bounds = self.crnt_level.level_bounds.collidepoint(
            self.player.position
        )
        
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
            self.object_handler, self
            )
        
        self.player.reset()

        #asteroid = Asteroid((512, 200), (2.5, 0), 1, 20)
        #self.crnt_level.obstacles.append(asteroid)

    def next_level(self):
        SaveManager.data['levels_completed'][self.level_index] = True

        self.level_index += 1        
        self.start_level()

    def transition_next_level(self):
        transition = self.transition
        transition.function = self.next_level
        transition.start(1.5)
