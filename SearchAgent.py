import random
import math
from environment import Agent, Environment
from simulator import Simulator
import sys
from searchUtils import searchUtils
import numpy as np

class SearchAgent(Agent):
    """ An agent that drives in the Smartcab world.
        This is the object you will be modifying. """ 

    def __init__(self, env,location=None):
        super(SearchAgent, self).__init__(env)     # Set the agent in the evironment 
        self.valid_actions = self.env.valid_actions  # The set of valid actions
        self.action_sequence=[]
        self.searchutil = searchUtils(env)

    def choose_action(self):
        """ The choose_action function is called when the agent is asked to choose
            which action to take next"""

        # Set the agent state and default action
        action=None
        if len(self.action_sequence) >=1:
            action = self.action_sequence[0] 
        if len(self.action_sequence) >=2:
            self.action_sequence=self.action_sequence[1:]
        else:
            self.action_sequence=[]
        return action

    def drive(self,goalstates,inputs):
        """Write your algorithm for self driving car"""
        #initialise a open list to store all children        
        openList = []
        
        #initialise a list to store the best action
        action_sequence=[]
        print(self.state)
        #loop through all possible valid actions
        for a in self.valid_actions:
            #obtain new state by applying valid action to current state
            newstate = self.env.applyAction(self,self.state,a)
            
            #Heuristic function(straight line distance from newstate location to goal lane)
            #3 is multiplied to make sure forward 3-x gets the highest preference followed by forward and then left,right
            h=3*(goalstates[0]['location'][1]-newstate['location'][1])
            
            #g function(no of steps taken to move from current state to new state)
            g=np.abs(newstate['location'][1]-self.state['location'][1])+np.abs(newstate['location'][0]-self.state['location'][0])
            
            #f(total of h and g)
            f=h+g
            
            #each newstate is inserted in priority queue as per their f value
            openList=self.searchutil.insertStateInPriorityQueue(openList,newstate,f)
        
        #obtain the action taken to move from current state to state with lowest f value
        action_sequence.append(self.env.getAction(self.state,openList[0][0]))
        
        return action_sequence       



    def update(self):
        """ The update function is called when a time step is completed in the 
            environment for a given trial. This function will build the agent
            state, choose an action, receive a reward, and learn if enabled. """
        startstate = self.state
        goalstates =self.env.getGoalStates()
        inputs = self.env.sense(self)
        self.action_sequence = self.drive(goalstates,inputs)
        action = self.choose_action()  # Choose an action
        self.state = self.env.act(self,action)        
        return
        

def run(filename):
    """ Driving function for running the simulation. 
        Press ESC to close the simulation, or [SPACE] to pause the simulation. """

    env = Environment(config_file=filename,fixmovement=False)
    
    agent = env.create_agent(SearchAgent)
    env.set_primary_agent(agent)
    
    ##############
    # Create the simulation
    # Flags:
    #   update_delay - continuous time (in seconds) between actions, default is 2.0 seconds
    #   display      - set to False to disable the GUI if PyGame is enabled
    sim = Simulator(env, update_delay=2)
    
    ##############
    # Run the simulator
    ##############
    sim.run()


if __name__ == '__main__':
    run(sys.argv[1])
