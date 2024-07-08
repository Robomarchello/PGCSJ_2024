# TODO/ideas: 
# Physics handler, black hole (attractor), negative mass object (repel), asteroids (static and dynamic ones)
# teleport, timed barriers, gravity inversion timer, reflective surfaces, additional launch thingy
from dataclasses import dataclass
import pygame
from src.engine.constants import GRAVITY_CONST, SPEED_FACTOR
from src.engine.utils import collide_circles
from src.engine.camera import Camera
from src.engine.asset_manager import AssetManager

__all__ = ['BlackHole', 'OrbitingBlackHole', 'Asteroid', 
           'ForceZone', 'GravityInvertor', 'ObjectHandler', 
           'Collectible', 'Portal', 'PortalPair', 
           'LaunchPoint', 'FinishPoint'
           ]


class BlackHole:
    def __init__(self, position, mass):
        self.position = pygame.Vector2(position)
        self.mass = mass 

        self.radius = 25 + abs(mass) * 0.15
        self.color = pygame.Color(255, 255, 255)

    @property
    def cam_pos(self):
        return Camera.displace_position(self.position)

    def draw(self, surface):
        if self.mass > 0:
            pygame.draw.circle(surface, self.color, self.cam_pos, self.radius)
        else:
            pygame.draw.circle(surface, self.color, self.cam_pos, self.radius, 5)

    def calculate_attraction(self, position_other, mass_other):
        diff = self.position - position_other
        if diff == (0, 0):
            return pygame.Vector2(0, 0), 0
        direction = diff.normalize()
        distance = diff.magnitude()
        gravity_force = (GRAVITY_CONST * mass_other * self.mass) / distance ** 2
        
        return direction * gravity_force


class OrbitingBlackHole(BlackHole):
    def __init__(self, origin, position, mass, rot_speed):
        super().__init__(position, mass)

        self.origin = pygame.Vector2(origin)
        self.rot_speed = rot_speed

    # def draw additional circle

    def update(self, delta):
        vec = self.position - self.origin
        vec.rotate_ip(self.rot_speed * delta * SPEED_FACTOR)

        new_position = vec + self.origin
        self.position = new_position


class Asteroid:
    def __init__(self, position, velocity, mass, radius):
        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(velocity)
        self.acceleration = pygame.Vector2()
        self.force = pygame.Vector2()

        self.mass = mass
        self.radius = radius

        self.orientation = 0.0

    @property
    def cam_pos(self):
        return Camera.displace_position(self.position)

    def update(self, delta):
        self.acceleration += self.force / self.mass
        self.velocity += self.acceleration * delta * SPEED_FACTOR
        self.position += self.velocity * delta * SPEED_FACTOR

        self.acceleration *= 0
        self.force *= 0
    
    def draw(self, surface):
        pygame.draw.circle(surface, 'grey', self.cam_pos, self.radius)


class ForceZone:
    def __init__(self, force, rect, timer=0.0):
        self.force = force
        self.rect = pygame.Rect(rect)

        self.timer = timer
        self.crnt_timer = timer

    @property
    def cam_rect(self):
        return Camera.displace_rect(self.rect)

    def draw(self, surface):
        pygame.draw.rect(surface, 'orange', self.cam_rect, 5)

    def update(self, delta):
        pass


class Collectible:
    def __init__(self, position, texture_key, texture_key_picked):
        self.position = pygame.Vector2(position)

        self.texture_key = texture_key
        self.texture_key_picked = texture_key_picked

        self.texture = AssetManager.images[texture_key]
        self.texture_picked = AssetManager.images[texture_key_picked]

        self.rect = self.texture.get_rect(center=self.position)
        self.radius = self.rect.width / 2

        self.picked_up = False

    @property
    def cam_pos(self):
        return Camera.displace_position(self.position)

    def draw(self, surface):
        cam_rect = self.rect.copy()
        cam_rect.center = self.cam_pos

        # make animation?
        if not self.picked_up:
            surface.blit(self.texture, cam_rect.topleft)
        else:
            surface.blit(self.texture_picked, cam_rect.topleft)
        #surface.blit(self.texture, self.rect.topleft)


@dataclass
class Portal:
    rect: pygame.Rect
    hitrect: pygame.Rect
    normal: pygame.Vector2    
    color: pygame.Color

    def draw(self, surface):
        cam_rect = self.rect.copy()
        cam_rect.x -= Camera.pos[0]
        cam_rect.x -= Camera.pos[1]
        # temporary thing?
        cam_hit_rect = self.rect.copy()
        cam_hit_rect.x -= Camera.pos[0]
        cam_hit_rect.x -= Camera.pos[1]
        pygame.draw.rect(surface, self.color, cam_rect)
        pygame.draw.rect(surface, 'white', cam_hit_rect)


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

    @property
    def cam_pos(self):
        return Camera.displace_position(self.position)

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
        pygame.draw.circle(surface, 'grey', self.cam_pos, self.radius)


class FinishPoint:
    def __init__(self, position, radius, player):
        self.position = pygame.Vector2(position)
        self.radius = radius

        self.player = player
        
        self.touched = False

        self.complete_timer = 2.0
        self.timer = self.complete_timer
        self.completed = False

    @property
    def cam_pos(self):
        return Camera.displace_position(self.position) 

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
        pygame.draw.circle(surface, 'yellow', self.cam_pos, self.radius)



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

        if self.black_holes_collision():
            print('Collision!')

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

    def black_holes_collision(self):
        for obj in self.objects:
            if isinstance(obj, BlackHole):
                collision = collide_circles(
                    obj.position, obj.radius,
                    self.player.position, self.player.radius
                )
                if collision:
                    return True

            if isinstance(obj, OrbitingBlackHole):
                collision = collide_circles(
                    obj.position, obj.radius,
                    self.player.position, self.player.radius
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