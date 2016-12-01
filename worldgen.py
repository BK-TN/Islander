import entities
import random
import math
from point import Point

def generate_heightmap(size):
    hmap = [[10 for x in range(-size,size)] for y in range(-size,size)]

    for i in range(16):
        radius = random.randint(8, int(size / 2))
        xpos = random.randint(-size + radius, size - radius)
        ypos = random.randint(-size + radius, size - radius)

        for x in range(xpos - radius, xpos + radius):
            for y in range(ypos - radius, ypos + radius):
                dx = (xpos - x) ** 2
                dy = (ypos - y) ** 2
                disttocenter = math.sqrt(dx+dy)
                if x > -size and x < size and y > -size and y < size:
                    depth = -int(1 - (disttocenter / radius) * 3)
                    if depth < 1:
                        hmap[x][y] = depth
    return hmap


def generate(world):
    i = 0
    size = 50
    random.seed()

    hmap = generate_heightmap(size)

    for x in range(-size,size):
        for y in range(-size,size):
            for z in range(0,5):
                h = hmap[x][y]
                if z < h:
                    entity_to_add = entities.water()
                elif z == h:
                    entity_to_add = entities.grass()
                elif z == h+1:
                    entity_to_add = entities.dirt()
                else:
                    entity_to_add = entities.rock()
                world.add_entity(entity_to_add,Point(x,y,z))
                i += 1
    print("created " + str(i) + " walls")
