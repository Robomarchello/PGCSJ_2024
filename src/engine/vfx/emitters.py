import math
import random
from typing import Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import pygame
from pygame.locals import *
from src.engine.constants import SPEED_FACTOR
from src.engine.utils import Debug, calculate_gradient


class Shape(Enum):
    RECT = 1
    CIRCLE = 2


class EmitterShape(Enum):
    RECT = 'rect'
    ELLIPSE = 'ellipse'


def to_range(value):
    if isinstance(value, tuple):
        return list(value)
    if isinstance(value, list):
        return value
    return [value, value]


@dataclass
class ParticleTemplate:
    angle_range: float | Tuple[float]
    speed_range: float | Tuple[float]
    texture_rot_range: float | Tuple[float]
    life_range: float | Tuple[float]
    scale_range: float | Tuple[float]
    color: 'ColorBehavior'
    velocity_change: float = 1.0
    scale_change: float = 1.0
    texture: Optional[pygame.Surface] = None
    shape: Optional[Shape] = None


@dataclass
class ColorBehavior:
    color: Optional[pygame.Color] = None
    gradient: Optional[Tuple[pygame.Color]] = None

    def get_color(self, age: float, life: float) -> pygame.Color:
        if self.color is not None:
            return self.color
        if self.gradient is not None:
            progress = min(age / life, 0.9999) # so the index in bounds
            index = int(progress * len(self.gradient))
            return self.gradient[index]

class Particle:
    def __init__(
            self,
            position,
            angle,
            speed,
            texture_rot_speed,
            life,
            scale,
            gradient,
            velocity_change = 1.0,
            scale_change = 1.0,
            texture=None,
            shape=None,
            ):
        self.position = position
        self.velocity = pygame.Vector2(
            speed * math.cos(math.radians(angle)),
            -speed * math.sin(math.radians(angle))
        )
        self.acceleration = pygame.Vector2()
        
        self.texture_rotation = angle
        self.texture_rot_speed = texture_rot_speed

        self.crnt_color = gradient[0]

        self.life = life
        self.half_life = self.life / 2
        self.crnt_life = life

        self.scale = scale

        self.velocity_change = velocity_change
        self.scale_change = scale_change

        self.texture_rect = texture.get_rect()
        self.shape = shape


class Emitter:
    def __init__(
        self,
        particle_template: ParticleTemplate,
        emit_rect: pygame.Rect,
        blend_mode=BLENDMODE_NONE
    ):
        self.particle_template = particle_template

        self.emit_rect = emit_rect
        self.particles = []

        self.gradient = calculate_gradient(
            particle_template.colors, 
            particle_template.color_intervals,
            300
        )

        # continious emitting
        self.emit_timer = 3.5 / 1000
        self.timer = self.emit_timer

        self.blend_mode = blend_mode

        # Make this a parameter
        self.emitter_type = EmitterShape.ELLIPSE

    def burst(self, particle_num):
        for _ in range(particle_num):
            particle = self.new_particle(self.emit_rect)
            self.particles.append(particle)

    def update(self, delta):
        Debug.add_text(f'particle count: {len(self.particles)}')
        
        for particle in self.particles:
            self._update_particle(particle, delta)

        self.timer -= delta
        if self.timer < 0:
            steps_skipped = abs(math.ceil(self.timer / self.emit_timer))
            for _ in range(steps_skipped + 1):
                particle = self.new_particle(self.emit_rect)

                self.particles.append(particle)
            
            self.timer = self.emit_timer

    def draw(self, surface):
        surface.fblits([self._draw_particle(particle, surface) for particle in self.particles], self.blend_mode)

    def _get_particle_color(self, particle: Particle):
        progress = 1 - (particle.crnt_life / particle.life)

        gradient = self.gradient
        # bug here
        color = gradient[int(progress * len(gradient))] # - 1

        return color
    
    def _update_particle(self, particle: Particle, delta):
        # Update acceleration
        particle.acceleration += particle.velocity * (particle.velocity_change - 1)

        particle.crnt_color = self._get_particle_color(particle)

        # Update physics
        particle.motion_logic(delta)

        # Update life
        particle.crnt_life -= delta
        if particle.crnt_life < 0:
            self.particles.remove(particle)
            return 

        # Update scale
        scale_change = particle.scale * (particle.scale_change - 1) * delta * SPEED_FACTOR
        particle.scale += scale_change

        # Update texture rotation
        particle.texture_rotation += particle.texture_rot_speed * delta * SPEED_FACTOR

    def _draw_particle(self, particle: Particle, surface):
        pass

    def new_particle(self, emit_rect) -> Particle: 
        if self.emitter_type == EmitterShape.RECT:
            position = self._rect_random(emit_rect)

        elif self.emitter_type == EmitterShape.ELLIPSE:
            position = self._ellipse_random(emit_rect)

        angle = random.uniform(*to_range(self.particle_template.angle_value))
        speed = random.uniform(*to_range(self.particle_template.speed_value))
        texture_rot_speed = random.uniform(*to_range(self.particle_template.texture_rot_value))
        life = random.uniform(*to_range(self.particle_template.life_value))
        scale = random.uniform(*to_range(self.particle_template.scale_value))

        particle = Particle(
            position,
            angle,
            speed,
            texture_rot_speed,
            life,
            scale,
            self.gradient,
            self.particle_template.velocity_change,
            self.particle_template.scale_change,
            texture=self.particle_template.texture,
            shape=self.particle_template.shape
        )

        return particle

    def _ellipse_random(self, rect):
        angle = random.uniform(0, 6.28)
        length_w = random.uniform(0, rect.width / 2)
        length_h = random.uniform(0, rect.height / 2)
        position = (
            math.cos(angle) * length_w + rect.centerx,
            -math.sin(angle) * length_h + rect.centery
        )

        return position
    
    def _rect_random(self, rect):
        position = (
            random.randint(0, rect.width) + rect.x,
            random.randint(0, rect.height) + rect.y
        )

        return position
    
    def cache_rotation(self, texture, start_angle, end_angle, interval):
        cached_list = []

        for angle in range(start_angle, end_angle, interval):
            rotated_texture = pygame.transform.rotate(texture, angle)

            cached_list.append(rotated_texture)
        
        return cached_list

    def from_file():
        # TODO: create emitter from json file
        pass


class Textured_Emitter(Emitter):
    def __init__(
        self,
        particle_template: ParticleTemplate,
        emit_rect: pygame.Rect,
        texture: pygame.Surface,
        blend_mode=BLENDMODE_NONE
    ):
        self.texture = texture
        self.cached_texture_rot = self.cache_rotation(texture, 0, 360, 1)

        super().__init__(particle_template, emit_rect, blend_mode)

    def draw(self, surface):
        surface.fblits([self._draw_particle(particle, surface) for particle in self.particles], self.blend_mode)
    
    def _draw_particle(self, particle: Particle, surface):
        rot_frame = int(particle.texture_rotation) % 360 - 1
        rotated_texture = self.cached_texture_rot[rot_frame]
        transformed_texture = pygame.transform.scale_by(
            rotated_texture, 
            particle.scale
        )
        trans_texture_rect = transformed_texture.get_rect()

        transformed_texture.fill(
            particle.crnt_color,
            special_flags=BLEND_RGB_MULT
        )
        transformed_texture.set_alpha(particle.crnt_color.a)

        trans_texture_rect.center = particle.position

        return transformed_texture, trans_texture_rect.topleft
    

class pg_draw_Emitter(Emitter):
    def __init__(
        self,
        particle_template: ParticleTemplate,
        emit_rect: pygame.Rect,
        shape: Shape,
        blend_mode=BLENDMODE_NONE
    ):
        self.shape = shape
        
        super().__init__(particle_template, emit_rect, blend_mode)

    def draw(self, surface):
        for particle in self.particles:
            self._particle_draw(surface, particle)

    def _particle_draw(self, surface, particle: Particle):
        if self.shape == Shape.RECT:
            pygame.draw.rect(
                surface,
                self._get_particle_color(particle),
                particle.texture_rect
            )
            
        if self.shape == Shape.CIRCLE:
            pygame.draw.circle(
                surface,
                self._get_particle_color(particle),
                particle.position,
                30 * particle.scale
            )