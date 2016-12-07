import components, actions
import pygame
import math
from collections import defaultdict
from point import Point

class DrawingSystem:
    def __init__(self, screen, camera_target):
        self.screen = screen
        self.camera_pos = Point(0,0,0)
        self.camera_target = camera_target
        self.tileset = pygame.image.load("tileset.png") #12x16
        self.tileset.set_colorkey((0,0,0))
        self.tilew = 12
        self.tileh = 16
        self.entities = []
    def check_entity(self, entity):
        pass
    def process(self, world):
        def draw(drawable, draw_background):
            # Find the tile to use based on the ASCII value of the char to draw
            src_x = ord(drawable.char) % 16
            src_y = math.floor(ord(drawable.char) / 16)
            # Create the rect this tile should be drawn in
            rect = pygame.Rect(
            (screentiles_x / 2 - self.camera_pos.x + x) * self.tilew,
            (screentiles_y / 2 - self.camera_pos.y + y) * self.tileh,
            self.tilew,
            self.tileh)
            # Set the tile color by changing the tileset's palette (Which is really fast)
            self.tileset.set_palette_at(1,drawable.color)
            if draw_background:
                pygame.draw.rect(self.screen, drawable.bgcolor, rect)
            # Draw tile
            self.screen.blit(
            self.tileset,
            (rect.x,rect.y),
            pygame.Rect(src_x * self.tilew, src_y * self.tileh, self.tilew, self.tileh)
            )

        if self.camera_target != None:
            pos = world.find_pos(self.camera_target)
            self.camera_pos = pos

        self.screen.fill((0,0,0))

        # Find the max amount of tiles that fit the with and height of the screen
        # So we can calculate the center of it
        screentiles_x = self.screen.get_width() / self.tilew
        screentiles_y = self.screen.get_height() / self.tileh

        # Calculate 'borders' to draw within
        left = math.floor(self.camera_pos.x - screentiles_x/2)
        right = math.floor(self.camera_pos.x + screentiles_x/2)
        top = math.floor(self.camera_pos.y - screentiles_y/2)
        bottom = math.floor(self.camera_pos.y + screentiles_y/2)

        for x in range(left,right):
            for y in range(top,bottom):
                #gridslice = sorted(world.search_slice(x,y),key=lambda e: world.find_pos(e).z)
                drawn = False
                for z in range(self.camera_pos.z,10):
                    if drawn: break
                    entities_on_pos = world.check_spot(Point(x,y,z))
                    drawables = [d for d in (e.get(components.Drawable) for e in entities_on_pos) if d != None]
                    if len(drawables) > 0:
                        drawables = sorted(drawables, key=lambda d: d.depth)
                        draw(drawables[0], z == self.camera_pos.z)
                        drawn = True

        pygame.display.flip()

class MovementSystem:
    def __init__(self):
        self.entities = []
    def check_entity(self, entity):
        if entity.has(components.Character) or entity.has(components.MoveRight):
            self.entities.append(entity)
    def process(self, world):
        def try_move(world, entity, pos):
            can_move = True

            physical_comp = entity.get(components.Physical)
            if physical_comp != None:
                space_left = world.get_spot_space(pos)
                if space_left < physical_comp.volume:
                    can_move = False

            if can_move:
                world.move_entity(entity, pos)

        for e in self.entities:
            character = e.get(components.Character)
            moveright = e.get(components.MoveRight)
            if character != None:
                movement = e.get_actions(actions.MoveAction)
                for mov in movement:
                    try_move(world, e, Point(mov.xtarget, mov.ytarget, 0)) #TODO: add a.ztarget

            if moveright != None:
                pos = world.find_pos(e)
                try_move(world, e, Point(pos.x + 1, pos.y, pos.z))

class PhysicsSystem:
    def __init__(self):
        self.entities = []
    def check_entity(self, entity):
        if entity.has(components.Physical):
            self.entities.append(entity)
    def process(self, world):
        for e in self.entities:
            phys = e.get(components.Physical)
            pos = world.find_pos(e)
            pos_below = Point(pos.x,pos.y,pos.z+1)
            space_below = world.get_spot_space(pos_below)
            if space_below < phys.volume:
                world.move_entity(e,pos_below)
