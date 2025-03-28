import pygame
from src.engine.utils import collide_circles
from src.engine.objects import *


# physics sytem
class PhysicsHandler:
    # performs physical and other calculations
    def __init__(self, player, objects, obstacles):
        self.player = player

        self.objects = objects
        self.obstacles = obstacles

    def get_forces(self, obj: Object):
        '''
        Calculate force that objects act on (position, mass)
        '''
        forces = pygame.Vector2(0, 0)
        for other_obj in self.objects:
            if isinstance(other_obj, BlackHole): # Includes OrbitingBlackHole 
                gravity_force = other_obj.calculate_attraction(obj)
                forces += gravity_force

            elif isinstance(other_obj, ForceZone):
                if other_obj.rect.collidepoint(obj.position):
                    forces += other_obj.force
                    
        return forces

    def teleport_check(self, obj: Object):
        if not hasattr(obj, "radius"):
            raise AttributeError(
                f"Object of type {type(obj).__name__} must have a 'radius' attribute."
            )
        for other_obj in self.objects:
            if isinstance(other_obj, PortalPair):
                rect = pygame.Rect(0, 0, obj.radius * 2, obj.radius * 2)
                rect.center = obj.position
                collision = other_obj.on_collision(rect, obj.velocity)

                return collision

    def draw(self, surface):
        for obj in self.objects:
            obj.draw(surface)

        for obstacle in self.obstacles:
            obstacle.draw(surface)

    def update(self, delta):
        for obj in self.objects:
            if isinstance(obj, BlackHole): 
                obj.update(delta)

        if not self.player.exploded:
            self.player.force += self.get_forces(self.player)

            collision = self.teleport_check(self.player)
            if collision:
                new_rect, new_vel = collision
                self.player.position.update(new_rect.center)
                self.player.velocity = new_vel

            self._update_obstacles(delta)   

    def _update_obstacles(self, delta):
        # update dynamic objects
        for obstacle in self.obstacles:
            obstacle.force += self.get_forces(obstacle)

            collision = self.teleport_check(obstacle)
            if collision:
                new_rect, new_vel = collision
                obstacle.position = pygame.Vector2(new_rect.center)
                obstacle.velocity = new_vel

            obstacle.update(delta)

    def object_collision(self, obj: Object):
        if not hasattr(obj, "radius"):
            raise AttributeError(
                f"Object of type {type(obj).__name__} must have a 'radius' attribute."
            )
        for other_obj in self.objects:
            if isinstance(other_obj, BlackHole):
                collision = collide_circles(
                    other_obj.position, other_obj.radius, obj.position, obj.radius
                )
                if collision:
                    return True
        for obstacle in self.obstacles:
            if isinstance(obstacle, Asteroid):
                collision = collide_circles(
                    obstacle.position, obstacle.radius, obj.position, obj.radius
                )
                if collision:
                    return True
        return False

    def predict_player(self, time, position, start_vel, mass, radius, count):
        '''
        get the position of player 
        after given time interval and prediction count
        '''
        positions = [position.copy()]

        prediction_obj = PredictionObject(position, start_vel, mass, radius)

        for _ in range(count):
            forces = self.get_forces(prediction_obj)
            prediction_obj.force += forces    
            prediction_obj.update(time)

            # portal stuff
            collision = self.teleport_check(prediction_obj)
            if collision:
                new_rect, new_vel = collision
                prediction_obj.position = pygame.Vector2(new_rect.center)
                prediction_obj.velocity = new_vel

            if self.object_collision(prediction_obj):
                return positions

            positions.append(prediction_obj.position.copy())

        return positions
        
    def read_objects(self, file_path):
        pass