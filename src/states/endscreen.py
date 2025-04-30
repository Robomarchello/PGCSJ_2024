import pygame
from pygame.locals import *
import src.states as states
import src.engine.config as c
from src.engine import State
from src.engine.asset_manager import AssetManager
from src.engine.objects.decoration import Decoration
from src.engine.vfx.emitters import *
from src.engine.utils import calculate_gradient
from src.engine.camera import Camera
from src.engine.space import SpaceBackground


class StarEmitter(Emitter):
    def __init__(self, emit_rect):
        colls = (
        (255, 0, 0),
        (255, 255, 0),
        (0, 255, 0, 255),
        (148, 0, 211, 0)
        )
        gradient = calculate_gradient(
            colls,
            (0.0, 0.3, 0.65, 1.0),
            300
        )
        texture = AssetManager.images['particle'].convert_alpha()
        template = ParticleTemplate(
            angle_range=(0, 360),
            speed_range=(9, 9),
            life_range=(1.7, 1.7),
            scale_range=(1, 2),
            texture=texture,
            gradient=gradient,
            texture_rot_range=(-1, 1),
            velocity_change=0.98
        )
        super().__init__(template, texture, emit_rect, emitter_type=EmitterShape.STAR)


class FireworksEmitter(Emitter):
    def __init__(self, emit_rect, colls, intervals):
        gradient = calculate_gradient(
            colls,
            intervals,
            300
        )
        texture = AssetManager.images['particle1'].convert_alpha()
        template = ParticleTemplate(
            angle_range=(0, 360),
            speed_range=(4, 7),
            life_range=(2, 3),
            scale_range=(0.5, 2),
            texture=texture,
            gradient=gradient,
            texture_rot_range=(-1, 1),
            velocity_change=0.98
        )
        super().__init__(template, texture, emit_rect, emitter_type=EmitterShape.ELLIPSE)



class EndScreen(State):
    def __init__(self):
        super().__init__()
        star_rect = pygame.Rect(200, 200, 25, 25)

        self.space = SpaceBackground()
        
        star_emitter = StarEmitter(star_rect) 
        self.emitters = [star_emitter]
        self._init_emitters()

        self.duration = 0.75
        self.timer = self.duration

        self.text = Decoration((240, 200), 'final')

    def burst_update(self, delta):
        self.timer -= delta

        if self.timer < 0:
            emitter = random.choice(self.emitters)
            emitter.burst(150)
            emitter.emit_rect.center = (
                random.randint(200, 1165),
                random.randint(100, 668)
            )

            self.timer = self.duration

    def on_start(self):
        pass
    
    def on_exit(self):
        pass

    def draw(self, surface):
        self.space.draw(surface)

        for emitter in self.emitters:
            emitter.draw(surface)

        self.text.draw(surface)
        
    def update(self, delta):
        Camera.update(delta)
        self.space.update(delta)
        for emitter in self.emitters:
            emitter.update(delta)

        self.burst_update(delta)

        self.text.update(delta)
        Camera.focus = pygame.Vector2((1365 / 2, 768 / 2))

    def handle_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.manager.next_state = states.Menu()

        Camera.handle_event(event)

    def _init_emitters(self):
        fireworks_rect = pygame.Rect(200, 200, 15, 15)

        colls = (
        (255, 0, 0),
        (255, 255, 0),
        (0, 255, 0, 255),
        (148, 0, 211, 0)
        )
        intervals = (0.0, 0.3, 0.65, 1.0)
        emitter = FireworksEmitter(fireworks_rect, colls, intervals)
        self.emitters.append(emitter)

        colls = (
            (255, 0, 200),
            (255, 120, 220),
            (255, 120, 220, 0)
        )
        intervals = (0.0, 0.5, 1.0)
        self.emitters.append(FireworksEmitter(fireworks_rect, colls, intervals))

        # 🟢 Emerald → Lime → Transparent
        colls = (
            (0, 255, 0),
            (150, 255, 0),
            (150, 255, 0, 0)
        )
        intervals = (0.0, 0.8, 1.0)
        self.emitters.append(FireworksEmitter(fireworks_rect, colls, intervals))

        # 🔵 Indigo → Blue → Transparent
        colls = (
            (80, 0, 255),
            (100, 180, 255),
            (100, 180, 255, 0)
        )
        intervals = (0.0, 0.7, 1.0)
        self.emitters.append(FireworksEmitter(fireworks_rect, colls, intervals))
