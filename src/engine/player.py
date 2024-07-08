import pygame
from pygame import Vector2
from pygame.locals import MOUSEBUTTONDOWN, MOUSEBUTTONUP
from src.engine.constants import SPEED_FACTOR, DEBUG_VEL, SCREEN_H
from src.engine.camera import Camera
from src.engine.utils import Debug


class Player:
    radius = 25

    def __init__(self):
        self.position = Vector2(100, SCREEN_H / 2)
        self.velocity = Vector2(0, 0)
        self.acceleration = Vector2(0, 0)

        self.mass = 1

        self.freeze = True

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

        ...

        self.acceleration *= 0 

    def draw(self, surface):
        #pygame.draw.circle(surface, 'red', self.position, self.radius)

        pygame.draw.circle(surface, 'red', self.cam_pos, self.radius)


class Controller:
    def __init__(self, player, rect, object_handler):
        self.player = player
        self.rect = rect

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
        pygame.draw.rect(surface, 'blue', self.cam_rect, 2)
        
        for position in self.prediction:
            #if self.holding:
            cam_pos = Camera.displace_position(position)
            pygame.draw.circle(surface, 'green', cam_pos, 3)

        if self.holding:
            pygame.draw.circle(surface, 'grey', self.mouse_pos, 10)

    def update(self, delta):
        self.mouse_pos = pygame.mouse.get_pos()

        if self.holding and self.player.cam_pos != self.mouse_pos:
            self.difference = self.player.cam_pos - self.mouse_pos
            norm_diff = self.difference.normalize()
            magnitude = self.difference.magnitude() * 0.02  # 0.03
            magnitude = max(self.min_speed, magnitude)
            magnitude = min(magnitude, self.max_speed)

            self.launch_force = norm_diff * magnitude

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