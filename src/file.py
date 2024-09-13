# file.py - Reads Road File(s) and Prints Results
#
# Author: Cameron Sims
# Date: 06/08/2024
#

# Required Imports #######################

# Internal Imports
import road     # Used to save data into

# External Imports
import csv      # Used to read a csv file

##########################################


# Read connection data from a file
def read_connection_manifest(filename, connections): 
    # Read the manifest file
    file = open(filename, "r")
    
    # Read the data
    data = csv.DictReader(file)
    
    # For all the lines in the file...
    for line in data:
        # Create a variable to use
        ID = int(line["id"])
        CRASH_INDEX = float(line["crash"])
        c = road.Connection(ID, CRASH_INDEX, [])
        
        connections.update({c.id: c})


# Read road data from a file
def read_road_manifest(filename, roads, connections):
    # Open the manifest file
    file = open(filename, "r")
    
    # Read the data
    data = csv.DictReader(file)
    
    # Get the Connection by ID
    def get_vertex(connections, id):
        return connections[id]
    
    # For all the lines in the file...
    for line in data:
        # Set which is used to find valeus with our ID
        ID = int(line["id"])
        NAME = line["name"]
        LENGTH = float(line["length"])
        SPEED = float(line["speed"])
        
        FROM = int(line["from"])
        TO = int(line["to"])
        
        # Connections
        CONS = [FROM, TO]
        
        # Vertexes
        FROM_V = get_vertex(connections, FROM)
        TO_V = get_vertex(connections, TO)
        # Add this road to both 
        FROM_V.connections.append(ID)
        TO_V.connections.append(ID)
        
        # Create a variable to use 
        r = road.Road(ID, NAME, LENGTH, SPEED, CONS)
        
        # Add this instance to the set
        roads.update({r.id: r})

# Save road data 
def save_road_data(road_csv, road_data):
    # Open the file.
    file = open(road_csv, "w")
    
    # Print in format
    
    
    # Close FSTREAM
    file.close()

# Save Connection Data
def save_cons_data(cons_csv, cons_data):
    # Open the file.
    file = open(cons_csv, "w")
    
    # The columns 
    columns = [ "id", "crossed", "targeted", "deaths" ]
    LAST_COLUMN = columns[len(columns) - 1]
    
    # Print in format
    file.write("id,crossed,targeted,crashes\n")
    
    # For all connections...
    for connection in cons_data["nodes"]:
        # Add each columns value into the row
        for col in columns:
            # Get the value 
            column_value = connection[col]
            # Add it 
            file.write(str(column_value))
            # if not last... add a comma
            if col != LAST_COLUMN:
                file.write(',')
            # Otherwise, print a new line
            else:
                # Add row
                file.write('\n')
    
    # Close FSTREAM
    file.close()

# Save simulation data   
def save_sim_data(road_csv, cons_csv, simulation_data):
    # Save road data 
    save_road_data(road_csv, simulation_data["roads"])
    
    # Save con data 
    save_cons_data(cons_csv, simulation_data["intersections"])
    
    # Save session data 