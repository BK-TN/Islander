import entities
from point import Point

def generate(world):
    i = 0
    size = 50
    for x in range(-size,size):
        for y in range(-size,size):
            world.add_entity(entities.wall(),Point(x,y,1))
            i += 1
    print("created " + str(i) + " walls")
