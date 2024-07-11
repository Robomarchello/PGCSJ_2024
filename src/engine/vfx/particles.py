import pygame
import math
import random
from src.engine.constants import SPEED_FACTOR
from utils import Debug


class Particle:
    def __init__(self, position, angle, speed, life, rotation,
                  rotation_change, color1, color2, texture):
        self.position = position
        self.velocity = pygame.Vector2(
            speed * math.cos(math.radians(angle)),
            -speed * math.sin(math.radians(angle))
        )
        self.acceleration = pygame.Vector2(0, 0)

        self.life = life
        self.crnt_life = life

        self.texture_rotation = rotation
        self.rotation_change = rotation_change

        self.color1 = color1
        self.color2 = color2
        self.crnt_color = color1

        self.texture = texture
        self.texture_rect = texture.get_rect()



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

        self.emit_timer = 0.1
        self.timer = self.emit_timer

        for _ in range(self.particle_num):
            particle = self.new_particle(
                self.angle_range, 
                self.speed_range, 
                self.life_range, 
                self.rotation_range,
                self.color1,
                self.color2,
                texture,
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

        self.timer -= delta
        if self.timer < 0:
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
            self.timer = self.emit_timer

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
        life_time = random.randrange(*life_range)
        texture_rotation = random.randint(0, 360)
        rotation_change = random.randint(*rotation_range)

        particle = Particle(position, angle, speed, life_time, texture_rotation, rotation_change, color1, color2, texture)

        return particle

    def _update_particle(self, particle, delta):
        particle.acceleration[1] = 0.1
        #particle.acceleration += -0.01 * particle.velocity

        progress = 1 - (particle.crnt_life / particle.life)
        particle.crnt_color = particle.color1.lerp(particle.color2, progress)

        particle.crnt_life -= delta
        if particle.crnt_life < 0:
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
        texture.blit(rotated_texture, (0, 0), special_flags=pygame.BLEND_MULT)

        rotated_texture_rect.center = particle.position
        surface.blit(texture, rotated_texture_rect.topleft, special_flags=pygame.BLEND_ADD)

        return
        pygame.draw.circle(
            surface, 
            (255, 0, 0), 
            particle.position, 
            10,
        )

    def cache_rotation(self, texture, start_angle, end_angle, interval):
        cached_list = []

        for angle in range(start_angle, end_angle, interval):
            rotated_texture = pygame.transform.rotate(texture, angle)

            cached_list.append(rotated_texture)
        
        return cached_list

    def from_file():
        # TODO: create emitter from json file
        pass