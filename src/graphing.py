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

# Used to set roads and connections to a graph
def create_graph(filename, roads, cons):

    net = pyvis.network.Network(notebook = True)
    
    # Physics Nodes
    net.toggle_physics(True)
    net.show_buttons(filter_=['physics'])
    
    #net.set_options("{physics:{nodeDistance:200}}")
    
    
    # For all connections...
    for cid in cons:
        # Get node 
        c = cons[cid]
        # Add a node
        TITLE = "ID: " + str(c.id) + "\nCrash Percentage: " + str(c.crash)
        net.add_node(c.id, 
                     label=str(c.id), 
                     size=5, 
                     title=TITLE)
        
    # Once all the connections are established...
    for rid in roads:
        # Get the road we're refering to
        r = roads[rid]
        # Add an edge
        TITLE = "ID: " + str(r.id) + "\nName: " + r.name + "\nLength: " + str(r.length) + "\nSpeed:" + str(r.speed)
        net.add_edge(r.connections[0], r.connections[1],
                     label=r.name, 
                     length=r.length,
                     title=TITLE)
    
    
    net.show(filename)