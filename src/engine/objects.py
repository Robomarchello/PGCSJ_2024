# TODO/ideas: 
# Physics handler, black hole (attractor), negative mass object (repel), asteroids (static and dynamic ones)
# teleport, timed barriers, gravity inversion timer, reflective surfaces, additional launch thingy
from dataclasses import dataclass
import pygame
from src.engine.constants import GRAVITY_CONST, SPEED_FACTOR
from src.engine.utils import collide_circles


__all__ = ['BlackHole', 'Asteroid', 'ForceZone', 
           'GravityInvertor', 'ObjectHandler', 'Collectible',
           'Portal', 'PortalPair', 'LaunchPoint', 'FinishPoint'
           ]


class BlackHole:
    def __init__(self, position, mass):
        self.position = position
        self.mass = mass 

        self.radius = 20
        self.color = pygame.Color(255, 255, 255)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.position, self.radius)
        
    def calculate_attraction(self, position_other, mass_other):
        diff = self.position - position_other
        if diff == (0, 0):
            return pygame.Vector2(0, 0), 0
        direction = diff.normalize()
        distance = diff.magnitude()
        gravity_force = (GRAVITY_CONST * mass_other * self.mass) / distance ** 2
        
        return direction * gravity_force


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
        self.force = force
        self.rect = pygame.Rect(rect)

        self.timer = timer
        self.crnt_timer = timer

    def draw(self, surface):
        pygame.draw.rect(surface, 'orange', self.rect, 5)

    def update(self, delta):
        pass


class Collectible:
    def __init__(self, position, texture=None, texture_picked=None):
        self.position = position

        self.rect = texture.get_rect(center=self.position)
        self.radius = self.rect.width / 2

        self.picked_up = False

        self.texture = texture
        self.texture_picked = texture_picked

    def draw(self, surface):
        # make animation?
        if not self.picked_up:
            surface.blit(self.texture, self.rect.topleft)
        else:
            surface.blit(self.texture_picked, self.rect.topleft)
        #surface.blit(self.texture, self.rect.topleft)


@dataclass
class Portal:
    rect: pygame.Rect
    hitrect: pygame.Rect
    normal: pygame.Vector2    
    color: pygame.Color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, 'white', self.hitrect)


class PortalPair:
    def __init__(self, portal_1, portal_2):
        self.portal_1 = portal_1
        self.portal_2 = portal_2

    def update(self, delta):
        pass

    def draw(self, surface):
        self.portal_1.draw(surface)
        self.portal_2.draw(surface)

    def on_collision(self, rect, velocity):
        if velocity == (0, 0):
            return False
        
        rect_after = rect.copy()
        vel_after = velocity.copy()
        vel_normal = vel_after.normalize()
        
        dot_check = vel_normal.dot(self.portal_1.normal)
        if self.portal_1.hitrect.colliderect(rect) and dot_check > 0.0:
            portal_angle = self.portal_1.normal.angle_to(self.portal_2.normal)
            rect_after.center = self.portal_2.rect.center
            vel_after.rotate_ip(portal_angle)
            
            return rect_after, vel_after

        dot_check = vel_normal.dot(self.portal_2.normal) 
        if self.portal_2.hitrect.colliderect(rect) and dot_check < 0.0:
            portal_angle = self.portal_2.normal.angle_to(self.portal_1.normal)
            rect_after.center = self.portal_1.rect.center
            vel_after.rotate_ip(portal_angle)

            return rect_after, vel_after

        return False


class ReflectiveSurface:
    def __init__(self, start_pos, end_pos):
        self.start_pos = pygame.Vector2(start_pos)
        self.end_pos = pygame.Vector2(end_pos)

        line = self.end_pos - self.start_pos
        self.normal = line.normalize().rotate(90)

    def draw(self, surface):
        pygame.draw.line(surface, (255, 0, 0), self.start_pos, self.end_pos, 5)

    def get_closest(self, position):
        # feels kinda hard to implement, so L.A.T.E.R
        pass

    def resolve_collision(self, position):
        pass


class GravityInvertor:
    def __init__(self, position, timer, object_handler):
        self.position = position

        self.timer = timer
        self.crnt_timer = timer
        self.object_handler = object_handler
        
    def draw(self, surface):
        pass

    def update(self, delta):
        self.crnt_timer -= delta
        if self.crnt_timer < 0:
            self.crnt_timer = self.timer

            # *invert here* (which is probably is *-1 object's or player's mass )


class LaunchPoint:
    def __init__(self, position, radius, player, controller):
        self.position = position
        self.radius = radius

        self.player = player
        self.controller = controller
        
        self.used = False

    def update(self, delta):
        collision = collide_circles(
            self.position, self.radius,
            self.player.position, self.player.radius
        )
        if collision and not self.used:
            self.player.freeze = True
            self.controller.shot = True

            self.controller.launch_point = self

            pull_force = self.pull_to_force(self.player.position)
            self.player.position += pull_force * delta * SPEED_FACTOR

    def pull_to_force(self, position): 
        difference = pygame.Vector2(
            self.position[0] - position[0],
            self.position[1] - position[1]
        )
        return difference * 0.18

    def draw(self, surface):
        pygame.draw.circle(surface, 'grey', self.position, self.radius)


class FinishPoint:
    def __init__(self, position, radius, player):
        self.position = position
        self.radius = radius

        self.player = player
        
        self.touched = False

        self.complete_timer = 2.0
        self.timer = self.complete_timer
        self.completed = False

    def update(self, delta):
        collision = collide_circles(
            self.position, self.radius,
            self.player.position, self.player.radius
        )
        if collision and not self.completed:
            self.player.freeze = True
            self.touched = True

            pull_force = self.pull_to_force(self.player.position)
            self.player.position += pull_force * delta * SPEED_FACTOR

        if self.touched:
            self.timer -= delta

            if self.timer < 0.0:
                self.completed = True

    def pull_to_force(self, position): 
        difference = pygame.Vector2(
            self.position[0] - position[0],
            self.position[1] - position[1]
        )
        return difference * 0.1

    def draw(self, surface):
        pygame.draw.circle(surface, 'yellow', self.position, self.radius)



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
        forces = self.get_forces(self.player.position, self.player.mass)
        self.player.acceleration += forces

        collision = self.teleport_check(
            self.player.position, 
            10, self.player.velocity
            )
        if collision:
            new_rect, new_vel = collision
            self.player.position = new_rect.center
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

            positions.append(last_pos.copy())

        if count == 1:
            return last_pos
        else:
            return positions
        
    def read_objects(self, file_path):
        pass