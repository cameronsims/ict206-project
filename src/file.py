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

# Save a row
def save_data(stream, data, columns):
    # Get last column 
    LAST_COLUMN = columns[len(columns) - 1]
    
    # Write header 
    for col_name in columns:
        stream.write(col_name)
        # If not last 
        if col_name != LAST_COLUMN:
            stream.write(',')
    stream.write('\n')

    # For all connections...
    for connection in data:
        # Add each columns value into the row
        for col in columns:
            # Get the value 
            column_value = connection[col]
            # Add it 
            stream.write(str(column_value))
            # if not last... add a comma
            if col != LAST_COLUMN:
                stream.write(',')
            # Otherwise, print a new line
            else:
                # Add row
                stream.write('\n')

# Save road data 
def save_road_data(roads, road_csv, road_data):
    # Open the file.
    file = open(road_csv, "w")
    
    # The columns 
    columns = [ "id", "entered", "exited" ]
    
    # For all connections...
    save_data(file, road_data["vertex"], columns)
    
    # Close FSTREAM
    file.close()

# Save Connection Data
def save_cons_data(cons, cons_csv, cons_data, roads):
    # Open the file.
    file = open(cons_csv, "w")
    
    # This gets all the roads of the connection
    def read_probabilities(con_id):
        # Probability String 
        probabilities = ""
        # Get the connections...
        con = cons[con_id]
        
        # Check all roads 
        for r_id in con.connections:
            # Calculate the percentage.
            r = roads[r_id]
            px = road.death_probability(cons, con, r)
            s = (str(px) + ' ')
            probabilities += s
        return probabilities
    
    # The columns 
    columns = [ "id", "crossed", "targeted", "deaths", "crash probability" ]
    
    # Connection IDs
    last = len(columns) - 1
    col_name = columns[last]
    for con_id in cons:
        cons_data["nodes"][con_id - 1][col_name] = read_probabilities(con_id)
    
    # For all connections...
    save_data(file, cons_data["nodes"], columns)
    
    # Close FSTREAM
    file.close()

# Save simulation data   
def save_sim_data(roads, road_csv, cons, cons_csv, simulation_data):
    # road.road_death_probability(road, cons, road, con)
    # Save road data 
    save_road_data(roads, road_csv, simulation_data["roads"])
    
    # Save con data 
    save_cons_data(cons, cons_csv, simulation_data["intersections"], roads)