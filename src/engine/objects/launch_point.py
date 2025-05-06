import pygame
from src.engine.config import SPEED_FACTOR
from src.engine.utils import collide_circles
from src.engine.objects import Object
from src.engine.camera import Camera
from src.engine.physics_handler import PhysicsHandler


class LaunchPoint(Object):
    def __init__(self, position, radius, solution_vector, player, controller):
        super().__init__(position)

        self.radius = radius

        self.player = player
        self.controller = controller
        
        self.used = False

        self.solution_vector = solution_vector
        self.solution_revealed = True
        self.trajectory = []

    def set_solution_trajectory(self, physics_handler: PhysicsHandler):
        self.trajectory = physics_handler.predict_player(
            time=0.016,
            position=self.player.position,
            start_vel=self.solution_vector,
            mass=self.player.mass,
            radius=self.player.radius,
            count=51
        )[::3]

    def update(self, delta):
        collision = collide_circles(
            self.position, self.radius,
            self.player.position, self.player.radius
        )
        if collision and not self.used:
            self.player.freeze = True

            self.controller.launch_point = self

            pull_force = self.pulling_force(self.player.position)
            self.player.position += pull_force * delta * SPEED_FACTOR

    def pulling_force(self, position: pygame.Vector2): 
        difference = self.position - position
        
        return difference * 0.18

    def draw(self, surface):
        pygame.draw.circle(surface, 'grey', self.cam_pos, self.radius * Camera.scale_factor)

        self.draw_trajectory(surface)

    def draw_trajectory(self, surface):
        if self.solution_revealed:
            for position in self.trajectory:
                cam_pos = Camera.displace_position(position)
                pygame.draw.circle(surface, 'grey', cam_pos, 3)

    def serialize(self):
        return {
            'type': 'LaunchPoint',
            'position': tuple(self.position),
            'radius': self.radius,
            'solution_vector': self.solution_vector
        }

    @classmethod
    def deserialize(cls, data: dict, player, controller):
        return cls(
            position=data['position'],
            radius=data['radius'],
            solution_vector=data['solution_vector'],
            player=player,
            controller=controller
            )