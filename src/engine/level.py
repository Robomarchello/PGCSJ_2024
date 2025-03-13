import os
import json
from pathlib import Path
import pygame
from collections import defaultdict

from src.engine.objects import *
from src.engine.asset_manager import AssetManager
from src.engine.utils import Debug, collide_circles, draw_dashed_line
from src.engine.camera import Camera
from src.engine.constants import *


class Level:
    obj_classes = {
        'BlackHole': BlackHole,
        'OrbitingBlackHole': OrbitingBlackHole,
        'ForceZone': ForceZone,
        'Asteroid': Asteroid,
        'Collectible': Collectible,
        'LaunchPoint': LaunchPoint
    }

    def __init__(self, player, controller, object_handler, level_manager=None):
        self.player = player
        self.controller = controller
        self.object_handler = object_handler

        self.level_manager = level_manager

        self.path = None
        self.collided = False
        self.in_bounds = False

        # for level creation
        # self.player_position = (100, 500)
        # self.player.position.update(self.player_position)

        self.max_speed = None
        if self.max_speed is not None:
            self.controller.max_speed = self.max_speed

        self.level_bounds = pygame.Rect(-10, -10, 1044, 788)
        self.lock_camera = True

        self.objects = []
        self.obstacles = []
        self.launch_points = []
        self.collectibles = []

        self.objects.append(
           BlackHole((350 + 300, 380 + 50), 75)
        )

        self.finish_point = FinishPoint((820, SCREENSIZE[1] // 2 - 150), 35, self.player)

        # level creation
        #self.save_level('src/levels/level14.json', False)
        #self.load_level('src/levels/level13.json')

        Camera.focus = pygame.Vector2(SCREEN_AREA.center) #  self.player.position
        Camera.offset = pygame.Vector2(SCREEN_AREA.center)
        
        # if self.lock_camera:
        #     Camera.origin_lock()

        self.text_timer = 1
        self.text_timer_crnt = self.text_timer

        self.text_visible = False

    def update(self, delta):   
        if self.object_handler.death_collision(self.player):
            self.player.velocity *= 0
            self.player.acceleration *= 0

            self.player.explode()

            if not self.collided:
                self.collided = True

        for collectible in self.collectibles:
            if collide_circles(self.player.position, self.player.radius,
                               collectible.position, collectible.radius):
                collectible.picked_up = True
        
        for launch_point in self.launch_points:
            launch_point.update(delta)

        self.finish_point.update(delta)

        if self.finish_point.completed and not self.finish_point.reacted:
            self.next_level()

            self.finish_point.reacted = True

        self.time_restart_text(delta)

    def draw(self, surface):
        cam_level_bounds = Camera.displace_rect(self.level_bounds)
        self.draw_bounds(surface, cam_level_bounds)
        for collectible in self.collectibles:
            collectible.draw(surface)

        for launch_point in self.launch_points:
            launch_point.draw(surface)

        self.finish_point.draw(surface)

        self.restart_text(surface)

    def draw_bounds(self, surface, rect):
        draw_dashed_line(
            surface, rect.topleft, rect.topright, 10, 3, 'white', 3
        )
        draw_dashed_line(
            surface, rect.topright, rect.bottomright, 10, 3, 'white', 3
        )
        draw_dashed_line(
            surface, rect.bottomright, rect.bottomleft, 10, 3, 'white', 3
        )
        draw_dashed_line(
            surface, rect.bottomleft, rect.topleft, 10, 3, 'white', 3
        )

    def restart_text(self, surface):
        font = AssetManager.fonts['font_24']
        text = 'Press R To Restart'

        render = font.render(text, False, 'white')
        render_rect = render.get_rect()
        render_rect.centerx = SCREEN_W // 2
        render_rect.top = SCREEN_H - 150

        if self.collided or not self.in_bounds:
            surface.blit(render, render_rect.topleft)

    def time_restart_text(self, delta):
        self.text_timer_crnt -= delta
        if self.text_timer_crnt < 0.0:
            self.text_visible = not self.text_visible
            self.text_timer_crnt = self.text_timer

    def next_level(self):
        transition = self.level_manager.transition
        transition.function = self.level_manager.next_level
        transition.start(1.5)

    def restart(self):
        # like why should I reset everything 
        # if I can just load the whole level
        self.load_level(self.path)

        self.player.reset()

        self.collided = False
        Camera.focus.update(SCREEN_W // 2, SCREEN_H // 2)

    def save_level(self, path, save=False):
        level_dict = {}

        # save objects
        level_dict['objects'] = defaultdict(list)
        for obj in self.objects:
            data = obj.serialize()
            group = data['type'] + 's'

            level_dict['objects'][group].append(data)

        # save obstacles
        level_dict['obstacles'] = defaultdict(list)
        for obstacle in self.obstacles:
            data = obstacle.serialize()
            group = data['type'] + 's'

            level_dict['obstacles'][group].append(data)

        # save collectibles
        level_dict['collectibles'] = defaultdict(list)
        for collectible in self.collectibles:
            data = collectible.serialize()
            group = data['type'] + 's'

            level_dict['collectibles'][group].append(data)

        # save launch points
        level_dict['launch_points'] = defaultdict(list)
        for launch_point in self.launch_points:
            data = launch_point.serialize()
            group = data['type'] + 's'

            level_dict['launch_points'][group].append(data)

        # save finish point
        level_dict['finish_point'] = self.finish_point.serialize()

        level_dict['level_bounds'] = tuple(self.level_bounds)

        level_dict['player_position'] = self.player_position
        if self.max_speed is not None:
            level_dict['controller_max_speed'] = self.max_speed
        else:
            level_dict['controller_max_speed'] = None

        if save:
            with open(path, 'w') as file:
                json.dump(level_dict, file)

    def load_level(self, path):
        self.path = path

        with open(path, 'r') as file:
            level_dict = json.load(file)

        # read objects
        self.objects = []
        obj_dict = level_dict['objects']
        for group in obj_dict.values():
            for data in group:
                self.objects.append(
                    self.obj_classes[data['type']].deserialize(data)
                )

        # read obstacles
        self.obstacles = []
        obs_dict = level_dict['obstacles']
        for group in obs_dict.values():
            for data in group:
                self.obstacles.append(
                    self.obj_classes[data['type']].deserialize(data)
                )
    
        # read collectibles
        self.collectibles = []
        collectibles_dict = level_dict['collectibles']
        for group in collectibles_dict:
            for data in group:
                self.collectibles.append(
                    self.obj_classes[data['type']].deserialize(data)
                )

        # read launch points
        self.launch_points = []
        lp_dict = level_dict['launch_points']
        for group in lp_dict.values():
            for data in group:
                self.launch_points.append(
                    self.obj_classes[data['type']].deserialize(data, self.player, self.controller)
                )

        # read finish point
        self.finish_point = FinishPoint.deserialize(level_dict['finish_point'], self.player)

        self.player_position = level_dict['player_position']
        self.player.position.update(self.player_position)

        if level_dict.get('controller_max_speed'):
            self.player.controller = level_dict['controller_max_speed']

        self.level_bounds = pygame.Rect(level_dict['level_bounds'])

        self.object_handler.objects = self.objects
        self.object_handler.obstacles = self.obstacles

    @classmethod
    def level_from_file(cls, player, controller, object_handler, path, level_manager=None):
        new_level = Level(player, controller, object_handler, level_manager)
        new_level.load_level(path)

        return new_level


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

        self.level_index = 0

        self.crnt_level = None

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
        # making sure it's sorted same in all systems
        files.sort()

        for name in files:
            if name.endswith('.json'):
                levels.append(folder_path + name)
        
        return levels

    def next_level(self):
        if self.level_index >= len(self.levels):
            return
        
        if self.crnt_level is not None:
            self.crnt_level.finish_point.completed = False
            self.crnt_level.level_manager = None

        self.crnt_level = Level.level_from_file(
            self.player, self.controller, 
            self.object_handler, self.levels[self.level_index], self
            )
        
        self.crnt_level.player.clear_emitters()
        
        self.progress[self.level_index] = True
        self.level_index += 1

        #asteroid = Asteroid((512, 200), (2.5, 0), 1, 20)
        #self.crnt_level.obstacles.append(asteroid)

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
