import components, systems
from threading import Timer
import time
from collections import defaultdict
import itertools
from point import Point

class World:
    def __init__(self, player, screen):
        self.grid = defaultdict(list) # Entities in grid format
        self.entities = [] # Entities in list format
        self.positions = {} # The positions of entities are also stored per-entity
        self.player = player
        self.systems = [
            systems.MovementSystem(),
            #systems.DrawingSystem(screen, player),
        ]

    # Entity addition/removal/change functions
    def add_entity(self, entity, pos):
        self.grid[pos].append(entity)
        self.entities.append(entity)
        self.positions[entity] = pos

    def remove_entity(self, entity):
        pass

    def find_pos(self, entity):
        return self.positions[entity]

    def move_entity(self, entity, newPos):
        current_cell = self.grid[self.find_pos(entity)]
        current_cell.remove(entity)
        new_cell = self.grid[newPos]
        new_cell.append(entity)
        self.positions[entity] = newPos

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

    def check_spot(self, pos):
        return self.grid[pos]

    def search_slice(self, x, y, z_center, z_range):
        results = []
        for z in range(z_center - z_range, z_center + z_range):
            results += self.check_spot(Point(x,y,z))
        return results

    def get_spot_space(self, pos):
        space = 1
        ents = self.check_spot(pos)
        for e in ents:
            s = e.get(components.Solid)
            if s != None:
                space -= s.volume
        return space
