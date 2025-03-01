from src.engine.objects import Object


class PredictionObject(Object):
    def __init__(self, position, velocity, mass=1, radius=1):
        super().__init__(position, velocity, mass)

        self.radius = radius

    def update(self, delta):
        self.motion_logic(delta)