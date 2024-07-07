import json
import pygame
from src.engine.objects import *
from src.engine.asset_manager import AssetManager
from src.engine.utils import collide_circles
from src.engine.camera import Camera
from src.engine.constants import SCREENSIZE


class Level:
    def __init__(self, player, controller, object_handler):
        self.player = player
        self.controller = controller
        self.object_handler = object_handler

        self.player.position.x = 200

        self.level_bounds = pygame.Rect(-10, -10, 1044, 788)
        self.lock_camera = True

        self.objects = []
        self.obstacles = []
        self.launch_points = []
        self.collectibles = []

        center = (
            SCREENSIZE[0] // 2,
            SCREENSIZE[1] // 2
        )
        another_hole = OrbitingBlackHole(
            center, (center[0] + 100, center[1]), 35, 2
        )
        self.objects.append(another_hole)
        another_hole = BlackHole(
            center, 10
        )
        self.objects.append(another_hole)

        self.finish_point = FinishPoint((824, SCREENSIZE[1] // 2), 30, self.player)

        self.save_level('level_saved.json')
        #self.load_level('level_saved.json')

        self.object_handler.objects = self.objects
        self.object_handler.obstacles = self.obstacles
        
        Camera.focus = self.player.position
        Camera.secondary_focus = self.finish_point.position

        if self.lock_camera:
            Camera.origin_lock()

    def update(self, delta):        
        for collectible in self.collectibles:
            if collide_circles(self.player.position, self.player.radius,
                               collectible.position, collectible.radius):
                if not collectible.picked_up:
                    collectible.picked_up = True
        
        for launch_point in self.launch_points:
            launch_point.update(delta)

        self.finish_point.update(delta)

    def draw(self, surface):
        cam_level_bounds = Camera.displace_rect(self.level_bounds)
        pygame.draw.rect(surface, (255, 0, 0), cam_level_bounds, 3)
        for collectible in self.collectibles:
            collectible.draw(surface)

        for launch_point in self.launch_points:
            launch_point.draw(surface)

        self.finish_point.draw(surface)

        if self.finish_point.completed:
            Camera.focus = self.player.position

            # print('*transition to next level*')
            
    def save_level(self, path):
        level_dict = {}

        # save objects
        level_dict['objects'] = {}
        obj_dict = level_dict['objects']
        obj_id = 0
        for obj in self.objects:
            if isinstance(obj, BlackHole):
                key = f'black_hole_{obj_id}'
                obj_dict[key] = {}
                obj_dict[key]['position'] = tuple(obj.position)
                obj_dict[key]['mass'] = obj.mass

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

        return 
        with open(path, 'w') as file:
            print(json.dumps(level_dict, file))

    def load_level(self, path):
        self.objects = []
        with open(path, 'r') as file:
            level_dict = json.load(file)

        # read objects
        obj_dict = level_dict['objects']
        for obj_key in obj_dict:
            if obj_key.startswith('black_hole'):
                read_object = BlackHole(
                    obj_dict[obj_key]['position'],
                    obj_dict[obj_key]['mass']
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

        if level_dict['level_bounds'] is not None:
            self.level_bounds = pygame.Rect(level_dict['level_bounds'])
        else:
            self.level_bounds = None


class LevelManager:
    def __init__(self, levels_folder, player, controller, object_handler):
        self.levels = []

        self.levels_folder = levels_folder
        self.player = player
        self.controller = controller
        self.object_handler = object_handler

        self.crnt_level = None

    def next_level(self):
        self.crnt_level = Level()
        self.levels.pop()