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
        if self.camera_target != None:
            pos = world.find_pos(self.camera_target)
            self.camera_pos = pos

        self.screen.fill((0,0,0))

        tw = self.tilew
        th = self.tileh

        # Find the max amount of tiles that fit the with and height of the screen
        # So we can calculate the center of it
        screentiles_x = self.screen.get_width() / tw
        screentiles_y = self.screen.get_height() / th

        # Calculate 'borders' to draw within
        left = math.floor(self.camera_pos.x - screentiles_x/2)
        right = math.floor(self.camera_pos.x + screentiles_x/2)
        top = math.floor(self.camera_pos.y - screentiles_y/2)
        bottom = math.floor(self.camera_pos.y + screentiles_y/2)

        for x in range(left,right):
            for y in range(top,bottom):
                # print(str(x) + " - " + str(y))
                #gridslice = sorted(world.search_slice(x,y),key=lambda e: world.find_pos(e).z)
                gridslice = world.search_slice(x,y,self.camera_pos.z,2)
                if len(gridslice) > 0:
                    e = gridslice[0]
                    drawable = e.get(components.Drawable)
                    if drawable != None:
                        # Find the tile to use based on the ASCII value of the char to draw
                        src_x = ord(drawable.char) % 16
                        src_y = math.floor(ord(drawable.char) / 16)

                        rect = pygame.Rect(
                        screentiles_x * tw / 2 - self.camera_pos.x * tw + x * tw,
                        screentiles_y * th / 2 - self.camera_pos.y * th + y * th,
                        tw,
                        th)

                        self.tileset.set_palette_at(1,drawable.color)

                        if world.find_pos(e).z == self.camera_pos.z:
                            # Draw background color
                            pygame.draw.rect(self.screen, drawable.bgcolor, rect)
                        # Draw tile
                        self.screen.blit(
                        self.tileset,
                        (rect.x,rect.y),
                        pygame.Rect(src_x * tw, src_y * th, tw, th)
                        )
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

            solid_comp = entity.get(components.Solid)
            if solid_comp != None:
                space_left = world.get_spot_space(pos)
                if space_left < solid_comp.volume:
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
