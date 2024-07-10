from dataclasses import dataclass
import pygame
from src.engine.constants import SPEED_FACTOR
from src.engine.utils import collide_circles
from src.engine.objects.objects import *


class ObjectHandler:
    # performs physical and other calculations
    def __init__(self, player, objects, obstacles):
        self.player = player

        self.objects = objects
        self.obstacles = obstacles

    def get_forces(self, position, mass):
        '''
        Calculate forces that self.objects act on a body (position, mass)
        '''
        forces = pygame.Vector2(0, 0)
        for obj in self.objects:
            if isinstance(obj, BlackHole):
                gravity_force = obj.calculate_attraction(
                    position, mass
                )

                forces += gravity_force

            if isinstance(obj, OrbitingBlackHole):
                gravity_force = obj.calculate_attraction(
                    position, mass
                )
                forces += gravity_force

            if isinstance(obj, ForceZone):
                if obj.rect.collidepoint(position):
                    forces += obj.force

        return forces

    def teleport_check(self, position, radius, velocity):
        for obj in self.objects:
            if isinstance(obj, PortalPair):
                rect = pygame.Rect(0, 0, radius * 2, radius * 2)
                rect.center = position
                collision = obj.on_collision(rect, velocity)

                return collision

    def draw(self, surface):
        for obj in self.objects:
            obj.draw(surface)

        for obstacle in self.obstacles:
            obstacle.draw(surface)

    def update(self, delta):
        for obj in self.objects:
            if isinstance(obj, OrbitingBlackHole):
                obj.update(delta)

        forces = self.get_forces(self.player.position, self.player.mass)
        self.player.acceleration += forces

        collision = self.teleport_check(
            self.player.position, 
            10, self.player.velocity
            )
        if collision:
            new_rect, new_vel = collision
            self.player.position.update(new_rect.center)
            self.player.velocity = new_vel

        self._update_obstacles(delta)

    def _update_obstacles(self, delta):
        # update dynamic objects
        for obstacle in self.obstacles:
            forces = self.get_forces(obstacle.position, obstacle.mass)
            obstacle.force += forces

            collision = self.teleport_check(
                obstacle.position, 
                10, obstacle.velocity
                )
            if collision:
                new_rect, new_vel = collision
                obstacle.position = pygame.Vector2(new_rect.center)
                obstacle.velocity = new_vel

            obstacle.update(delta)

    def black_holes_collision(self, position, radius):
        for obj in self.objects:
            if isinstance(obj, BlackHole):
                collision = collide_circles(
                    obj.position, obj.radius,
                    position, radius
                )
                if collision:
                    return True

            if isinstance(obj, OrbitingBlackHole):
                collision = collide_circles(
                    obj.position, obj.radius,
                    position, radius
                )
                if collision:
                    return True
        
        return False

    def predict_player(self, time, position, start_vel, start_accel, count):
        '''
        get the position of player 
        after given time interval and prediction count
        '''
        positions = [position.copy()]
        velocity = pygame.Vector2(start_vel)
        acceleration = pygame.Vector2(start_accel)
        radius = self.player.radius

        for _ in range(count):
            last_pos = positions[-1]
            forces = self.get_forces(last_pos, self.player.mass)

            acceleration += forces    

            velocity += acceleration * time * SPEED_FACTOR
            last_pos += velocity * time * SPEED_FACTOR
            acceleration *= 0 

            # portal stuff
            collision = self.teleport_check(
                last_pos, 
                10, velocity
                )
            if collision:
                new_rect, new_vel = collision
                last_pos = pygame.Vector2(new_rect.center)
                velocity = new_vel

            if self.black_holes_collision(last_pos, radius):
                return positions

            positions.append(last_pos.copy())

        if count == 1:
            return last_pos
        else:
            return positions
        
    def read_objects(self, file_path):
        pass