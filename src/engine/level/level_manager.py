import pygame
import os

from src.engine.enums import FinishPointState

from .level_base import LevelLoader
from src.engine.save_manager import SaveManager
from src.engine.utils import Debug
from src.engine.camera import Camera
from src.engine.config import SCREEN_AREA, LEVELS_PATH
from src.engine.gui.restart_bar import RestartBar


class LevelManager:
    def __init__(self, player, controller, physics_handler, transition, restart_func):
        self.levels = self.get_levels(LEVELS_PATH)

        self.player = player
        self.controller = controller
        self.physics_handler = physics_handler

        self.transition = transition
        self.transition.function = self.next_level

        self.level_index = 0
        self.crnt_level = None

        self.collided = False
        self.in_bounds = False

        self.restart_bar = RestartBar(self.controller, self, restart_func)

        # think about this
        Camera.focus = pygame.Vector2(SCREEN_AREA.center)
        Camera.offset = pygame.Vector2(SCREEN_AREA.center)

    def draw(self, surface):
        self.crnt_level.draw(surface)
        self.restart_bar.draw(surface)

    def update(self, delta):
        self.crnt_level.update(delta)

        self._update_game(delta)
        self._update_camera()
        Debug.add_text(f'Level: {self.level_index}')

    def _update_game(self, delta):
        self.in_bounds = self.crnt_level.level_bounds.collidepoint(
            self.player.position
        )
        self.restart_bar.revealed = self.collided or not self.in_bounds
        self.restart_bar.update(delta)

    def _update_camera(self):
        if self.crnt_level.finish_point.state in {FinishPointState.TOUCHING, FinishPointState.REACTED}:
            Camera.set_target_scale(1.25)
        Camera.focus.update(self.get_focus())

    def get_focus(self):
        # case for small levels
        if self.in_bounds:
            focus = self.crnt_level.level_bounds.center
            if (self.crnt_level.finish_point.state in {FinishPointState.TOUCHING, FinishPointState.REACTED}
                or self.collided):
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
        self.collided = False

        Camera.set_scale(Camera.camera_zoom.scale_modes[-1])

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
        self.level_index += 1
        if self.level_index < len(SaveManager.data['levels_completed']):
            SaveManager.data['levels_completed'][self.level_index] = True
            SaveManager.save_data() 

        self.start_level()

    def transition_next_level(self):
        transition = self.transition
        transition.function = self.next_level
        transition.start(1.5)

    def handle_event(self, event):
        self.restart_bar.handle_event(event)