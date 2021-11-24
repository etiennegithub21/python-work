import sys, time, pygame
from pygame import display
from pygame.locals import *
from modules import *

def jeu(is_human, is_trainable):

    ###
    ### MAIN CODE
    ###

    # Setting our environment
    environement = EnvSnake((2,2), (25,25), is_human, is_trainable)

    # Setting pygame 
    pygame.init()
    surface = pygame.display.set_mode((500,500))
    pygame.display.set_caption("Snake")

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

        font = pygame.font.SysFont("Helvetica", 15)
        text = font.render("Score : " + str(environement.snake_length * 10 - 10), True, (255, 255, 255))
        surface.blit(text, (420,480))

        # EVENTS
        for event in pygame.event.get():

            # On appuie sur le boutton quitter
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        FPS.tick(10)

if __name__ == "__main__" :
    jeu(True, False)