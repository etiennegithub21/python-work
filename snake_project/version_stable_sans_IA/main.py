import sys, time, pygame
from pygame.locals import *
from modules import *

###
### MAIN CODE
###

# Setting our environment
environement = EnvSnake((2,2), (25,25), is_human=True, is_trainable=False)

# Setting pygame 
pygame.init()
surface = pygame.display.set_mode((500,500))

# Frame Per Seconds
FPS = pygame.time.Clock()

# Game Loop 
while True : 

    pygame.display.update()

    # Collision ?
    if environement.collisions == True: 
        print("You lose !")
        sys.exit()

    # TAKE ACTION 
    action = environement.take_action()

    # UPDATE
    if environement.is_finished() == False: 
        environement.play(action)

    # Win ?
    else: 
        print("You won !")
        sys.exit()

    # DISPLAY
    surface.fill((0, 0, 0))
    environement.show(surface)

    # EVENTS
    for event in pygame.event.get():

        # On appuie sur le boutton quitter
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    FPS.tick(10)
