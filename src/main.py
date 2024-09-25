# main.py - The main part of the program, everything links to here
#
# Author: Cameron Sims
# Date: 06/08/2024
#

# Required Imports ##########################

# Internal Imports
import display     # Used for printing and showing to user
import graphing    # Used for graphing
import simulation  # Used for running the simulation
import analysis    # Used for analysing the simulation
import file        # Used for CSV

#############################################

# We've loaded all our imports...

# These are the CSV files for the data we're reading (relative)
DATA_DIRECTORY = "./data/"
ROAD_MANIFEST = DATA_DIRECTORY + "roads.csv"             # Location of the road csv file
CONNECT_MANIFEST = DATA_DIRECTORY + "connections.csv"    # Location of the connections csv file
SIMDATA_MANIFEST = DATA_DIRECTORY + "sim_data.json"      # Location of the data json file

# This where our file is going to be output (relative)
OUTPUT_DIRECTORY = "./out/"
GRAPH_FILENAME = OUTPUT_DIRECTORY + "graph.html"

ROAD_CSV_FILENAME = OUTPUT_DIRECTORY + "road_report.csv"
CONS_CSV_FILENAME = OUTPUT_DIRECTORY + "intersection_report.csv"

# Import data from an external file
simulation.data_create(SIMDATA_MANIFEST)

# Print Signature
display.print_signature()

# Sets for quick access to road or connection data
# There cannot be a duplicate ID, which makes sense in-terms of our program
# Since it is a map, the O(n) is either log(n) or 1 (depending on type)
cons = {}    # Connection Map
roads = {}   # Road Map

# Read manifest(s)
display.print_connection_begin()

# Read the data pertaining to how the structure of the roads work
file.read_connection_manifest(CONNECT_MANIFEST, cons)
file.read_road_manifest      (ROAD_MANIFEST,    roads, cons)

# Tell user we succeeded
display.print_connection_end()

# Get data for the simulation
simulation_data = simulation.begin(roads, cons)

# Perform Analysis...
analysis.perform_analysis(roads, cons, simulation_data)

# Save results
file.save_sim_data(roads, ROAD_CSV_FILENAME, cons, CONS_CSV_FILENAME, simulation_data)

# Create the graph
display.print_pyvis_begin()

# Create the graph
graphing.create_graph(GRAPH_FILENAME, roads, cons, simulation_data)

# Tell user that we have completed the program.
display.print_pyvis_end()