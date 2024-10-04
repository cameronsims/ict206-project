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

# Import data from an external file
simulation.data_create("./data/sim_data.json")

# Print Signature
display.print_signature()

cons = {}    # Connection Map
roads = {}   # Road Map

# Read manifest(s)
display.print_connection_begin()

# Read the data pertaining to how the structure of the roads work
file.read_manifest_files("./data/", "./data/time.csv", roads, cons)

# Tell user we succeeded
display.print_connection_end()

# Get data for the simulation
simulation_data = simulation.begin(roads, cons)

# Perform Analysis...
analysis.perform_analysis(roads, cons, simulation_data)

# Save results
file.save_sim_data(roads, "./out/road_report.csv", cons, "./out/intersection_report.csv", "./out/weather_report.csv", simulation_data)

# Create the graph
display.print_pyvis_begin()

# Create the graph
graphing.create_graph("./out/graph.html", "./data/network.js", roads, cons, simulation_data)

# Tell user that we have completed the program.
display.print_pyvis_end()