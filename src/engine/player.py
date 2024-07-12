import math
import pygame
from pygame import Vector2
from pygame.locals import MOUSEBUTTONDOWN, MOUSEBUTTONUP
from src.engine.constants import SPEED_FACTOR, DEBUG_VEL, SCREEN_H, PLATFORM
from src.engine.camera import Camera
from src.engine.utils import Debug
from src.engine.asset_manager import AssetManager
from src.engine.vfx.emitters import Emitter, JetEmitter


rect = pygame.Rect(0, 0, 32, 32)



class Player:
    radius = 32

    def __init__(self):
        self.position = Vector2(100, SCREEN_H / 2)
        self.last_position = self.position.copy()

        self.velocity = Vector2(0, 0)
        self.acceleration = Vector2(0, 0)

        self.image = AssetManager.images['player'].convert_alpha()
        self.look_angle = 0
        self.look_vec = pygame.Vector2(
            math.cos(self.look_angle), -math.sin(self.look_angle)
        )

        self.explode_emitter = Emitter(
            (0, 360), (1, 2), (4, 5), (0, 1), (245, 232, 199), (245, 232, 199), 
            AssetManager.images['particle'], 130, rect, None
        )
        self.jet_emitter = JetEmitter()

        self.mass = 1

        self.jet_location = pygame.Vector2()
        
        self.freeze = True
        self.exploded = False

    @property
    def cam_pos(self):
        return self.position - Camera.pos

    def update(self, delta):
        Debug.add_text(f'player_pos: {self.position}')
        if self.freeze:
            self.velocity *= 0
            self.acceleration *= 0  
        self.velocity += self.acceleration * delta * SPEED_FACTOR
        self.position += self.velocity * delta * SPEED_FACTOR

        self.get_look_angle(self.velocity)

        self.jet_location = self.position - self.look_vec * 30

        self.explode_emitter.update(delta)
        self.jet_emitter.update(delta, self.look_angle, self.jet_location,
                                self.velocity.length())

        if self.velocity.length() > 1:
            self.jet_emitter.flying = True
        else:
            self.jet_emitter.flying = False

        self.acceleration *= 0 

        self.last_position = self.position.copy()

    def get_look_angle(self, vector):
        self.look_angle = math.degrees(math.atan2(-vector.y, vector.x)) - 90
        if vector != (0, 0):
            self.look_vec = vector.normalize()

        Debug.add_text(vector)

    def draw(self, surface):
        self.jet_emitter.draw(surface)
        self.explode_emitter.draw(surface)

        rotated_img = pygame.transform.rotate(self.image, self.look_angle)
        rotated_rect = rotated_img.get_rect(center=self.cam_pos)

        if not self.exploded:
            surface.blit(rotated_img, rotated_rect.topleft)
        
        # debug below
        # pygame.draw.circle(surface, 'red', self.cam_pos, self.radius, 2)
    
    def explode(self):
        if not self.exploded:
            self.exploded = True

            self.explode_emitter.emit_rect.center = self.position
            self.explode_emitter.burst()


    def clear_emitters(self):
        self.jet_emitter.clear()
        self.explode_emitter.clear()


class Controller:
    def __init__(self, player, rect, object_handler):
        self.player = player
        self.rect = rect

        self.radius = rect.width / 2

        self.object_handler = object_handler
        self.prediction = []

        self.preview_balls = 51 # 300

        self.holding = False
        self.difference = pygame.Vector2(0, 0)  

        self.launch_point = None
        self.launch_force = pygame.Vector2()
        self.min_speed = 1
        self.max_speed = 7

        self.mouse_pos = pygame.mouse.get_pos()

        self.debug_movement = True

    @property
    def cam_rect(self):
        return Camera.displace_rect(self.rect)

    def draw(self, surface):
        if self.player.exploded:
            return
        
        pygame.draw.circle(surface, 'blue', self.cam_rect.center, self.radius, 3)
        #pygame.draw.rect(surface, 'blue', self.cam_rect, 2)
        
        if not self.player.freeze or self.holding:
            for position in self.prediction:
                cam_pos = Camera.displace_position(position)
                pygame.draw.circle(surface, 'white', cam_pos, 3)

        if self.holding:
            pygame.draw.circle(surface, 'grey', self.mouse_pos, 10)

    def update(self, delta):
        self.mouse_pos = pygame.mouse.get_pos()

        if self.holding and self.player.cam_pos != self.mouse_pos:
            self.difference = self.player.cam_pos - self.mouse_pos
            norm_diff = self.difference.normalize()

            magnitude = self.difference.magnitude() * 0.02  # 0.03
            if PLATFORM == 'emscripten':
                magnitude = self.difference.magnitude() * 0.05
            magnitude = max(self.min_speed, magnitude)
            magnitude = min(magnitude, self.max_speed)

            self.launch_force = norm_diff * magnitude

            self.player.get_look_angle(self.launch_force)

        if self.holding:
            start_vel = self.player.velocity + self.launch_force
        else:
            start_vel = self.player.velocity.copy()
            
        start_acc = self.player.acceleration.copy()
        self.prediction = self.object_handler.predict_player(
            0.016, self.player.position, start_vel, start_acc, self.preview_balls
            )[::3]

        self.rect.center = self.player.position

        if self.debug_movement:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                self.player.position.x -= DEBUG_VEL * delta * SPEED_FACTOR
            if keys[pygame.K_d]:
                self.player.position.x += DEBUG_VEL * delta * SPEED_FACTOR
            if keys[pygame.K_w]:
                self.player.position.y -= DEBUG_VEL * delta * SPEED_FACTOR 
            if keys[pygame.K_s]:
                self.player.position.y += DEBUG_VEL * delta * SPEED_FACTOR

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.cam_rect.collidepoint(self.mouse_pos):
                    if self.launch_point is not None:
                        self.holding = True

            if event.button == 3:
                self.holding = False
                
        if event.type == MOUSEBUTTONUP:
            if self.holding:
                self.player.velocity += self.launch_force
                self.player.freeze = False

                if self.launch_point is not None:
                    self.launch_point.used = True
                    self.launch_point = None

                self.holding = False