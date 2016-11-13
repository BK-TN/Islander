import entities

def generate(world):
    i = 0
    size = 50
    for x in range(-size,size):
        for y in range(-size,size):
            print(str(x) + " - " + str(y))
            world.entities.append(entities.wall(x,y,1))
            i += 1
    print("created " + str(i) + " walls")
