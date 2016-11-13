import components, systems
from threading import Timer
import time
from collections import defaultdict

class World:
    def __init__(self, entities, player, screen):
        self.entities = entities
        self.player = player
        self.systems = [
            systems.MovementSystem(),
            #systems.DrawingSystem(screen, player),
        ]

    # Time handling functions
    def step_until_ready(self):
        char = self.player.get(components.Character)
        while True:
            self.step()
            if char.ready:
                break

    def wait(self, steps):
        while steps > 0:
            self.step()
            steps -= 1

    def step(self):
        for sys in self.systems:
            sys.process(self)

        for e in self.entities:
            e.clear_actions()

    # Entity finding / data gathering functions
    def check_spot(self, x, y, z):
        result = []
        for e in self.entities:
            t = e.get(components.Transform)
            if t != None:
                if t.x == x and t.y == y and t.z == z:
                    result.append(e)
        return result

    def get_spot_space(self, x, y, z):
        space = 1
        ents = self.check_spot(x,y,z)
        for e in ents:
            s = e.get(components.Solid)
            if s != None:
                space -= s.volume
        return space
