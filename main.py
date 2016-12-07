import sys, pygame, math, random
import entities, systems, components, actions
from world import World
import worldgen
from point import Point
import time

if __name__ == "__main__":
    # Constants go here
    screen_width = 640
    screen_height = 480

    # Pygame init and setup
    pygame.init()
    screen = pygame.display.set_mode((screen_width,screen_height))
    pygame.display.set_caption("shit game")
    timer = pygame.time.Clock()

    # Create world with starting entities
    player = entities.player()
    world = World(player, screen)

    worldgen.generate(world)

    world.add_entity(player,Point(0,0,0))
    world.add_entity(entities.rock(),Point(3,0,0))
    world.add_entity(entities.rock(),Point(4,0,0))
    world.add_entity(entities.rock(),Point(4,1,0))
    world.add_entity(entities.moveright(),Point(-10,1,0))

    drawer = systems.DrawingSystem(screen, player)

    # Do an initial draw
    drawer.process(world)

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()

                now = time.time()

                # Player movement
                pt = world.find_pos(player)
                if event.key == pygame.K_KP1: # South west
                    world.player.give_action(actions.MoveAction(pt.x-1,pt.y+1))
                if event.key == pygame.K_KP2: # South
                    world.player.give_action(actions.MoveAction(pt.x,pt.y+1))
                if event.key == pygame.K_KP3: # South east
                    world.player.give_action(actions.MoveAction(pt.x+1,pt.y+1))
                if event.key == pygame.K_KP4: # West
                    world.player.give_action(actions.MoveAction(pt.x-1,pt.y))
                if event.key == pygame.K_KP6: # East
                    world.player.give_action(actions.MoveAction(pt.x+1,pt.y))
                if event.key == pygame.K_KP7: # North west
                    world.player.give_action(actions.MoveAction(pt.x-1,pt.y-1))
                if event.key == pygame.K_KP8: # North
                    world.player.give_action(actions.MoveAction(pt.x,pt.y-1))
                if event.key == pygame.K_KP9: # North east
                    world.player.give_action(actions.MoveAction(pt.x+1,pt.y-1))
                if event.key == pygame.K_KP5: # Wait
                    pass
                    #world.wait(2)

                # Step until player is ready

                world.step_until_ready()
                step = time.time()
                drawer.process(world)
                draw = time.time()

                print("Step(s) took " + str(round(step - now,3)*1000) + "ms")
                print("Draw took " + str(round(draw - step,3)*1000) + "ms")

        # Get delta time
        dt = timer.tick() * 0.001
        #pygame.time.wait(10)
