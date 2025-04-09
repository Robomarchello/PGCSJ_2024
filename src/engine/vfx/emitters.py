import random
import pygame
from pygame.locals import *
from src.engine.constants import SPEED_FACTOR
from src.engine.enums import EmitterShape
from src.engine.utils import rect_random, ellipse_random, to_range, Debug
from .particles import Particle, ParticleTemplate


class Emitter:
    def __init__(
        self,
        template: ParticleTemplate,
        texture: pygame.Surface,
        emit_rect: pygame.Rect,
        emitter_type: EmitterShape = EmitterShape.RECT,
        blend_mode=BLENDMODE_NONE
    ):
        self.template = template
        self.texture = texture
        self.emit_rect = emit_rect
        self.emitter_type = emitter_type
        self.blend_mode = blend_mode

        self.particles: list[Particle] = []
        self.cached_texture_rot = self.cache_rotation(self.texture, 0, 360, 1)

        # Continuous emission support
        self.emit_timer = 0
        self.timer = 0
        self.to_emit = 0

    # ------------------------------
    # Public methods
    # ------------------------------
    def set_emit_continious(self, duration: float, particle_count: int):
        self.emit_timer = duration / particle_count
        self.timer = duration

    def burst(self, particle_count: int):
        self.to_emit += particle_count

    def update(self, delta: float):
        self._emit_continious(delta)
        
        # Emit particles
        for _ in range(int(self.to_emit)):
            self.particles.append(self.new_particle())

        self.to_emit %= 1

        # Update particles
        for particle in self.particles:
            self._update_particle(particle, delta)

    def draw(self, surface: pygame.Surface):
        surface.fblits(
            [self._draw_particle(p) for p in self.particles],
            self.blend_mode
        )

    def clear(self):
        self.particles = []

    def modify_particle(self, particle: Particle):
        # To be optionally overridden by subclasses
        pass

    # ------------------------------
    # Internal logic
    # ------------------------------
    def _emit_continious(self, delta: float):
        if self.timer > 0:
            self.timer -= delta
            self.to_emit += delta / self.emit_timer

    def _update_particle(self, particle: Particle, delta: float):
        particle.motion_logic(delta)
        particle.age -= delta

        if particle.age < 0:
            self.particles.remove(particle)
            return

        particle.update_color()
        particle.texture_rotation += particle.texture_rot_speed * delta * SPEED_FACTOR

        particle.update_param_change(delta)

    def _draw_particle(self, particle: Particle):
        rot_frame = int(particle.texture_rotation) % 360 - 1
        rotated_texture = self.cached_texture_rot[rot_frame]
        transformed = pygame.transform.scale_by(rotated_texture, particle.scale)

        transformed.fill(particle.color, special_flags=BLEND_RGB_MULT)
        transformed.set_alpha(particle.color.a)

        rect = transformed.get_rect(center=particle.cam_pos)
        return transformed, rect.topleft

    def new_particle(self) -> Particle:
        # Position based on emitter shape
        if self.emitter_type == EmitterShape.RECT:
            position = rect_random(self.emit_rect)
        elif self.emitter_type == EmitterShape.ELLIPSE:
            position = ellipse_random(self.emit_rect)
        else:
            raise ValueError("Unsupported emitter shape")

        angle = random.uniform(*to_range(self.template.angle_range))
        speed = random.uniform(*to_range(self.template.speed_range))
        texture_rot_speed = random.uniform(*to_range(self.template.texture_rot_range))
        life = random.uniform(*to_range(self.template.life_range))
        scale = random.uniform(*to_range(self.template.scale_range))

        particle = Particle(
            position=pygame.Vector2(position),
            angle=angle,
            speed=speed,
            life=life,
            scale=scale,
            texture=self.texture,
            gradient=self.template.gradient,
            texture_rot_speed=texture_rot_speed,
            velocity_change=self.template.velocity_change,
            scale_change=self.template.scale_change
        )

        self.modify_particle(particle)
        return particle

    def cache_rotation(self, texture, start_angle, end_angle, interval):
        cached_list = []
        for angle in range(start_angle, end_angle, interval):
            rotated_texture = pygame.transform.rotate(texture, angle)
            cached_list.append(rotated_texture)
        return cached_list
