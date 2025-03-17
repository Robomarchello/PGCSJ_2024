import os
import json
from pathlib import Path

from .level_base import LevelLoader
from src.engine.utils import Debug
from src.engine.camera import Camera
from src.engine.constants import *


class LevelManager:
    def __init__(self, levels_folder, player, controller, object_handler, transition):
        self.levels = self.get_levels(levels_folder)

        self.progress = [False] * len(self.levels)
        self.progress[0] = True

        self.levels_folder = levels_folder
        self.player = player
        self.controller = controller
        self.object_handler = object_handler

        self.transition = transition
        self.transition.function = self.next_level

        self.level_index = -1

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

    def next_level(self):
        self.level_index += 1

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
        
        self.player.clear_emitters()
        
        self.progress[self.level_index] = True

        #asteroid = Asteroid((512, 200), (2.5, 0), 1, 20)
        #self.crnt_level.obstacles.append(asteroid)

    def transition_next_level(self):
        transition = self.transition
        transition.function = self.next_level
        transition.start(1.5)

    def restart_level(self):
        self.crnt_level = LevelLoader.load_level(
            path=self.levels[self.level_index],
            player=self.player,
            controller=self.controller,
            object_handler=self.object_handler,
            level_manager=self)

        self.player.reset()

        self.collided = False
        Camera.focus.update(SCREEN_W // 2, SCREEN_H // 2)

    def get_progress(self, file_path):
        my_file = Path(file_path)
        if not my_file.is_file():
            self.progress_init()
        
        with open(file_path, 'r') as file:
            data = json.load(file)

        self.progress = data

    def progress_init(self, file_path):
        my_file = Path(file_path)
        if my_file.is_file():
            self.get_progress(SAVE_PATH)
        else:
            self.progress = [False] * len(self.levels)
            self.progress[0] = True

        self.save_progress(file_path)

    def save_progress(self, file_path):
        with open(file_path, 'w') as file:
            json.dump(self.progress, file)
