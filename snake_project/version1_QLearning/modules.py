import sys, time, pygame
from pygame.locals import *
from random import *
import numpy as np

class EnvSnake: 
    
    def __init__(self, start, world_size, is_human=True, is_trainable=False, display = True):

        # Configuration arguments
        self.is_human = is_human
        self.is_trainable = is_trainable
        self.display = display

        # Actions 1 2 3 4 <-> D R U L
        self.actions = [
            [0,1],
            [1,0],
            [0,-1],
            [-1,0]
        ]  

        # Snake size
        self.snake_lenght = 1 

        # Food position [init : no food]
        self.food_x = randint(0, world_size[0]-1)
        self.food_y = randint(0, world_size[1]-1)

        # Snake win limit 
        # max should be world_size_X times world_size_Y
        self.snake_win_limit = 50

        # Start point for snake player & queue position
        self.snake_x = start[0]
        self.snake_y = start[1] 

        self.snake_queue_x = start[0]
        self.snake_queue_y = start[1]

        self.start_x = start[0]
        self.start_y = start[1]

        self.save_action = 2

        # Collision callback 
        self.collisions = False

        # World Size
        self.size_x = world_size[0]
        self.size_y = world_size[1] 

        # World Init
        # each case in world represent the action taken by the snake (1,2,3,4) [init : right]
        # 0 if it's empty
        # 5 if it's food
        self.world = [[0 for _ in range(self.size_x)] for _ in range(self.size_y)] 
        self.world[self.snake_y][self.snake_x] = 2

    def reset(self): 
        """
            re-initialization of world and snake initial position
        """

        self.world = [[0 for _ in range(self.size_x)] for _ in range(self.size_y)] 
        self.world[self.start_y][self.start_x] = 2

        self.snake_x = self.start_x
        self.snake_y = self.start_y

        self.snake_queue_x = self.start_x
        self.snake_queue_y = self.start_y

        self.snake_lenght = 1

        self.collisions = False

        self.save_action = 2

    def show(self, surface): 
        """
            Using pygame module to represent a frame
            surface : pygame object
        """

        # Block Pixel Size
        bps = 100

        for i in range(self.size_x): 
            for j in range(self.size_y):

                current_block = self.world[j][i]

                # Snake head
                pygame.draw.rect(surface, (255, 255, 255), (self.snake_x*bps, self.snake_y*bps, bps, bps))

                # Snake body
                if current_block < 5 and current_block != 0:
                    pygame.draw.rect(surface, (255, 255, 255), (i*bps, j*bps, bps, bps)) 

                # Food 
                pygame.draw.rect(surface, (0, 0, 255), (self.food_x*bps, self.food_y*bps, bps, bps))

    def is_finished(self, next_pos=(0,0)): 
        """
            Basic test for win condition
            default (0,0)
        """

        # Next position
        x,y = next_pos[0], next_pos[1]

        # Test : WIN, COLLIDE
        if self.snake_lenght == self.snake_win_limit: 
            return True, "win"
        
        if x < 0 or x >= self.size_x or y < 0 or y >= self.size_y:
            return True, "out of board"

        world_pos = self.world[y][x]
        if world_pos > 0 and world_pos < 5: 
            return False, "dont eat yourself"

        return False, "nope"

    def next_pos(self, action):
        """
            Return the next position
        """

        # Computing next position for snake's head
        next_position_X = self.snake_x + self.actions[action][0]
        next_position_Y = self.snake_y + self.actions[action][1]

        return (next_position_X, next_position_Y)

    def play(self, next_pos, action): 
        """
            Snake is moving, no matters who is deciding, this method just updates the world
        """

        # Updating the body of snake
        self.world[self.snake_y][self.snake_x] = action

        # Update coordonates
        self.snake_x = next_pos[0]
        self.snake_y = next_pos[1]

        # If snake is eating, queue isn't changing but food had th respawn
        if next_pos[0] == self.food_x and next_pos[1] == self.food_y:

            nocolide = False

            # Do not place food on the snake
            while nocolide == False:

                # Randomly choosen
                self.food_x = randint(1, self.size_x-2)
                self.food_y = randint(1, self.size_y-2)

                if self.world[self.food_y][self.food_x] == 0:
                    nocolide = True

            # snake lenght increase
            self.snake_lenght += 1 

        # If snake is not eating 
        else: 

            # Saving action 
            action_queue = self.world[self.snake_queue_y][self.snake_queue_x]

            # Last queue position becomes empty
            self.world[self.snake_queue_y][self.snake_queue_x] = 0

            # Moving the queue 
            try:
                self.snake_queue_x += self.actions[action_queue][0]
                self.snake_queue_y += self.actions[action_queue][1]
            except: 
                print(action_queue)

    def take_action(self, *args): 
        """
            Human action OR Agent action 
            Return 1 2 3 4 as an action code
            [ *args = st, Q, eps for AI case ]
        """

        # Human controls 
        if self.is_human == True: 
            pressed_keys = pygame.key.get_pressed()

            # un changement ? 
            if pressed_keys[K_UP]: 
                self.save_action = 2
            elif pressed_keys[K_RIGHT]: 
                self.save_action = 1
            elif pressed_keys[K_DOWN]: 
                self.save_action = 0
            elif pressed_keys[K_LEFT]: 
                self.save_action = 3

            return self.save_action

        # Follow QTable
        elif self.is_human == False and self.is_trainable == False: 
            st, Q = args 
            action = np.argmax(Q[st])
            return action

        # Agent control needs IA training 
        elif self.is_human == False and self.is_trainable == True:
            st, Q, eps = args[0], args[1], args[2]

            # Take an action
            if uniform(0, 1) < eps:
                action = randint(0, 3)

            else: # Or greedy action 
                action = np.argmax(Q[st])
                
            # on ajuste le resultat grace à une politique
            return action


        




