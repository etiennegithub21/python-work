import sys, time, pygame
from pygame.locals import *
from modules import *
import pickle
import math

ALPHA, GAMMA, EPS = 0.1, 0.9, 0.4
    
def QTable(env): 
    """
        initialization of a QTable 
        STATES : DeltaX, DeltaY, Lenght
        Distance from Food and snake lenght
        6 500 000 different states
        4 actions for each states 
        26 000 000 different actions
    """

    # Q Table as dictionnary 
    QT = {}

    #matches_key = {}

    for i in range(0, env.size_x): 
        for j in range(0, env.size_y): 
            for k in range(0, env.size_y):
                for l in range(0, env.size_y):

                    # Low collision risk 
                    text = str(i)+":"+str(j)+":"+str(k)+":"+str(l)
                    st = hash(text)

                    # High space needed
                    QT[st] = [0, 0, 0, 0]
    return QT

def value_fct(env, action): 
    """
        Return state and reward
    """

    Reward = 0

    newX, newY = env.next_pos(action)

    deltaX = newX - env.food_x
    deltaY = newY - env.food_y

    if deltaX == 0 and deltaY == 0:
        Reward = 1

    if env.is_finished((newX,newY)) == True: 
        Reward = -1
   
    text = str(newX)+":"+str(newY)+":"+str(env.food_x)+":"+str(env.food_y)
    state = hash(text) 

    return state, Reward

def mainExec(env):
    """
        adapter l'execution du code en fonction des parametres d'execution
    """ 

    global ALPHA, GAMMA, EPS

    # Game loop for classical visual execution
    if env.display == True:

        # Setting pygame 
        pygame.init()
        surface = pygame.display.set_mode((500,500))

        # Frame Per Seconds
        FPS = pygame.time.Clock()

        # Bool 
        finished = False

        # Initial action
        # Useful for the agent computing
        action = env.save_action

        # Game Loop 
        while True : 

            pygame.display.update()

            # STILL PLAYING ?
            if finished == True: 
                print("HIGH SCORE : {}".format(env.snake_lenght))
                sys.exit()
            else:
                # TAKE ACTION 
                if env.is_human == True:
                    action = env.take_action()
                else: 
                    st,r = value_fct(env, action)
                    action = env.take_action(st, QTab)

                # COMPUTING NEXT POSITION   
                next_position = env.next_pos(action)

                # Playing if there is no problems
                if env.is_finished(next_position)[0] == True: 
                    print(env.is_finished(next_position)[1])
                    finished = True
                else:
                    # UPDATE
                    env.play(next_position, action)

                # DISPLAY
                surface.fill((0, 0, 0))
                env.show(surface)

            # EVENTS
            for event in pygame.event.get():

                # On appuie sur le boutton quitter
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            FPS.tick(5)
    
    # Training AI
    elif env.is_human == False and env.is_trainable == True: 
        print("--- Train process launched --- ")

        # Reseting environement world
        env.reset() 

        for k in range(10000): 

            env.reset() 
            st = hash("{}:{}:{}:{}".format(env.snake_x,env.snake_y, env.food_x, env.food_y))

            # initilization
            quit = False

            while quit == False:

                # Chosing action by epsilon greedy process
                at = env.take_action(st, QTab, EPS)

                next_position = env.next_pos(at)
                quit = env.is_finished(next_position)[0]
                
                if quit != True:
                    stp1, r = value_fct(env,at)

                    atp1 = env.take_action(stp1, QTab, 0.0)

                    QTab[st][at] = QTab[st][at] + ALPHA*(r + GAMMA*QTab[stp1][atp1] - QTab[st][at])

                    st = stp1

                    env.play(next_position, at)


    











###
### MAIN CODE
###

# Training

environement = EnvSnake((2,2), (5,5), is_human=False, is_trainable=True, display=False)

QTab = QTable(environement)

# TRAIN
mainExec(environement)

# PLAY
environement.reset()
environement.is_trainable = False
environement.display = True
mainExec(environement)



