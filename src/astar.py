# astar.py - Calculating A* 
#
# Author: Cameron Sims
# Date: 27/09/2024
#

import road

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
        node = cons[node_id]
        
        # Remove the node we just read.
        unvisited.remove(node_id)
        
        # Get's current node's neighbours
        neighbours  = road.get_neighbours(roads, cons, node)
        
        # Get the node ID in the neighbour array 
        for child_id in neighbours:
            # Get current node 
            child = cons[child_id]
            
            # Get the value of our parent ID, plus this value 
            child_dist = distance[node_id] + child.crash
            
            # If the value that we just read is smaller than the value held...
            if child_dist < distance[child_id]:
                # Set this value 
                distance[child_id] = child_dist
    
    return distance

# This finds the path based on certain type of path finding
# This is A*
def find_path(roads, cons, current, destination, greedf):
    # Check if this current node is the ID...
    if current.id == destination.id:
        # If it is, return the path]
        return [ current.id ]
    
    # We will then execute A*, here is where A* Begins 
    
    # This is how we construct our path 
    path = dict()
    
    # Dikstra's Algorithm, this is a dictionary of all distances
    dist = dict() # Distance (g)
    cost = dict() # Cost     (f)
    
    # Set to infinity
    for node_id in cons:
        dist[node_id] = float("inf")
        cost[node_id] = float("inf")
    
    dist[current.id] = 0
    
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
                location_id = node_id
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
        
        # Reverse our path...
        ret_path.append(current.id)
        ret_path = ret_path[::-1]
        return ret_path
    
    # While we have things in our array
    while len(opened) > 0:
        # Get the first in our queue
        location_id = next_node()
    
        # Get our vertex after we figure out the smallest
        location = cons[location_id]
        
        # If this ID is the id we're looking for 
        if location_id == destination.id:
            # Return the path 
            opt_path = get_path(location_id)]
            return opt_path
        
        # Remove the first from the list 
        opened.remove(location_id)
        closed.append(location_id)
        
        # For all neighbours of our node...
        neighbours = road.get_neighbours(roads, cons, location)
        for neighbour_id in neighbours:
            # Neighbour node
            neighbour = cons[neighbour_id]
            road_between = road.get_road_between(roads, location, neighbour)
            
            distance = road_between.length
            
            # Create G Score
            g_score = dist[ location_id ] + distance
            
            if g_score < dist[neighbour_id]:
                # This is our greedf
                hx = greedf(location, road_between, neighbour)
            
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
    return [ -1 ]

# These are optimal paths...
# These are dictionaries so that we access it like this...
# opt[start][end] -> path
optimal_distance = dict()
optimal_balanced = dict()
optimal_speed = dict()

# This is dropped and re-generated every hour (if a driver dies)
optimal_saftey = dict()

#
# find_destination(roads, location, destination)
# - This is a helper function to path find to a place.
#
def find_destination(driver, roads, cons, location, destination):
    # Check if location and destination are the same...
    if (location == destination):
        return [ -1 ]
    
    # This is where the nodes are
    loc_node = cons[location]   # This is where the current driver is.
    dest_node = cons[destination]  # This is where the driver wants to go.
    
    # Now try to find a connection between the two...
    # We're going to use a path finding algorithm of least resistance
    
    # Before we do anything... 
    # Ensure that the driver doesn't need to update the path checking...
    if driver.behaviour == road.Behaviour.RECKLESS:
        return optimal_speed[location][destination]
    # Also check if it is shortest 
    elif driver.behaviour == road.Behaviour.SHORTEST:
        return optimal_distance[location][destination]
    elif driver.behaviour == road.Behaviour.BALANCED:
        return optimal_balanced[location][destination]
    
    # This refers to the node IDs that have been visited
    if location in optimal_saftey:
        if destination not in optimal_saftey[location]:
            path = find_path(roads, cons, loc_node, dest_node, road.driver_greed(driver))
            optimal_saftey[location][destination] = path
            optimal_saftey[destination][location] = path[::-1]
            
    else:
        path = find_path(roads, cons, loc_node, dest_node, road.driver_greedf(driver))
        optimal_saftey[location][destination] = path
        optimal_saftey[destination][location] = path[::-1]
    return optimal_saftey[location][destination]

# We will generate our optimal paths for static variables (distance and speed)
def find_optimal_paths(roads, cons):
    # Before we do anything, set absolutely everything to None, unless it is itself.
    for loc_id in cons:
        optimal_distance[loc_id] = dict()
        optimal_speed   [loc_id] = dict()
        optimal_saftey  [loc_id] = dict()
        optimal_balanced[loc_id] = dict()
        
        
        # Set self to self to be -1
        optimal_distance[loc_id][loc_id] = [ -1 ]
        optimal_speed   [loc_id][loc_id] = [ -1 ]
        optimal_balanced[loc_id][loc_id] = [ -1 ]
        
        for dest_id in cons:
            optimal_distance[loc_id][dest_id] = None
            optimal_speed   [loc_id][dest_id] = None
            optimal_balanced[loc_id][dest_id] = None
    
    
    # For every single connection...
    for loc_id in cons:    
        # The location ID 
        loc = cons[loc_id]
        
        # For every single destination 
        for dest_id in cons:
            # Destination ID 
            dest = cons[dest_id]
            # If we are not at the same node 
            if optimal_distance[loc_id][dest_id] == None and optimal_speed[loc_id][dest_id] == None:
                # Get fastest by speed
                path_short = find_path(roads, cons, loc, dest, road.driver_greedShortest)
                
                # Get fastest by distance 
                path_speed = find_path(roads, cons, loc, dest, road.driver_greedQuickest)
                
                # Get balanced 
                path_balanced = find_path(roads, cons, loc, dest, road.driver_greedBalanced)
                
                # Find for both greedfs...
                optimal_distance[loc_id][dest_id] = path_short
                optimal_speed   [loc_id][dest_id] = path_speed
                optimal_balanced[loc_id][dest_id] = path_balanced
                
                optimal_distance[dest_id][loc_id] = path_short[::-1]
                optimal_speed   [dest_id][loc_id] = path_speed[::-1]
                optimal_balanced[dest_id][loc_id] = path_balanced[::-1]

# This will drop the safety cache
def drop_saftey_cache():
    # For all keys 
    keys = optimal_distance.keys()
    
    # Create saftey dictionary.
    optimal_saftey = dict()
    
    # Create another for each connection
    for key in keys:
        optimal_saftey[key] = dict()