import math
import random
import pygame
from src.engine.utils import Debug
from src.engine.constants import SPEED_FACTOR
from src.engine.asset_manager import AssetManager
from .particles import Particle


class Emitter:
    def __init__(
        self,
        angle_range: tuple[float, float],
        speed_range: tuple[float, float],
        life_range: tuple[float, float],
        rotation_range: tuple[float, float],
        color1,
        color2,
        texture,
        particle_num,
        emit_rect,
        blend_mode=None
    ):
        self.angle_range = self.start_angle, self.end_angle = angle_range
        self.speed_range = self.min_speed, self.max_speed = speed_range
        self.life_range = self.life_min, self.life_max = life_range
        self.rotation_range = self.rotation_min, self.rotation_max = rotation_range

        self.color1 = pygame.Color(color1)
        self.color2 = pygame.Color(color2)

        self.texture = texture
        self.cached_texture_rot = self.cache_rotation(self.texture, 0, 360, 1)

        self.particle_num = particle_num
        self.emit_rect = emit_rect
        self.particles = []
        self.remove_queue = []

        self.blend_mode = blend_mode

    def burst(self):
        for _ in range(self.particle_num):
            particle = self.new_particle(
                self.angle_range, 
                self.speed_range, 
                self.life_range, 
                self.rotation_range,
                self.color1,
                self.color2,
                self.texture,
                self.emit_rect,
            )
            self.particles.append(particle)

    def update(self, delta):
        Debug.add_text(f'particle count: {len(self.particles)}')
        for particle in self.particles:
            self._update_particle(particle, delta)

        # check if this really necessary
        for particle in self.remove_queue:
            self.particles.remove(particle)

    def draw(self, surface):
        for particle in self.particles:
            self._draw_particle(particle, surface)

    def new_particle(
        self,
        angle_range: tuple[float, float],
        speed_range: tuple[float, float],
        life_range: tuple[float, float],
        rotation_range: tuple[float, float],
        color1,
        color2,
        texture,
        emit_rect,
        ) -> Particle:
        
        position = [
            random.randint(0, emit_rect.width) + emit_rect.x,
            random.randint(0, emit_rect.height) + emit_rect.y
        ]
        angle = random.uniform(*angle_range)
        speed = random.uniform(*speed_range)
        life_time = random.uniform(*life_range)
        texture_rotation = random.randint(0, 360)
        rotation_change = random.randint(*rotation_range)

        particle = Particle(position, angle, speed, life_time, texture_rotation, rotation_change, color1, color2, texture)

        return particle

    def _update_particle(self, particle, delta):
        friction = 0.005 * particle.velocity
        particle.acceleration += friction
        
        try:
            progress = 1 - (particle.crnt_life / particle.life)
        except:
            print("I don't care about float division")
            progress = 0.9
        particle.crnt_color = particle.color1.lerp(particle.color2, progress)

        particle.crnt_life -= delta
        if particle.crnt_life <= 0:
            self.particles.remove(particle)

        particle.texture_rotation += particle.rotation_change * delta * SPEED_FACTOR

        particle.velocity += particle.acceleration * delta * SPEED_FACTOR
        particle.position += particle.velocity * delta * SPEED_FACTOR
        
        particle.acceleration *= 0

    def _draw_particle(self, particle, surface):
        rotated_texture = self.cached_texture_rot[int(particle.texture_rotation) % 360 - 1]
        rotated_texture_rect = rotated_texture.get_rect(center=particle.texture_rect.center)
        texture = pygame.Surface(rotated_texture.get_size())
        texture.fill(particle.crnt_color)
        texture.blit(rotated_texture, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        rotated_texture_rect.center = particle.cam_pos
        surface.blit(texture, rotated_texture_rect.topleft) # special_flags=self.blend_mode

    def clear(self):
        self.particles = []

    def cache_rotation(self, texture, start_angle, end_angle, interval):
        cached_list = []

        for angle in range(start_angle, end_angle, interval):
            rotated_texture = pygame.transform.rotate(texture, angle)

            cached_list.append(rotated_texture)
        
        return cached_list
    

class JetEmitter(Emitter):
    def __init__(self):
        self.look_range = (-10, 10)
        speed_range = (0.1, 0.2)
        life_range = (15, 20)
        rotation_range = (-1, 1)
        color1 = pygame.Color(67, 85, 133)
        color2 = pygame.Color(67, 85, 133)

        self.emit_timer = 0.1
        self.timer = self.emit_timer
        self.flying = False

        particle_num = 10
        emit_rect = pygame.Rect(0, 0, 5, 5)

        texture = AssetManager.images['particle']#.convert_alpha()
        texture.set_colorkey((0, 0, 0))

        super().__init__(
            self.look_range, 
            speed_range, 
            life_range, 
            rotation_range, 
            color1, 
            color2, 
            texture, 
            particle_num, 
            emit_rect
        )

    def update(self, delta, look_angle, jet_back, speed):
        for particle in self.particles:
            self._update_particle(particle, delta)
            
        self.emit_rect.center = jet_back

        self.look_range = (look_angle - 10 - 90, look_angle + 10 - 90)
        
        if self.flying:
            self.timer -= delta
            if self.timer < 0:
                particle = self.new_particle(
                    self.look_range, 
                    self.speed_range, 
                    self.life_range, 
                    self.rotation_range,
                    self.color1,
                    self.color2,
                    self.texture,
                    self.emit_rect,
                )
                self.particles.append(particle)
                self.timer = self.emit_timer


class BlackHoleEmitter(Emitter):
    def __init__(self, position, radius, mass):
        self.look_range = (-10, 10)
        speed_range = (0.1, 0.2)
        life_range = (0.5, 1)
        rotation_range = (-1, 1)
        color1 = pygame.Color(67, 85, 133)
        color2 = pygame.Color(67, 85, 133)

        self.emit_timer = 0.05
        self.timer = self.emit_timer
        self.flying = False

        self.mass = mass
        self.speed = mass * 0.05

        particle_num = 10
        if self.mass > 0:
            emit_rect = pygame.Rect(0, 0, radius * 2 + 60, radius * 2 + 60)
        else:
            emit_rect = pygame.Rect(0, 0, radius, radius)

        emit_rect.center = position

        texture = AssetManager.images['particle']#.convert_alpha()
        texture.set_colorkey((0, 0, 0))

        super().__init__(
            self.look_range, 
            speed_range, 
            life_range, 
            rotation_range, 
            color1, 
            color2, 
            texture, 
            particle_num, 
            emit_rect
        )

    def update_rect(self, position):
        self.emit_rect.center = position

    def update(self, delta):
        for particle in self.particles:
            self._update_particle(particle, delta)
        
        self.timer -= delta
        if self.timer < 0:
            particle = self.new_particle(
                self.life_range, 
                self.rotation_range,
                self.color1,
                self.color2,
                self.texture
            )
            self.particles.append(particle)
            self.timer = self.emit_timer

    def new_particle(
        self,
        life_range: tuple[float, float],
        rotation_range: tuple[float, float],
        color1,
        color2,
        texture,
        ) -> Particle:
        
        position = [
            random.randint(0, self.emit_rect.width) + self.emit_rect.x,
            random.randint(0, self.emit_rect.height) + self.emit_rect.y
        ]
        diff = pygame.Vector2(self.emit_rect.center) - position
        angle = math.degrees(math.atan2(-diff.y, diff.x))
        if self.mass > 0:
            life_time = (diff.length() / self.speed) * 0.016
        else:
            life_time = random.uniform(*life_range)
        texture_rotation = random.randint(0, 360)
        rotation_change = random.randint(*rotation_range)

        particle = Particle(position, angle, self.speed, life_time, texture_rotation, rotation_change, color1, color2, texture)

        return particle
