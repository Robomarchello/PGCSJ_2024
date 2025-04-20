import math
import random
import pygame
from src.engine.utils import calculate_gradient, Debug
from src.engine.asset_manager import AssetManager
from src.engine.config import SPEED_FACTOR
from .emitters import Emitter, EmitterShape
from .particles import ParticleTemplate, Particle


class JetEmitter(Emitter):
    def __init__(self, emit_rect):
        gradient = calculate_gradient(
            ((129, 143, 180, 200), (129, 143, 180, 200), (5, 25, 75, 0)),
            (0.0, 0.7, 1.0),
            300
        )
        texture = AssetManager.images['particle'].convert_alpha()
        template = ParticleTemplate(
            angle_range=(-10, 10),
            speed_range=(0.1, 0.2),
            life_range=(2, 4),
            scale_range=(1, 1),
            scale_change=0.995,
            texture=texture,
            gradient=gradient,
            texture_rot_range=(-1, 1)
        )

        super().__init__(template, texture, emit_rect, emitter_type=EmitterShape.RECT)

        self.flying = False
        self.emit_timer = 0.8

    def update(self, delta, look_angle, jet_back, speed):
        self._emit_continious(delta)
        
        # Emit particles
        for _ in range(int(self.to_emit)):
            self.particles.append(self.new_particle())

        self.to_emit %= 1

        self.emit_rect.center = jet_back
        self.template.angle_range = (look_angle - 5 + 180, look_angle + 5 + 180)
        self.template.speed_range = (0.1 * speed, 0.1 * speed)

        # Update particles
        for particle in self.particles[:]:
            self._update_particle(particle, delta)
        Debug.add_text(f'particle count: {len(self.particles)}')

    def _emit_continious(self, delta):
        if self.flying:
            self.to_emit += delta / self.emit_timer * SPEED_FACTOR


class BlackHoleEmitter(Emitter):
    def __init__(self, position, radius, mass):
        self.mass = mass
        self.speed = mass * 0.05

        emit_size = radius * 2 + 60 if mass > 0 else radius
        emit_rect = pygame.Rect(0, 0, emit_size, emit_size)
        emit_rect.center = position

        texture = AssetManager.images['particle'].convert_alpha()
        gradient = calculate_gradient(
            ((67, 85, 133), (67, 85, 133)),
            (0.0, 1.0),
            300
        )
        template = ParticleTemplate(
            angle_range=(-180, 180),  # will be overridden in modify_particle
            speed_range=(self.speed, self.speed),  # fixed speed
            life_range=(0.5, 1),  # fallback for mass <= 0
            scale_range=(1, 1),
            texture=texture,
            gradient=gradient,
            texture_rot_range=(-1, 1)
        )

        super().__init__(
            template=template,
            texture=texture,
            emit_rect=emit_rect,
            emitter_type=EmitterShape.RECT
        )

        self.emit_timer = 0.05
        self.timer = self.emit_timer

    def update(self, delta):
        self.timer -= delta
        if self.timer < 0:
            self.burst(1)
            self.timer = self.emit_timer

        super().update(delta)

    def update_rect(self, position):
        self.emit_rect.center = position

    def modify_particle(self, particle: Particle):
        # Set velocity towards black hole center
        diff = pygame.Vector2(self.emit_rect.center) - particle.position

        if diff.length() == 0:
            diff = pygame.Vector2(1, 0)  # Avoid division by zero

        particle.velocity = diff.normalize() * self.speed
        angle = math.degrees(math.atan2(-diff.y, diff.x))
        particle.texture_rotation = angle

        # Custom lifetime based on distance
        if self.mass > 0:
            particle.life = (diff.length() / self.speed) * 0.016
        else:
            particle.life = random.uniform(*self.template.life_range)

        particle.age = particle.life

class ExplodeEmitter(Emitter):
    def __init__(self, emit_rect):
        gradient = calculate_gradient(
            ((67, 85, 133), (5, 24, 75)),
            (0.0, 1.0),
            300
        )
        texture = AssetManager.images['particle'].convert_alpha()
        template = ParticleTemplate(
            angle_range=(0, 360),
            speed_range=(1, 2),
            life_range=(2.5, 3.5),
            scale_range=(0, 1),
            texture=texture,
            gradient=gradient,
            texture_rot_range=(-1, 1)
        )
        super().__init__(template, texture, emit_rect, emitter_type=EmitterShape.RECT)

    def update(self, delta):
        self._emit_continious(delta)
        
        # Emit particles
        for _ in range(int(self.to_emit)):
            self.particles.append(self.new_particle())

        self.to_emit %= 1

        # Update particles
        for particle in self.particles:
            self._update_particle(particle, delta)
        Debug.add_text(f'particle count: {len(self.particles)}')