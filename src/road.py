# road.py - Defines important classes to the system
#
# Author: Cameron Sims
# Date: 06/08/2024
#

from enum import Enum
import random

#
# Connection Class
# - Defines a connection between at most 4 roads
#

class Connection:
    # The ID of the connection (-1 is an illegal ID)
    id = -1
    
    # What the connection connects to (MUST BE ROADS)
    connections = set()
    
    # This is the speed index (functions as the weight)
    # 0.01 - 100.00
    speed = 0.0
    
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
    RECKLESS = 0        # QUICKEST (SPEED)
    TIMID    = 1        # SAFEST   (DEATH)
    SHORTEST = 2        # SHORTEST (LENGTH)

BEHAVIOUR_ARR = ['RECKLESS', 'TIMID', 'SHORTEST']
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
    
    # The path of nodes
    path = []
    
    # This is a boolean which marks the driver for deletion
    died = False
    
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
        
# Find Quickest Path (QUICKEST NEVER CHANGES)
def driver_heuristicQuickest(cur_node, road, next_node): 
    # Generate the heuristic of the road
    return road.length * road.speed;

# Find Safest   Path (THIS CHANGES)
def driver_heuristicSafest  (cur_node, road, next_node):
    return cur_node.crash * next_node.crash

# Find Shortest Path (LENGTH NEVER CHANGES)
def driver_heuristicShortest(cur_node, road, next_node):
    return road.length

# Heuristic Checks
def driver_heuristic(driver):
    behaviour = driver.behaviour
    # IF the driver wants the quickest
    if behaviour is Behaviour.RECKLESS:
        return driver_heuristicQuickest
    # IF driver wants the safest
    elif behaviour is Behaviour.TIMID: 
        return driver_heuristicSafest
    # IF the driver wants the shortest length
    elif behaviour is Behaviour.SHORTEST:
        return driver_heuristicShortest
    else:
        return None


# This function gets the node relating to an id
def get_road(roads, goal):
    # This is a legacy function.
    return roads[goal]
    
# This function gets the node relating to an id
def get_connection(connections, id):
    return connections[id]

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
        road = get_road(roads, road_id)
        
        # Get connections of this road
        if left_id in road.connections:
            # If the right id is also in the connections 
            if right_id in road.connections:
                # Return this road
                return road
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
        road = get_road(roads, road_id) 
        
        # For both of the values 
        for con_id in road.connections:
            # Add the node thats not the one we just came from
            if node_id != con_id:
                neighbour.append(con_id)
    # Return the array 
    return neighbour


# This calculates the longest from each other
def get_distances(roads, cons, current, destination):
    # Dikstra's Algorithm, this is a dictionary of all distances
    distance = { 
        # This sets all node values to infinity
        node: float("inf") for node in cons
    }
    
    # The distances from this distance is going to be 0
    distance[current.id] = 0
    
    # Add nodes we've not added 
    unvisited = []
    
    # Add all nodes besides the current node
    for con_id in cons:
        if con_id != current.id:
            unvisited.append(con_id)
    
    # For all these nodes we've not visited 
    while len(unvisited) > 0:
        # Smallest node ID
        node_id = -1
        
        # Get an unvisited node...
        for unvisited_node_id in unvisited:
            # If there is no smallest node 
            if node_id == -1:
                node_id = unvisited_node_id
            # If we found a new smallest node
            elif distance[unvisited_node_id] < distance[node_id]:
                node_id = unvisited_node_id
    
        # Get the ID 
        node = get_connection(cons, node_id)
        
        # Remove the node we just read.
        unvisited.remove(node_id)
        
        # Get's current node's neighbours
        neighbours  = get_neighbours(roads, cons, node)
        
        # Get the node ID in the neighbour array 
        for child_id in neighbours:
            # Get current node 
            child = get_connection(cons, child_id)
            
            # Get the value of our parent ID, plus this value 
            child_dist = distance[node_id] + child.crash
            
            # If the value that we just read is smaller than the value held...
            if child_dist < distance[child_id]:
                # Set this value 
                distance[child_id] = child_dist
    
    return distance

# This is used recursively, to check nodes individually 
# - Returns true if not all have been visited...
# - False if all have been visited
def check_path(current, visited, destination):
    # Check all connections for our node.
    for c in current.connections:
        # Check visitation...
        if c not in visited or c == destination:
            return True
    # None were founds...
    return False
    
# This finds the path based on certain type of path finding
# This is A*
def find_path(roads, cons, current, destination, heuristic):
    
    # Check if this current node is the ID...
    if current.id == destination.id:
        # If it is, return the path
        #print("Found ID: " + str(destination))
        return [ current.id ]
    
    # We will then execute A* 
        
    # Here is where A* Begins 
    
    # This is how we construct our path 
    path = dict()
    
    # Dikstra's Algorithm, this is a dictionary of all distances
    dist = { node: float("inf") for node in cons } # Distance (g)
    dist[current.id] = 0
    
    cost = { node: float("inf") for node in cons } # Cost (f)
    
    # Start with our first node opened
    opened = [ current.id ] # Queue
    closed = [  ]
    
    def next_node():
        # Start
        location_id = -1
        # Loop through our list 
        for node_id in opened:
            # If location is -1
            if location_id == -1:
                location_id = node_id
            # If the item's f value is smaller than current 
            elif cost[node_id] < cost[location_id]:
                location_id = location_id
        return location_id
    
    def get_path(location_id):
        # We must start at the node that the driver starts at....
        ret_path = [ ]
        
        # (ID -> Next_ID)s
        
        # Then we must use the dictonary to extract values, while we still have our origin in.
        # Since we added to the beginning all our path should be extracted.
        next_id = location_id
        while next_id in path:
            # Add to the beginning of our array
            ret_path.append(next_id);
            
            # Next ID
            next_id = path[next_id]
        # Add our start. 
        ret_path.append(next_id)
        return ret_path[::-1] # Reverse
    
    # While we have things in our array
    while len(opened) > 0:
        # Get the first in our queue
        location_id = next_node()
    
        # Get our vertex after we figure out the smallest
        location = get_connection(cons, location_id)
        
        # If this ID is the id we're looking for 
        if location_id == destination.id:
            # Return the path 
            return get_path(location_id)
        
        # Remove the first from the list 
        opened.remove(location_id)
        closed.append(location_id)
        
        # For all neighbours of our node...
        neighbours = get_neighbours(roads, cons, location)
        for neighbour_id in neighbours:
            # Neighbour node
            neighbour = get_connection(cons, neighbour_id)
            road_between = get_road_between(roads, location, neighbour)
            
            distance = road_between.length
            
            # Create G Score
            g_score = dist[ location_id ] + distance
            
            if g_score < dist[neighbour_id]:
                # This is our heuristic
                hx = heuristic(location, road_between, neighbour)
            
                path[neighbour_id] = location_id
                dist[neighbour_id] = g_score 
                cost[neighbour_id] = g_score + hx
                
                # if our neighbour isn't already in the array...
                if neighbour_id not in opened:
                    # Add the value in
                    opened.append(neighbour_id)
                    
                    if neighbour_id in closed:
                        # Remove it from our closed...
                        closed.remove(neighbour_id)
    
    # If we somehow get here...
    # We did not find a connection in the path...
    # It cannot be in this connection, as we have tried every possible combination
    return [-1]

#
# find_destination(roads, location, destination)
# - This is a helper function to path find to a place.
#
def find_destination(driver, roads, cons, location, destination):
    # Check if location and destination are the same...
    if (location == destination):
        print(str(location) + " is the same node as " + str(destination))
        return [ -1 ]
    
    # This is where the nodes are
    loc_node = cons[location]   # This is where the current driver is.
    dest_node = cons[destination]  # This is where the driver wants to go.
    
    # Now try to find a connection between the two...
    # We're going to use a path finding algorithm of least resistance
    
    # This refers to the node iDs that have been visited
    return find_path(roads, cons, loc_node, dest_node, driver_heuristic(driver))