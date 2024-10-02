# graphing.py - Adds graph compatibility to the program
#
# Author: Cameron Sims
# Date: 06/08/2024
#

# Required Imports ##########################

# External Imports
import pyvis.network    # Read networks
import networkx as nx   # More network imports

#############################################

def make_road_title(road, road_data, pass_rate, conjestion):
    subjects = [
        "ID", 
        "Name", 
        "Length", 
        "Speed",
        "Pass",
        "Conjestion Score"
    ]
    values = [
        str(road.id),
        road.name,
        str(road.length),
        str(road.speed),
        str( 100*pass_rate(road.id) ),
        str(conjestion(road.id))
    ]
    
    # Add to title 
    title = ""
    for i in range(len(subjects)):
        greater = subjects[i] + ": "
        lesser = values[i] + "\n"
        title += (greater + lesser)
    
    # Return result 
    return title

# Create node title 
def make_node_title(con, node_data):
   # Make subjects and values
   subjects = [ 
       "ID", 
       "Crash Percentage", 
       "Deaths", 
       "Targeted", 
       "Crossed"
   ]
   values = [ 
       str(con.id), 
       str(con.crash), 
       str(node_data["deaths"]), 
       str(node_data["targeted"]),
       str(node_data["crossed"])
   ]
   
   # Add to the title...
   title = ""
   for i in range(len(subjects)):
       # Add greater and lesser half of string to a greater string to make a row
       greater = subjects[i] + ": "
       lesser = values[i] + "\n"
       title += (greater + lesser)
   return title

# Used to set roads and connections to a graph
def create_graph(filename, roads, cons, simulation_data):

    net = pyvis.network.Network(notebook = True)
    
    # Physics Nodes
    net.toggle_physics(True)
    net.show_buttons(filter_=['physics'])
    
    #net.set_options("{physics:{nodeDistance:200}}")
    def metric(n_id):
        return cons[n_id].deaths
    
    # Get the node where most the deaths occured...
    highest_death_node_id = max(cons, key=metric)
    lowest_death_node_id = min(cons, key=metric)
    
    highest_death_node = cons[highest_death_node_id]
    lowest_death_node = cons[lowest_death_node_id]
    
    highest_death = highest_death_node.deaths
    lowest_death = lowest_death_node.deaths
   
    # Get average deaths 
    total_deaths = 0
    for cid in cons:
        # Get node 
        con = cons[cid]
        total_deaths += con.deaths
    
    average_deaths = total_deaths / len(cons)
    if average_deaths == 0:
        average_deaths = 1
   
    # For all connections...
    total_visited = 0
    for cid in cons:
        # Get node 
        con = cons[cid]
        
        # Get the node in simulation data...
        node_data = simulation_data["intersections"]["nodes"][cid - 1]
        
        # Add a node
        TITLE = make_node_title(con, node_data)
        
        # Get how much deaths occured compared to the max 
        # We want it to scale linearly, add 1 so it shows
        death_scale = ((node_data["deaths"] + 1) / average_deaths) + 1
        total_visited += node_data["crossed"]
        
        net.add_node(con.id, 
                     label=str(con.id), 
                     size=death_scale, 
                     title=TITLE)
    
    # Find roads now
    road_data_all = simulation_data["roads"]["vertex"]
    average_visited = total_visited / len(cons)
    
    # Find maximum congestion
    def conjestion(id):
        road = roads[id]
        entered = road_data_all[id - 1]["entered"]
        cost = (road.length * road.speed)
        
        if cost == 0:
            return 0
            
        return (entered) / (average_visited*cost)
    
    def pass_rate(id):
        road = roads[id]
        data = road_data_all[id - 1]
        
        exited = data["exited"]
        if exited == 0:
            exited = 1
        
        enetered = data["entered"]
        
        return enetered / exited
    
    
    highest_conjestion_id = max(roads, key=conjestion)
    lowest_conjestion_id = min(roads, key=conjestion)
    
    highest_conjestion = conjestion(highest_conjestion_id)
    lowest_conjestion = conjestion(lowest_conjestion_id)
    
    highest_pass_rate_id = max(roads, key=pass_rate)
    lowest_pass_rate_id = min(roads, key=pass_rate)
    
    highest_pass_rate = pass_rate(highest_pass_rate_id)
    lowest_pass_rate = pass_rate(lowest_pass_rate_id)
    
    # Get average conjestion 
    total_conj = 0.0
    for rid in roads:
        total_conj += conjestion(rid)
    average_conjestion = total_conj / len(roads)
    
    # Once all the connections are established...
    for rid in roads:
        # Get the road we're refering to
        r = roads[rid]
        road_data = road_data_all[rid - 1]
        
        if average_conjestion == 0:
            average_conjestion = 1
        road_size = (conjestion(rid) - lowest_conjestion + 1) / (average_conjestion)
        
        # Add an edge
        TITLE = make_road_title(r, road_data, pass_rate, conjestion)
        net.add_edge(r.connections[0], r.connections[1],
                     label = r.name,
                     value = road_size,
                     length = r.length,
                     title = TITLE)
    
    
    net.show(filename)