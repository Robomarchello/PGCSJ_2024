import pygame

import json
from collections import defaultdict

from src.engine.objects import *
from src.engine.asset_manager import AssetManager
from src.engine.utils import collide_circles, draw_dashed_rect
from src.engine.camera import Camera
from src.engine.config import *
from src.engine.enums import FinishPointState


class LevelLoader:
    obj_classes = {
        'BlackHole': BlackHole,
        'OrbitingBlackHole': OrbitingBlackHole,
        'ForceZone': ForceZone,
        'Asteroid': Asteroid,
        'Collectible': Collectible,
        'LaunchPoint': LaunchPoint
    }

    @classmethod
    def save_level(cls, level: 'Level', path, save=True):
        level_dict = {}

        # objects
        level_dict['objects'] = defaultdict(list)
        for obj in level.objects:
            data = obj.serialize()
            group = data['type'] + 's'

            level_dict['objects'][group].append(data)

        # obstacles
        level_dict['obstacles'] = defaultdict(list)
        for obstacle in level.obstacles:
            data = obstacle.serialize()
            group = data['type'] + 's'

            level_dict['obstacles'][group].append(data)

        # collectibles
        level_dict['collectibles'] = defaultdict(list)
        for collectible in level.collectibles:
            data = collectible.serialize()
            group = data['type'] + 's'

            level_dict['collectibles'][group].append(data)

        # launch points
        level_dict['launch_points'] = defaultdict(list)
        for launch_point in level.launch_points:
            data = launch_point.serialize()
            group = data['type'] + 's'

            level_dict['launch_points'][group].append(data)

        # finish point
        level_dict['finish_point'] = level.finish_point.serialize()

        level_dict['level_bounds'] = tuple(level.level_bounds)

        level_dict['player_position'] = level.player_position

        # if level.max_speed is not None:
        #     level_dict['controller_max_speed'] = level.max_speed
        # else:
        #     level_dict['controller_max_speed'] = None
        level_dict['controller_max_speed'] = level.max_speed

        if save:
            with open(path, 'w') as file:
                json.dump(level_dict, file)

    @classmethod
    def load_level(cls, path, player, controller, physics_handler, level_manager):
        level = Level(player, controller, physics_handler, level_manager)

        with open(path, 'r') as file:
            level_dict = json.load(file)

        # read objects
        for group in level_dict['objects'].values():
            for data in group:
                level.objects.append(
                    cls.obj_classes[data['type']].deserialize(data)
                )

        # read obstacles
        for group in level_dict['obstacles'].values():
            for data in group:
                level.obstacles.append(
                    cls.obj_classes[data['type']].deserialize(data)
                )
    
        # read collectibles
        for group in level_dict['collectibles'].values():
            for data in group:
                level.collectibles.append(
                    cls.obj_classes[data['type']].deserialize(data)
                )

        # read launch points
        for group in level_dict['launch_points'].values():
            for data in group:
                level.launch_points.append(
                    cls.obj_classes[data['type']].deserialize(data, player, controller)
                )

        # read finish point
        level.finish_point = FinishPoint.deserialize(level_dict['finish_point'], player)

        player.position.update(level_dict['player_position'])
        if level_dict.get('controller_max_speed'):
            player.controller = level_dict['controller_max_speed']

        level.level_bounds = pygame.Rect(level_dict['level_bounds'])

        physics_handler.objects = level.objects
        physics_handler.obstacles = level.obstacles
        
        return level


class Level:
    def __init__(self, player, controller, physics_handler, level_manager):
        self.player = player
        self.controller = controller
        self.physics_handler = physics_handler
        self.level_manager = level_manager

        self.objects = []
        self.obstacles = []
        self.launch_points = []
        self.collectibles = []
        self.finish_point: FinishPoint = None

        self.path = None
        self.collided = False
        self.in_bounds = False

        self.max_speed = None
        if self.max_speed is not None:
            self.controller.max_speed = self.max_speed

        self.level_bounds = pygame.Rect()

        # level creation
        #self.save_level('src/levels/level14.json', False)
        #self.load_level('src/levels/level13.json')
        
        self.text_timer = 1
        self.text_timer_crnt = self.text_timer

        self.text_visible = False

    def update(self, delta):   
        if self.physics_handler.object_collision(self.player):
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

        if self.finish_point.state == FinishPointState.COMPLETED:
            self.level_manager.transition_next_level()
            
            self.finish_point._change_state(FinishPointState.REACTED)

        self.time_restart_text(delta)

    def draw(self, surface):
        cam_level_bounds = Camera.displace_rect(self.level_bounds)
        draw_dashed_rect(surface, cam_level_bounds, 10, 3, 'white', 3)
        for collectible in self.collectibles:
            collectible.draw(surface)

        for launch_point in self.launch_points:
            launch_point.draw(surface)

        self.finish_point.draw(surface)

        self.restart_text(surface)

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