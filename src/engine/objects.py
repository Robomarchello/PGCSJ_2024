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


class Asteroid:
    def __init__(self, position, velocity, mass, radius):
        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(velocity)
        self.acceleration = pygame.Vector2()
        self.force = pygame.Vector2()

        self.mass = mass
        self.radius = radius

        self.orientation = 0.0

    def update(self, delta):
        self.acceleration += self.force / self.mass
        self.velocity += self.acceleration * delta * SPEED_FACTOR
        self.position += self.velocity * delta * SPEED_FACTOR

        self.acceleration *= 0
        self.force *= 0
    
    def draw(self, surface):
        pygame.draw.circle(surface, 'grey', self.position, self.radius)


class ForceZone:
    def __init__(self, force, rect, timer=0.0):
        pass

    def draw(self):
        pass


class GravityInvertor:
    def __init__(self, position, timer, physics_handler):
        self.position = position

        self.timer = timer
        self.crnt_timer = timer
        self.physics_handler = physics_handler
        
    def draw(self, surface):
        pass

    def update(self, delta):
        self.crnt_timer -= delta
        if self.crnt_timer < 0:
            self.crnt_timer = self.timer

            # *invert here* (which is probably is *-1 object's or player's mass )


class PhysicsHandler:
    def __init__(self, player, objects, obstacles):
        self.player = player

        self.objects = objects
        self.obstacles = obstacles

    def draw(self, surface):
        for obj in self.objects:
            obj.draw(surface)

        for obstacle in self.obstacles:
            obstacle.draw(surface)

    def update(self, delta):
        for obj in self.objects:
            if isinstance(obj, BlackHole):
                norm_vec, gravity_force = obj.calculate_attraction(
                    self.player.position, self.player.mass
                )

                self.player.acceleration += norm_vec * gravity_force

        self._update_obstacles(delta)
            

    def _update_obstacles(self, delta):
        # update dynamic objects
        for obstacle in self.obstacles:
            for obj in self.objects:
            
                if isinstance(obj, BlackHole):
                    norm_vec, gravity_force = obj.calculate_attraction(
                        obstacle.position, obstacle.mass
                    )

                obstacle.force += norm_vec * gravity_force

            obstacle.update(delta)

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
            for obj in self.objects:
                if isinstance(obj, BlackHole):
                    norm_vec, gravity_force = obj.calculate_attraction(
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