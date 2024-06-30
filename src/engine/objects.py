# TODO/ideas: 
# Physics handler, black hole (attractor), negative mass object (repel), asteroids (static and dynamic ones)
# teleport, timed barriers, gravity inversion timer, reflective surfaces, additional launch thingy
import pygame
from src.engine.constants import GRAVITY_CONST, SPEED_FACTOR


class BlackHole:
    def __init__(self, position, mass):
        self.position = position
        self.mass = mass  # with negative mass repels👍

        self.radius = 20
        self.color = pygame.Color(255, 255, 255)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.position, self.radius)
        
    def calculate_attraction(self, position_other, mass_other):
        diff = self.position - position_other
        norm_vec = diff.normalize()
        distance = diff.magnitude()
        gravity_force = (GRAVITY_CONST * mass_other * self.mass) / distance ** 2
        
        return norm_vec, gravity_force


class PhysicsHandler:
    def __init__(self, player, objects):
        self.player = player

        self.objects = objects

    def draw(self, surface):
        for obj in self.objects:
            obj.draw(surface)

    def update(self, delta):
        for object in self.objects:
            if type(object) == BlackHole:
                norm_vec, gravity_force = object.calculate_attraction(
                    self.player.position, self.player.mass
                )

                self.player.acceleration += norm_vec * gravity_force

    def predict_player(self, time, position, start_vel, start_accel, count):
        '''
        get the position of player 
        after given time interval and prediction count
        '''
        positions = [position.copy()]
        velocity = pygame.Vector2(start_vel)
        acceleration = pygame.Vector2(start_accel)

        for _ in range(count):
            last_pos = positions[-1]
            for object in self.objects:
                if isinstance(object, BlackHole):
                    norm_vec, gravity_force = object.calculate_attraction(
                        last_pos, self.player.mass
                    )

                acceleration += norm_vec * gravity_force

            velocity += acceleration * time * SPEED_FACTOR
            last_pos += velocity * time * SPEED_FACTOR
            acceleration *= 0 

            positions.append(last_pos.copy())

        if count == 1:
            return last_pos
        else:
            return positions
        
    def read_objects(self, file_path):
        pass