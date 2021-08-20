# File: env.py
# Description: Building the environment-1 for the Mobile Robot to explore
# Agent - Mobile Robot
# Obstacles - 'road closed', 'trees', 'traffic lights', 'buildings'
# Environment: PyCharm and Anaconda environment
#
# MIT License
# Copyright (c) 2018 Valentyn N Sichkar
# github.com/sichkar-valentyn
#
# Reference to:
# Valentyn N Sichkar. Reinforcement Learning Algorithms for global path planning // GitHub platform. DOI: 10.5281/zenodo.1317899


# Importing libraries
import numpy as np  # To deal with data in form of matrices
import math 
import config

# # Setting the sizes for the environment
# pixels = 40   # pixels
# env_height = 9  # grid height
# env_width = 9  # grid width

# Global variable for dictionary with coordinates for the final route
a = {}


# Creating class for the environment
class Environment:
    def __init__(self,start,goal):
        self.action_space = ['up', 'down', 'left', 'right']
        self.n_actions = len(self.action_space)
        self.build_environment()
        self.start=start
        self.goal=goal
        self.coords=start

        # Dictionaries to draw the final route
        self.d = {}
        self.f = {}

        # Key for the dictionaries
        self.i = 0

        # Writing the final dictionary first time
        self.c = True

        # Showing the steps for longest found route
        self.longest = 0

        # Showing the steps for the shortest route
        self.shortest = 0

    # Function to build the environment
    def build_environment(self):
        #配置文件        
        self.con=config.Config()
        #环境的x范围
        self.x_range = eval(self.con.range['x'])
        #环境的y范围
        self.y_range = eval(self.con.range['y'])
        #环境的边界
        self.obs_boundary = eval(self.con.obs['bound'])
        #环境的矩形障碍
        self.obs_circle = eval(self.con.obs['cir'])
        #环境的圆形障碍
        self.obs_rectangle = eval(self.con.obs['rec'])



    # Function to reset the environment and start new Episode
    def reset(self):

        # Updating agent
        self.coords=self.start #将坐标置为起点

        # # Clearing the dictionary and the i
        self.d = {}
        self.i = 0

        # Return observation
        return self.coords

    # Function to get the next observation and reward by doing next step
    def step(self, action):
        # Current state of the agent
        state = self.coords
        base_action = [0,0]

        # Updating next state according to the action
        # Action 'up'
        if action == 0:
            if state[1]<self.obs_boundary[1][1]:
                base_action[1]+=1 
        # Action 'down'
        elif action == 1:
            if state[1]>1:
                base_action[1]-=1 
        # Action right
        elif action == 2:
            if state[0]<self.obs_boundary[1][2]:
                base_action[0]+=1 
        # Action left
        elif action == 3:
            if state[0]>1:
                base_action[0]-=1 

        # Moving the agent according to the action
        self.coords=(self.coords[0]+base_action[0],self.coords[1]+base_action[1])
        #self.canvas_widget.move(self.agent, base_action[0], base_action[1])

        # Writing in the dictionary coordinates of found route
        self.d[self.i] = self.coords

        # Updating next state
        next_state = self.d[self.i]

        # Updating key for the dictionary
        self.i += 1

        # Calculating the reward for the agent
        if next_state == self.goal:
            reward = 100
            done = True
            next_state = 'goal'

            # Filling the dictionary first time
            if self.c == True:
                for j in range(len(self.d)):
                    self.f[j] = self.d[j]
                self.c = False
                self.longest = len(self.d)
                self.shortest = len(self.d)

            # Checking if the currently found route is shorter
            if len(self.d) < len(self.f):
                # Saving the number of steps for the shortest route
                self.shortest = len(self.d)
                # Clearing the dictionary for the final route
                self.f = {}
                # Reassigning the dictionary
                for j in range(len(self.d)):
                    self.f[j] = self.d[j]

            # Saving the number of steps for the longest route
            if len(self.d) > self.longest:
                self.longest = len(self.d)

        elif self.is_collision(next_state):
            reward = -100
            done = True
            next_state = 'obstacle'

            # Clearing the dictionary and the i
            self.d = {}
            self.i = 0

        else:
            reward = -1
            done = False

        return next_state, reward, done

    # Function to refresh the environment
    def render(self):
        #time.sleep(0.03)
        self.update()

    # Function to show the found route
    def final(self):
        # Deleting the agent at the end
       # self.canvas_widget.delete(self.agent)

        # Showing the number of steps
        print('The shortest route:', self.shortest)
        print('The longest route:', self.longest)

        # Creating initial point
        # origin = np.array([20, 20])
        # self.initial_point = self.canvas_widget.create_oval(
        #     origin[0] - 5, origin[1] - 5,
        #     origin[0] + 5, origin[1] + 5,
        #     fill='blue', outline='blue')

        # Filling the route
        for j in range(len(self.f)):
            # Showing the coordinates of the final route
            print(self.f[j])
            #self.track = self.canvas_widget.create_oval(
                #self.f[j][0] + origin[0] - 5, self.f[j][1] + origin[0] - 5,
                #self.f[j][0] + origin[0] + 5, self.f[j][1] + origin[0] + 5,
                #fill='blue', outline='blue')
            # Writing the final route in the global variable a
            a[j] = self.f[j]
        
    def is_collision(self,state):
        delta = 0.5
        for (x, y, r) in self.obs_circle:
            if math.hypot(state[0] - x, state[1] - y) <= r + delta:
                return True

        for (x, y, w, h) in self.obs_rectangle:
            if 0 <= state[0] - (x - delta) <= w + 2 * delta \
                    and 0 <= state[1] - (y - delta) <= h + 2 * delta:
                return True

        for (x, y, w, h) in self.obs_boundary:
            if 0 <= state[0] - (x - delta) <= w + 2 * delta \
                    and 0 <= state[1] - (y - delta) <= h + 2 * delta:
                return True

        return False



# Returning the final dictionary with route coordinates
# Then it will be used in agent_brain.py
def final_states():
    return a


# This we need to debug the environment
# If we want to run and see the environment without running full algorithm
if __name__ == '__main__':
    env = Environment()
    env.mainloop()
