# create_graph.py - This is an off-shoot of the default program that just generates a graph
#
# Author: Cameron Sims
# Date: 20/08/2024
#

# Required Imports ##########################

# Internal Imports
import display
import file     # Used for Reading Road Files
import graphing # Used for graphing
import road
#############################################

# We've loaded all our imports...

# If all of our imports and variables worked...
# Then we will print out some things into the console

# Print Signature
display.print_signature()

# Sets for quick access to road or connection data
# There cannot be a duplicate ID, which makes sense in-terms of our program
cons = {}    # Connection Map
roads = {}   # Road Map

# Read manifest(s)
display.print_connection_begin()

file.read_connection_manifest("./data/connections.csv", cons)
file.read_road_manifest      ("./data/road.csv", roads, cons)

# Show that we have ended reading
display.print_connection_end()

# Create the graph
display.print_pyvis_begin()

# Generate boring data 
simulation_data = {
    "intersections": { "nodes": [] },
    "roads": { "vertex": [] }
}

simulation_data["intersections"]["length"] = 1
for con_id in cons:
    # Connections 
    #crossed,targeted,deaths,crash probability
    simulation_data["intersections"]["nodes"].append({
        "id": con_id,
        "crossed": 1,
        "targeted": 1,
        "deaths": 1
    })

simulation_data["roads"]["length"] = 1
for road_id in roads:
    # Connections 
    #crossed,targeted,deaths,crash probability
    simulation_data["roads"]["vertex"].append({
        "id": road_id,
        "entered": 1,
        "exited": 1
    })

# Create graph
graphing.create_graph("./out/graph.html", roads, cons, simulation_data)

display.print_pyvis_end()