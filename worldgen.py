import entities
from point import Point

def generate(world):
    i = 0
    size = 50
    for z in range(0,10):
        for x in range(-size,size):
            for y in range(-size,size):
                if z == 0:
                    entity_to_add = entities.grass()
                elif z == 1:
                    entity_to_add = entities.dirt()
                else:
                    entity_to_add = entities.rock()
                world.add_entity(entity_to_add,Point(x,y,z))
                i += 1
    print("created " + str(i) + " walls")
