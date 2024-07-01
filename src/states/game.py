import pygame
from src.engine import State, Debug, AssetManager
from src.engine.constants import *
from src.engine.player import Player, Controller
from src.engine.objects import PhysicsHandler, BlackHole, Asteroid


class Game(State):
    def __init__(self):
        super().__init__()
        self.surface = pygame.Surface(SCREENSIZE)

        self.player = Player()
        rect = pygame.Rect(0, 0, 75, 75)
        rect.center = self.player.position
        
        objects = []
        #objects.append(BlackHole((250, 384), 50))
        objects.append(BlackHole((500, 384), 50))
        obstacles = []
        obstacles.append(Asteroid((500, 280), pygame.Vector2(4.3, 0), 20, 15))
        obstacles.append(Asteroid((500, 488), pygame.Vector2(-4.3, 0), 20, 15))
        self.physics_handler = PhysicsHandler(self.player, objects, obstacles)

        self.controller = Controller(self.player, rect, self.physics_handler)

    def on_start(self):
        print('start')
    
    def on_exit(self):
        print('exit')

    def draw(self):
        self.surface.fill((0, 0, 0))

        self.physics_handler.draw(self.surface)

        self.controller.draw(self.surface)
        self.player.draw(self.surface)

        Debug.add_text(self.manager.clock.get_fps())

    def update(self, delta):
        self.player.update(delta)
        self.controller.update(delta)
        self.physics_handler.update(delta)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.manager.next_state = NewNextState()

        self.controller.handle_event(event)


class NewNextState(State):
    def __init__(self):
        super().__init__()
        self.surface = pygame.Surface(SCREENSIZE)

        self.image = AssetManager.images['fff']

    def on_start(self):
        print('start')
    
    def on_exit(self):
        print('*exit*')

    def draw(self):
        self.surface.fill((0, 0, 255))

        self.surface.blit(self.image, (0, 0))

        Debug.add_text(self.manager.clock.get_fps())

    def update(self, delta):
        pass

    def handle_event(self, event):
        pass
