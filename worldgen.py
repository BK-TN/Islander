import entities
from point import Point

def generate(world):
    i = 0
    size = 50
    for z in range(1,10):
        for x in range(-size,size):
            for y in range(-size,size):
                if z == 1:
                    world.add_entity(entities.dirt(),Point(x,y,z))
                else:
                    world.add_entity(entities.rock(),Point(x,y,z))
                i += 1
    print("created " + str(i) + " walls")
