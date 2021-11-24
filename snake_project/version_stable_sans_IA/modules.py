import sys, time, pygame
from pygame.locals import *
from random import randint

class EnvSnake: 
    
    def __init__(self, start, world_size, is_human=True, is_trainable=False):

        # Configuration arguments
        self.is_human = is_human
        self.is_trainable = is_trainable

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
        self.world[self.food_y][self.food_x] = 5

    def reset(self): 
        """
            re-initialization of world and snake initial position
        """

        self.world = [[0 for _ in range(self.size_x)] for _ in range(self.size_y)] 
        self.world[self.start_y][self.start_x] = 2

    def show(self, surface): 
        """
            Using pygame module to represent a frame
            surface : pygame object
        """

        # Block Pixel Size
        bps = 20

        for i in range(self.size_x): 
            for j in range(self.size_y):

                current_block = self.world[j][i]

                # Snake head
                pygame.draw.rect(surface, (255, 255, 255), (self.snake_x*bps, self.snake_y*bps, bps, bps))

                # Snake body
                if current_block < 5 and current_block != 0:
                    pygame.draw.rect(surface, (255, 255, 255), (i*bps, j*bps, bps, bps)) 

                # Food 
                if current_block == 5:
                    pygame.draw.rect(surface, (0, 0, 255), (i*bps, j*bps, bps, bps))

    def is_finished(self): 
        """
            Basic test for win condition
        """

        if self.snake_lenght == self.snake_win_limit: 
            return True
        return False 

    def play(self, action): 
        """
            Snake is moving, no matters who is deciding, this method just updates the world
        """

        # Updating the body of snake
        self.world[self.snake_y][self.snake_x] = action

        # Computing next position for snake's head
        next_position_X = self.snake_x + self.actions[action-1][0]
        next_position_Y = self.snake_y + self.actions[action-1][1]

        ###
        ### Collisions with borders ?
        ###

        self.collisions = False

        # Snake out of range
        if next_position_X >= self.size_x or next_position_X < 0 or next_position_Y >= self.size_y or next_position_Y < 0: 
            self.collisions = True

        # Snake colide with himself ?
        elif self.collisions == False: 
            next_world_pos = self.world[next_position_Y][next_position_X]

            if next_world_pos < 5 and next_world_pos > 0: 
                self.collisions = True 
            
            # Snake can move, no obstacle detected
            else: 
                self.snake_x = next_position_X
                self.snake_y = next_position_Y


        ###
        ### Dealing with the snake's queue
        ###

        # If snake is eating, queue isn't changing but food had th respawn
        if next_position_X == self.food_x and next_position_Y == self.food_y:

            # Randomly choosen
            self.food_x = randint(0, self.size_x-1)
            self.food_y = randint(0, self.size_y-1)

            # putting food on the table
            self.world[self.food_y][self.food_x] = 5

            # snake lenght increase
            self.snake_lenght += 1 

        # If snake is not eating 
        else: 

            # Saving action 
            action_queue = self.world[self.snake_queue_y][self.snake_queue_x]

            # Last queue position becomes empty
            self.world[self.snake_queue_y][self.snake_queue_x] = 0

            # Moving the queue 
            self.snake_queue_x += self.actions[action_queue-1][0]
            self.snake_queue_y += self.actions[action_queue-1][1]




    def take_action(self): 
        """
            Human action OR Agent action 
            Return 1 2 3 4 as an action code
        """

        # Human controls 
        if self.is_human == True: 
            pressed_keys = pygame.key.get_pressed()

            # un changement ? 
            if pressed_keys[K_UP]: 
                self.save_action = 3
            elif pressed_keys[K_RIGHT]: 
                self.save_action = 2
            elif pressed_keys[K_DOWN]: 
                self.save_action = 1
            elif pressed_keys[K_LEFT]: 
                self.save_action = 4

            return self.save_action

        # Agent control needs IA training 
        # Not ready




