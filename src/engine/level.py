import os
import json
import pygame
from src.engine.objects import *
from src.engine.asset_manager import AssetManager
from src.engine.utils import collide_circles
from src.engine.camera import Camera
from src.engine.constants import SCREENSIZE, SCREEN_W, SCREEN_H
from src.states.transition import TransitionState


class Level:
    def __init__(self, player, controller, object_handler, level_manager=None):
        self.player = player
        self.controller = controller
        self.object_handler = object_handler

        self.level_manager = level_manager

        self.path = None
        self.collided = False

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

        self.finish_point = FinishPoint((820, SCREENSIZE[1] // 2 - 150), 25, self.player)

        #self.save_level('src/levels/level14.json', False)
        #self.load_level('src/levels/level13.json')

        self.object_handler.objects = self.objects
        self.object_handler.obstacles = self.obstacles
        
        Camera.focus = pygame.Vector2(512, 384) #  self.player.position
        Camera.offset = pygame.Vector2(512, 384)
        
        # if self.lock_camera:
        #     Camera.origin_lock()

        self.text_timer = 1
        self.text_timer_crnt = self.text_timer

        self.text_visible = False


    def update(self, delta):      
        if self.object_handler.black_holes_collision():
            self.player.velocity *= 0
            self.player.acceleration *= 0

            if not self.collided:
                self.collided = True
                
                Camera.focus = self.player.position
            # Camera.secondary_focus = pygame.Vector2(self.finish_point.position)

        for collectible in self.collectibles:
            if collide_circles(self.player.position, self.player.radius,
                               collectible.position, collectible.radius):
                if not collectible.picked_up:
                    collectible.picked_up = True
        
        for launch_point in self.launch_points:
            launch_point.update(delta)

        self.finish_point.update(delta)

        self.time_restart_text(delta)

    def draw(self, surface):
        cam_level_bounds = Camera.displace_rect(self.level_bounds)
        pygame.draw.rect(surface, (255, 0, 0), cam_level_bounds, 3)
        for collectible in self.collectibles:
            collectible.draw(surface)

        for launch_point in self.launch_points:
            launch_point.draw(surface)

        self.finish_point.draw(surface)
        
        if self.finish_point.completed and not self.finish_point.reacted:
            if self.level_manager is not None:
                self.next_level()

            self.finish_point.reacted = True

        self.restart_text(surface)

    def restart_text(self, surface):
        font = AssetManager.fonts['font_24']
        text = 'Press R To Restart'

        render = font.render(text, False, 'white')
        render_rect = render.get_rect()
        render_rect.centerx = SCREEN_W // 2
        render_rect.top = SCREEN_H - 150

        if self.collided:
            surface.blit(render, render_rect.topleft)

    def time_restart_text(self, delta):
        self.text_timer_crnt -= delta
        if self.text_timer_crnt < 0.0:
            self.text_visible = not self.text_visible
            self.text_timer_crnt = self.text_timer

    def next_level(self):
        transition = self.level_manager.transition
        transition.function = self.level_manager.next_level
        transition.start()

    def restart(self):
        # like why should I reset everything 
        # if I can just load the whole level
        if self.path is not None:
            self.load_level(self.path)

        self.player.freeze = True
        self.player.velocity *= 0
        self.player.acceleration *= 0

        self.collided = False
        Camera.focus = pygame.Vector2(512, 384)

    def save_level(self, path, save=False):
        level_dict = {}

        # save objects
        level_dict['objects'] = {}
        obj_dict = level_dict['objects']
        obj_id = 0
        for obj in self.objects:
            if isinstance(obj, BlackHole) and not isinstance(obj, OrbitingBlackHole):
                key = f'black_hole_{obj_id}'
                obj_dict[key] = {}
                obj_dict[key]['position'] = tuple(obj.position)
                obj_dict[key]['mass'] = obj.mass

            if isinstance(obj, OrbitingBlackHole):
                key = f'orbiting_black_hole_{obj_id}'
                obj_dict[key] = {}
                obj_dict[key]['origin'] = tuple(obj.origin)
                obj_dict[key]['position'] = tuple(obj.position)
                obj_dict[key]['mass'] = obj.mass
                obj_dict[key]['rot_speed'] = obj.rot_speed

            if isinstance(obj, ForceZone):
                key = f'force_zone_{obj_id}'
                obj_dict[key] = {}
                obj_dict[key]['force'] = tuple(obj.force)
                obj_dict[key]['rect'] = obj.rect
                obj_dict[key]['timer'] = obj.timer

            if isinstance(obj, PortalPair):
                key = f'portal_pair_{obj_id}'
                obj_dict[key] = {}
                # looks kinda annoying
                obj_dict[key]['portal1']['rect'] = obj.portal_1.rect
                obj_dict[key]['portal1']['hitrect'] = obj.portal_1.hitrect
                obj_dict[key]['portal1']['normal'] = tuple(obj.portal_1.normal)
                obj_dict[key]['portal1']['color'] = obj.portal_1.color

                obj_dict[key]['portal2']['rect'] = obj.portal_2.rect
                obj_dict[key]['portal2']['hitrect'] = obj.portal_2.hitrect
                obj_dict[key]['portal2']['normal'] = tuple(obj.portal_2.normal)
                obj_dict[key]['portal2']['color'] = obj.portal_2.color

            obj_id += 1

        # save obstacles
        obs_id = 0
        level_dict['obstacles'] = {}
        obs_dict = level_dict['obstacles']
        for obstacle in self.obstacles:
            if isinstance(obstacle, Asteroid):
                key = f'asteroid_{obs_id}' 
                obs_dict[key] = {}

                obs_dict[key]['position'] = tuple(obstacle.position)
                obs_dict[key]['velocity'] = tuple(obstacle.velocity)
                obs_dict[key]['mass'] = obstacle.mass
                obs_dict[key]['radius'] = obstacle.radius
        
            obs_id += 1

        # save collectibles
        level_dict['collectibles'] = {}
        collectible_id = 0
        collectibles_dict = level_dict['collectibles']
        for collectible in self.collectibles:
            key = f'collectible_{collectible_id}'
            collectibles_dict[key] = {}
            #position, texture=None, texture_picked=None
            collectibles_dict[key]['position'] = tuple(collectible.position)
            collectibles_dict[key]['texture_key'] = collectible.texture_key
            collectibles_dict[key]['texture_key_picked'] = collectible.texture_key_picked

            collectible_id += 1

        # save launch points
        level_dict['launch_points'] = {}
        lp_id = 0
        lp_dict = level_dict['launch_points']
        for launch_point in self.launch_points:
            key = f'launch_point_{lp_id}'
            lp_dict[key] = {}

            lp_dict[key]['position'] = tuple(launch_point.position)
            lp_dict[key]['radius'] = launch_point.radius

            lp_id += 1

        # save finish point
        level_dict['finish_point'] = {}
        level_dict['finish_point']['position'] = tuple(self.finish_point.position)
        level_dict['finish_point']['radius'] = self.finish_point.radius 

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
        self.objects = []
        with open(path, 'r') as file:
            level_dict = json.load(file)

        if self.path is None:
            self.path = path

        # read objects
        obj_dict = level_dict['objects']
        for obj_key in obj_dict:
            if obj_key.startswith('black_hole'):
                read_object = BlackHole(
                    obj_dict[obj_key]['position'],
                    obj_dict[obj_key]['mass']
                )
                self.objects.append(read_object)

            if obj_key.startswith('orbiting_black_hole'):
                read_object = OrbitingBlackHole(
                    obj_dict[obj_key]['origin'],
                    obj_dict[obj_key]['position'],
                    obj_dict[obj_key]['mass'],
                    obj_dict[obj_key]['rot_speed'],
                )
                self.objects.append(read_object)
                
            if obj_key.startswith('force_zone'):
                read_object = ForceZone(
                    obj_dict[obj_key]['force'],
                    obj_dict[obj_key]['rect'],
                    obj_dict[obj_key]['timer'],
                )
                self.objects.append(read_object)

            if obj_key.startswith('portal_pair'):                
                portal_1 = Portal(
                    obj_dict[obj_key]['portal1']['rect'],
                    obj_dict[obj_key]['portal1']['hitrect'],
                    obj_dict[obj_key]['portal1']['normal'],
                    obj_dict[obj_key]['portal1']['color'],
                )
                portal_2 = Portal(
                    obj_dict[obj_key]['portal2']['rect'],
                    obj_dict[obj_key]['portal2']['hitrect'],
                    obj_dict[obj_key]['portal2']['normal'],
                    obj_dict[obj_key]['portal2']['color'],
                )
                
                read_object = PortalPair(portal_1, portal_2)

                self.objects.append(read_object)

        # read obstacles
        self.obstacles = []
        obs_dict = level_dict['obstacles']
        for obs_key in obs_dict:
            if obs_key.startswith('asteroid'):
                read_object = Asteroid(
                    obs_dict[obs_key]['position'],
                    obs_dict[obs_key]['velocity'],
                    obs_dict[obs_key]['mass'],
                    obs_dict[obs_key]['radius']
                )
                self.obstacles.append(read_object)
    
        # read collectibles
        self.collectibles = []
        collectibles_dict = level_dict['collectibles']
        for collectible_key in collectibles_dict:
            read_object = Collectible(
                collectibles_dict[collectible_key]['position'],
                collectibles_dict[collectible_key]['texture_key'],
                collectibles_dict[collectible_key]['texture_key_picked']
            )

            self.collectibles.append(read_object)

        # read launch points
        self.launch_points = []
        lp_dict = level_dict['launch_points']
        for lp_key in lp_dict:
            read_object = LaunchPoint(
                lp_dict[lp_key]['position'], 
                lp_dict[lp_key]['radius'],
                self.player,
                self.controller
            )

            self.launch_points.append(read_object)

        # read finish point
        self.finish_point = FinishPoint(
            level_dict['finish_point']['position'],
            level_dict['finish_point']['radius'],
            self.player
        )

        self.player_position = level_dict['player_position']
        self.player.position.update(self.player_position)

        if level_dict.get('controller_max_speed'):
            self.player.controller = level_dict['controller_max_speed']

        # level bounds
        if level_dict['level_bounds'] is not None:
            self.level_bounds = pygame.Rect(level_dict['level_bounds'])
        else:
            self.level_bounds = pygame.Rect(-10, -10, 1044, 788)

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

        self.levels_folder = levels_folder
        self.player = player
        self.controller = controller
        self.object_handler = object_handler

        self.transition = transition
        self.transition.function = self.next_level

        self.crnt_level = None

    def get_levels(self, folder_path):
        levels = []
        for name in os.listdir(folder_path):
            if name.endswith('.json'):
                levels.append(folder_path + name)
        
        return levels

    def next_level(self):
        if len(self.levels) <= 0:
            return
        
        if self.crnt_level is not None:
            self.crnt_level.finish_point.completed = False
            self.crnt_level.level_manager = None


        self.crnt_level = Level.level_from_file(
            self.player, self.controller, 
            self.object_handler, self.levels[0], self
            )
        self.crnt_level.load_level(self.levels[0])
        self.levels.pop(0)


