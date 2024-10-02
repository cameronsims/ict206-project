# road.py - Defines important classes to the system
#
# Author: Cameron Sims
# Date: 06/08/2024
#

from enum import Enum

import random
import math

#
# Connection Class
# - Defines a connection between at most 4 roads
#

class Connection:
    # The ID of the connection (-1 is an illegal ID)
    id = -1
    
    # What the connection connects to (MUST BE ROADS)
    connections = set()
    
    # This is the crash index (how likely it is to crash in this intersection)
    # 0.0 - 100.0
    crash = 0.0
    
    # This is the amount of deaths that have occured on this road 
    deaths = 0
    
    # This is the amount of times the road has been crossed
    crossed = 0
    
    # This is the amount of times the road has been targeted 
    targeted = 0
    
    # Constructor
    def __init__(self, id, crash, connections):
        # Set the ID
        self.id = id
        self.crash = crash
        
        self.connections = []
        
        # Add connections
        for link in connections:
            self.connections.append(link)
        
    # Equals
    def __eq__(self, other):
        return (self.id == other.id)
        
    # Lesser Than
    def __lt__(self, other):
        return (self.id < other.id)
   
    # Greater Than
    def __gt__(self, other):
        return (self.id > other.id)
        
    # Not Equal
    def __ne__(self, other):
        return not self.__eq__(other)
    
    # Lesser Than or Equal to
    def __le__(self, other):
        return not self.__gt__(self, other)
    
    # Greater Than or Equal To
    def __ge__(self, other):
        return not self.__lt__(self, other)
        
        
    # Hash Check, used in sets
    def __hash__(self):
        return int(self.id)

#
# Road class
# - Defines a way to get to place, needs to connect to a Connection
#

class Road:
    # The ID for the road
    id = -1
    
    # The name of the road
    name = "NULL"
    
    # The length of the class (u length)
    length = 0.0
    
    # The speed limit (u/hr)
    speed = 0.01
    
    # The Connections the road has to Connections
    connections = []
    
    # The amount of drivers on this road...
    drivers = 0
    
    # Constructor
    def __init__(self, id, name, length, speed, connections):
        # Set values
        self.id = id
        self.name = name
        self.length = length
        self.speed = speed

        self.connections = []
        
        # Add links to the array
        for link in connections:
            self.connections.append(link)
            
    # Equals
    def __eq__(self, other):
        return (self.id == other.id)
        
    # Lesser Than
    def __lt__(self, other):
        return (self.id < other.id)
   
    # Greater Than
    def __gt__(self, other):
        return (self.id > other.id)
        
    # Not Equal
    def __ne__(self, other):
        return not self.__eq__(other)
    
    # Lesser Than or Equal to
    def __le__(self, other):
        return not self.__gt__(self, other)
    
    # Greater Than or Equal To
    def __ge__(self, other):
        return not self.__lt__(self, other)
        
    
    # Hash Check, used in sets
    def __hash__(self):
        return int(self.id)

# Behaviour Enum 
# Behaviour of the driver, this impacts how they go to their destination 
class Behaviour(Enum):
    RECKLESS = 0        # QUICKEST (SPEED AND DISTANCE)
    TIMID    = 1        # SAFEST   (LEAST CHANCE OF DEATH)
    SHORTEST = 2        # SHORTEST (DISTANCE)
    BALANCED = 3        # Balanced (SPEED, LENGTH and DEATH)

# Used because Enums suck in python.
BEHAVIOUR_ARR = ['RECKLESS', 'TIMID', 'SHORTEST', 'BALANCED']
BEHAVIOUR_N = len(BEHAVIOUR_ARR)

#
# Driver class
# - Defines a driver on the road
#
class Driver:
    # Target (Connection)
    target = -1
    
    # Current (Connection)
    current = -1
    
    # Current Road (Road)
    on_road = None
    
    # The path of nodes
    path = []
    
    # This is a boolean which marks the driver for deletion
    died = False
    
    # This is the behaviour 
    behaviour = None
    
    # Progress, this is a % of how much of the current node we've completed
    progress = 0.0
    
    # Initial
    def __init__(self, current, target):
        self.current = current
        self.target = target
        self.path = []
        
        # Generate a value...
        behaviour_index =  random.randint(0, BEHAVIOUR_N - 1)
        behaviour_value = BEHAVIOUR_ARR[behaviour_index]
        self.behaviour = Behaviour[behaviour_value]
Driver.n = 0


# Find Quickest Path (QUICKEST NEVER CHANGES)
def driver_greedQuickest(cur_node, road, next_node): 
    # Generate the heuristic of the road
    return road.length * road.speed;

# Find Safest   Path (THIS CHANGES)
def driver_greedSafest  (cur_node, road, next_node):
    return cur_node.crash + next_node.crash

# Find Shortest Path (LENGTH NEVER CHANGES)
def driver_greedShortest(cur_node, road, next_node):
    return road.length

# Find most balanced path...
def driver_greedBalanced(cur_node, road, next_node):
    cost = driver_greedQuickest(cur_node, road, next_node)
    death = driver_greedSafest(cur_node, road, next_node)
    
    # If there is a significant chance of death...
    if death > 0.01:
        return death
        
    # If the chance of death is next to nothing, while the cost is large...
    if cost > 2 and death < 0.01:
        return cost
    
    # If neither, return with a combination of both
    return cost*death 

# Heuristic Checks
def driver_greed(driver):
    behaviour = driver.behaviour
    # IF the driver wants the quickest
    if behaviour is Behaviour.RECKLESS:
        return driver_greedQuickest
    # IF driver wants the safest
    elif behaviour is Behaviour.TIMID: 
        return driver_greedSafest
    # IF the driver wants the shortest length
    elif behaviour is Behaviour.SHORTEST:
        return driver_greedShortest
    elif behaviour is Behaviour.BALANCED:
        return driver_greedBalanced
    else:
        return None





# Get node between...
def get_road_between(roads, left, right):
    # For roads in the least between the two 
    left_len = len(left.connections)
    right_len = len(right.connections)
    
    left_id = left.id
    right_id = right.id
   
    min_node = left
   
    # If left is bigger...
    if left_len > right_len:
        min_node = right
        
    # Search this node.
    for road_id in min_node.connections:
        # Get the road 
        r = roads[road_id]
        
        # Get connections of this road
        if left_id in r.connections:
            # If the right id is also in the connections 
            if right_id in r.connections:
                # Return this road
                return r
    # If there was no road...
    return None

# Get node's neighbours 
def get_neighbours(roads, connections, node):
    # This is our neighbour array 
    neighbour = []
    node_id = node.id
    
    # For all connections
    for road_id in node.connections:
        # Get the road 
        road = roads[road_id]
        
        # For both of the values 
        for con_id in road.connections:
            # Add the node thats not the one we just came from
            if node_id != con_id:
                neighbour.append(con_id)
    # Return the array 
    return neighbour
 
