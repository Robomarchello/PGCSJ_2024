import math
import random
from typing import Tuple
from dataclasses import dataclass
import pygame
from pygame.locals import *
from src.engine.constants import SPEED_FACTOR
from src.engine.utils import Debug, rect_random, ellipse_random, to_range
from src.engine.enums import EmitterShape


@dataclass
class ParticleTemplate:
    angle_range: float | Tuple[float]
    speed_range: float | Tuple[float]
    life_range: float | Tuple[float]
    scale_range: float | Tuple[float]

    texture: pygame.Surface
    gradient: Tuple[pygame.Color]

    texture_rot_range: float | Tuple[float]

    velocity_change: float = 1.0
    scale_change: float = 1.0


class Particle:
    def __init__(
            self,
            position,
            angle,
            speed,
            life,
            scale,
            texture,
            gradient,
            texture_rot_speed,
            velocity_change=1.0,
            scale_change=1.0
        ):
        self.position = position
        self.velocity = pygame.Vector2(
            speed * math.cos(math.radians(angle)),
            -speed * math.sin(math.radians(angle))
        )
        self.acceleration = pygame.Vector2()
        
        self.life = life
        self.age = life

        self.scale = scale
        self.texture = texture
        self.texture_rotation = angle
        self.texture_rot_speed = texture_rot_speed

        self.gradient = gradient
        self.update_color()

        self.velocity_change = velocity_change
        self.scale_change = scale_change

        self.texture_rect = texture.get_rect()

    def motion_logic(self, delta):
        self.velocity += self.acceleration * delta * SPEED_FACTOR
        self.position += self.velocity * delta * SPEED_FACTOR

        self.acceleration *= 0
    
    def update_param_change(self, delta):
        self.scale += self.scale * (self.scale_change - 1) * delta * SPEED_FACTOR
        self.velocity += self.velocity * (self.velocity_change - 1) * delta * SPEED_FACTOR

    def update_color(self):
        progress = min(self.age / self.life, 0.9999)  # ensure index is in bounds
        index = int(progress * len(self.gradient))
        self.color = self.gradient[index]


class Particles:
    def __init__(
        self,
        texture,
        particle_template: ParticleTemplate,
        blend_mode=BLENDMODE_NONE
        ):
        self.particle_template = particle_template
        self.particles = []
        
        self.gradient = particle_template.gradient
        self.blend_mode = blend_mode

        self.texture = texture
        self.texture_cached = self.cache_rotation(self.texture, 0, 360, 360)

        self.emitters = []

    def update(self, delta):
        Debug.add_text(f'particle count: {len(self.particles)}')
        
        for particle in self.particles:
            self._update_particle(particle, delta)
        
        for task in self.tasks:
            task.update(delta)

    def _update_particle(self, particle: Particle, delta):
        # Update physics
        particle.motion_logic(delta)

        # Update life
        particle.age -= delta
        if particle.age < 0:
            self.particles.remove(particle)
            return 

        particle.update_color()

        # Update texture rotation
        particle.texture_rotation += particle.texture_rot_speed * delta * SPEED_FACTOR

    def draw(self, surface):
        surface.fblits([self._draw_particle(particle, surface) for particle in self.particles], self.blend_mode)
    
    def _draw_particle(self, particle: Particle):
        rot_frame = int(particle.texture_rotation) % 360 - 1
        rotated_texture = self.texture_cached[rot_frame]
        transformed_texture = pygame.transform.scale_by(
            rotated_texture, 
            particle.scale
        )
        trans_texture_rect = transformed_texture.get_rect()

        transformed_texture.fill(
            particle.color,
            special_flags=BLEND_RGB_MULT
        )
        transformed_texture.set_alpha(particle.color.a)

        trans_texture_rect.center = particle.position

        return transformed_texture, trans_texture_rect.topleft

    def cache_rotation(self, texture, start_angle, end_angle, interval):
        cached_list = []

        for angle in range(start_angle, end_angle, interval):
            rotated_texture = pygame.transform.rotate(texture, angle)

            cached_list.append(rotated_texture)
        
        return cached_list

    def from_file():
        # TODO: create emitter from json file
        pass


class Emitter:
    def __init__(
            self, 
            particle_template,
            emit_rect: pygame.Rect,
            emitter_type: EmitterShape,
            manager: ParticleHandler,
            ):
        self.particle_template = particle_template
        self.emit_rect = emit_rect
        self.emitter_type = emitter_type
        self.manager = manager

        self.timer = 0
        self.emit_interval = 0
        self.to_emit = 0

    def update(self, delta):
        self._emit_continious(delta)

        # add particle to system
        for _ in range(int(self.to_emit)):
            self.new_particle(self.emit_rect)

        self.to_emit %= 1

    def set_emit_continious(self, duration, particle_count):
        self.timer = duration
        self.emit_interval = duration / particle_count

    def burst(self, particle_num):
        self.to_emit += particle_num

    def _emit_continious(self, delta):
        timer -= delta
        if timer < 0:
            self.inactive = True
        self.to_emit += delta / self.emit_interval

    def modify_particle(self, particle):
        '''
        A hack to allow new classes to  modify particle before making sending it to manager.
        Probably not a good solution.
        '''
        pass

    def new_particle(self): 
        if self.emitter_type == EmitterShape.RECT:
            position = rect_random(self.emit_rect)

        elif self.emitter_type == EmitterShape.ELLIPSE:
            position = ellipse_random(self.emit_rect)

        angle = random.uniform(*to_range(self.particle_template.angle_value))
        speed = random.uniform(*to_range(self.particle_template.speed_value))
        texture_rot_speed = random.uniform(*to_range(self.particle_template.texture_rot_value))
        life = random.uniform(*to_range(self.particle_template.life_value))
        scale = random.uniform(*to_range(self.particle_template.scale_value))

        particle = Particle(
            position=position,
            angle=angle,
            speed=speed,
            life=life,
            scale=scale,
            gradient=self.manager.gradient,
            texture_rot_speed=texture_rot_speed,
            velocity_change=self.particle_template.velocity_change,
            scale_change=self.particle_template.scale_change,
        )
        self.modify_particle(particle)

        self.manager.particles.append(particle)