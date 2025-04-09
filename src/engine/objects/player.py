import random
import math

import pygame
from pygame import Vector2
from pygame.locals import MOUSEBUTTONDOWN, MOUSEBUTTONUP

from src.engine.constants import SPEED_FACTOR, DEBUG_VEL, PLATFORM
from src.engine.base import Base
from src.engine.camera import Camera
from src.engine.utils import Debug, clamp
from src.engine.asset_manager import AssetManager
from src.engine.vfx.emitters import Emitter
from src.engine.vfx.game_particles import JetEmitter, ExplodeEmitter
from src.engine.objects import Object, LaunchPoint
from src.engine.physics_handler import PhysicsHandler


class Player(Object):
    radius = 32

    def __init__(self):
        super().__init__(position=Vector2(), velocity=0, mass=1)

        self.look_angle = 0
        self.look_vec = pygame.Vector2()

        self.freeze = True
        self.exploded = False
        self.flying_last = False

        # assets
        self.image = AssetManager.images['player'].convert_alpha()
        self.jet_sound = AssetManager.sounds['jet']
        self.jet_channel = pygame.mixer.Channel(0)
        self.explosion_sounds = [
            AssetManager.sounds['explosion_1'],
            AssetManager.sounds['explosion_2'],
        ]

        # particles
        emitter_rect = pygame.Rect(0, 0, 32, 32)
        self.explode_emitter = ExplodeEmitter(emitter_rect)
        self.jet_emitter = JetEmitter(pygame.Rect(0, 0, 10, 10))
        self.jet_location = pygame.Vector2()

    def draw(self, surface):
        self.jet_emitter.draw(surface)
        self.explode_emitter.draw(surface)

        rotated_img = pygame.transform.rotate(self.image, self.look_angle)
        rotated_rect = rotated_img.get_rect(center=self.cam_pos)

        if not self.exploded:
            surface.blit(rotated_img, rotated_rect.topleft)
        
        # debug below
        # pygame.draw.circle(surface, 'red', self.cam_pos, self.radius, 2)

    def update(self, delta):
        Debug.add_text(f'player_pos: {self.position}')
        if self.freeze:
            self.velocity *= 0
            self.force *= 0
        
        self.motion_logic(delta)
        self.set_look_angle(self.velocity)
        self._update_emitters(delta)
        self._handle_jet_sound()

    def set_look_angle(self, vector): 
        self.look_angle = math.degrees(math.atan2(-vector.y, vector.x))
        if vector != (0, 0):
            self.look_vec = vector.normalize()
    
    def _update_emitters(self, delta):
        self.jet_location = self.position - self.look_vec * 30
        self.explode_emitter.update(delta)
        self.jet_emitter.update(delta, self.look_angle, self.jet_location, self.velocity.length())

    def _handle_jet_sound(self):
        if self.velocity.length() > 1:
            self.jet_emitter.flying = True
        else:
            self.jet_emitter.flying = False
            self.jet_channel.fadeout(100) # could cause the bug

        if not self.flying_last and self.jet_emitter.flying:
            self.jet_channel.play(self.jet_sound, -1)

        self.flying_last = self.jet_emitter.flying

    def explode(self):
        if not self.exploded and not self.freeze:
            self.exploded = True

            Camera.shake(0.3, 5)

            random_sound = random.choice(self.explosion_sounds)
            random_sound.play()

            self.explode_emitter.emit_rect.center = self.position
            self.explode_emitter.burst(300)

    def reset(self):
        self.freeze = True
        self.exploded = False
        self.velocity *= 0
        self.acceleration *= 0
        self._clear_emitters()

    def _clear_emitters(self):
        self.jet_emitter.clear()
        self.explode_emitter.clear()


class Controller(Base):
    def __init__(self, player: Player, rect: pygame.Rect, physics_handler: PhysicsHandler):
        self.player = player
        self.rect = rect
        self.radius = rect.width / 2

        self.physics_handler = physics_handler

        self.preview_balls = 51 # 300

        self.holding = False

        self.launch_point: LaunchPoint = None
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
        
        pygame.draw.circle(surface, (245, 232, 199), self.cam_rect.center, self.radius, 3)
        
        self.draw_trajectory(surface)

    def update(self, delta):
        self.mouse_pos = pygame.mouse.get_pos()

        self._handle_mouse_input()
        self.rect.center = self.player.position

        if self.debug_movement and Debug.enabled:
            self._debug_movement(delta)

    def draw_trajectory(self, surface):
        if not self.player.freeze or self.holding:
            points = self._get_trajectory()
            for position in points:
                cam_pos = Camera.displace_position(position)
                pygame.draw.circle(surface, 'white', cam_pos, 3)

        if self.holding:
            pygame.draw.circle(surface, 'grey', self.mouse_pos, 10)

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

    # --- Private Methods ---

    def _get_trajectory(self):
        if self.holding:
            start_vel = self.launch_force
        else:
            start_vel = self.player.velocity
        
        return self.physics_handler.predict_player(
            time=0.016, 
            position=self.player.position, 
            start_vel=start_vel,
            mass=self.player.mass,
            radius=self.player.radius, 
            count=self.preview_balls
        )[::3]

    def _debug_movement(self, delta):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.player.position.x -= DEBUG_VEL * delta * SPEED_FACTOR
        if keys[pygame.K_d]:
            self.player.position.x += DEBUG_VEL * delta * SPEED_FACTOR
        if keys[pygame.K_w]:
            self.player.position.y -= DEBUG_VEL * delta * SPEED_FACTOR 
        if keys[pygame.K_s]:
            self.player.position.y += DEBUG_VEL * delta * SPEED_FACTOR

    def _handle_mouse_input(self):
        """Calculate launch force and player look angle when holding."""
        if self.holding:
            difference = self.player.cam_pos - self.mouse_pos
            if difference == pygame.Vector2():
                return
            
            if PLATFORM == 'emscripten':
                # once camera scaling is done, this can be ✨removed✨
                magnitude = difference.magnitude() * 0.05
            else:
                magnitude = difference.magnitude() * 0.02

            magnitude = clamp(magnitude, self.min_speed, self.max_speed)
            norm_diff = difference.normalize()

            self.launch_force = norm_diff * magnitude
            self.player.set_look_angle(norm_diff)