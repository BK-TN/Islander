import components, actions
import pygame
import math
from collections import defaultdict

class DrawingSystem:
    def __init__(self, screen, camera_target):
        self.screen = screen
        self.camera_x = 0
        self.camera_y = 0
        self.camera_z = 0
        self.camera_target = camera_target
        self.tileset = pygame.image.load("tileset.png") #12x16
        self.tileset.set_colorkey((0,0,0))
        self.tilew = 12
        self.tileh = 16
    def process(self, world):
        if self.camera_target != None:
            t = self.camera_target.get(components.Transform)
            if t != None:
                self.camera_x = t.x
                self.camera_y = t.y
                self.camera_z = t.z

        self.screen.fill((0,0,0))

        tw = self.tilew
        th = self.tileh

        # Find the max amount of tiles that fit the with and height of the screen
        # So we can calculate the center of it
        screentiles_x = self.screen.get_width() / tw
        screentiles_y = self.screen.get_height() / th

        # Calculate 'borders' to draw within
        left = math.floor(self.camera_x - screentiles_x/2)
        right = math.floor(self.camera_x + screentiles_x/2)
        top = math.floor(self.camera_y - screentiles_y/2)
        bottom = math.floor(self.camera_y + screentiles_y/2)

        # Sort all entites into a grid in order to quickly fetch each slice
        grid = defaultdict(list)
        for e in world.entities:
            t = e.get(components.Transform)
            if t != None and t.x > left and t.x < right and t.y > top and t.y < bottom:
                grid[(t.x,t.y)].append(e)

        for x in range(left,right):
            for y in range(top,bottom):
                # print(str(x) + " - " + str(y))
                gridslice = sorted(grid[(x,y)],key=lambda e: e.get(components.Transform).z)
                if len(gridslice) > 0:
                    e = gridslice[0]
                    transform = e.get(components.Transform)
                    drawable = e.get(components.Drawable)
                    if drawable != None and transform != None:
                        # Find the tile to use based on the ASCII value of the char to draw
                        src_x = ord(drawable.char) % 16
                        src_y = math.floor(ord(drawable.char) / 16)

                        rect = pygame.Rect(
                        screentiles_x * tw / 2 - self.camera_x * tw + x * tw,
                        screentiles_y * th / 2 - self.camera_y * th + y * th,
                        tw,
                        th)

                        self.tileset.set_palette_at(1,drawable.color)

                        if transform.z == self.camera_z:
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
        pass
    def process(self, world):
        def try_move(world, solid_comp, transform_comp, x, y, z):
            can_move = True
            if solid_comp != None:
                space_left = world.get_spot_space(x,y,z)
                if space_left < solid_comp.volume:
                    can_move = False

            if can_move:
                transform_comp.x = x
                transform_comp.y = y
                transform_comp.z = z

        for e in world.entities:
            character = e.get(components.Character)
            transform = e.get(components.Transform)
            moveright = e.get(components.MoveRight)
            solid = e.get(components.Solid)
            if character != None and transform != None:
                movement = e.get_actions(actions.MoveAction)
                for mov in movement:
                    try_move(world, solid, transform, mov.xtarget, mov.ytarget, 0) #TODO: add a.ztarget

            if moveright != None and transform != None:
                try_move(world, solid, transform, transform.x + 1, transform.y, transform.z)
