# file.py - Reads/Prints File(s) 
#
# Author: Cameron Sims
# Date: 06/08/2024
#

# Required Imports #######################

# Internal Imports
import road     # Used to save data into
import death
import weather
import display
import uinput

# External Imports
import os
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
   
# Read the weather file   
def read_weather_file(filename):
    # Open the manifest file
    file = open(filename, "r")
    
    # Read the data
    data = csv.DictReader(file)
    
    total = 0.0
    
    # For all the lines in the file...
    for line in data:
        # Set which is used to find valeus with our ID
        NAME = line["TYPE"]
        PERCENT = line["PERCENT"]
        CRASH_MOD = line["CRASH"]
        SPEED_MOD = line["SPEED"]
        
        for i in range(weather.WEATHER_N):
            if weather.WEATHER_ARR[i] == NAME:
                # If it is, set it and continue with loop.
                f_px = float(PERCENT)
                f_px = abs(f_px)
                total = total + f_px
                weather.Weather.percentages[i] = total
                
                weather.Weather.crash_modifiers[i] = float(CRASH_MOD)
                weather.Weather.speed_modifiers[i] = float(SPEED_MOD)
                break
            i += 1

# Read the weather file   
def read_time_file(filename):
    # Open the manifest file
    file = open(filename, "r")
    
    # Read the data
    data = csv.DictReader(file)
    # For all the lines in the file...
    for line in data:
        # Set which is used to find valeus with our ID
        NAME = line["TYPE"]
        CRASH_MOD = line["CRASH"]
        
        for i in range(weather.TIME_N):
            if weather.TIME_ARR[i] == NAME:
                # If it is, set it and continue with loop.
                weather.Time.crash_modifiers[i] = float(CRASH_MOD)
                break
            i += 1

# This reads the manifests
def read_manifest_files(directory_file, time_file, roads, cons):
    # Get the directory list 
    road_dir = directory_file + "roads/"
    directories = os.listdir(road_dir)
    
    # Get the road/con network we want to use.
    display.print_dir_files("Please select a road network", directories)
    
    # Get the value from user 
    question = "Input file index (0-" + str(len(directories) - 1) + "):"
    file_n = -1
    while file_n < 0 or file_n > len(directories) - 1: 
        file_n = uinput.get_u0int(question, display.print_error)
    
    read_connection_manifest(road_dir + directories[file_n] + "/connections.csv", cons)
    read_road_manifest      (road_dir + directories[file_n] + "/roads.csv", roads, cons)
    
    
    # Get the weather we want 
    weather_dir = directory_file + "forecasts/"
    directories = os.listdir(weather_dir)
    
    display.print_dir_files("Please select a weather type", directories)
    
    # Get the value from user 
    question = "Input file index (0-" + str(len(directories) - 1) + "):"
    file_n = -1
    while file_n < 0 or file_n > len(directories) - 1:
        file_n = uinput.get_u0int(question, display.print_error)

    read_weather_file       (weather_dir + directories[file_n] + "/weather.csv")
    read_time_file          (time_file)

# Returns the data from a file 
def read_network_file(filename):
    # Read everything
    f = open(filename, "r")
    info = ""
    for line in f:
        info += line
    return info


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
    for row in data:
        # Add each columns value into the row
        for col in columns:
            # Get the value 
            column_value = row[col]
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
            px = death.death_probability(cons, con, r)
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

# Save Weather data 
def save_weather_data(weather_csv, weather_data):
    # Open the file.
    file = open(weather_csv, "w")
    
    # Create an array to represent the objects...
    
    # The columns 
    columns = [ "type", "frequency", "deaths" ]
    
    # The raw array
    weather_object_array = []
    for weather_name in weather.WEATHER_ARR:
        this_obj = {
            "type": weather_name,
            "frequency": weather_data[weather_name]["frequency"],
            "deaths": weather_data[weather_name]["deaths"]
        }
        weather_object_array.append(this_obj)
    
    # For all connections...
    save_data(file, weather_object_array, columns)
    
    # Close FSTREAM
    file.close()

# Save simulation data   
def save_sim_data(roads, road_csv, cons, cons_csv, weather_csv, simulation_data):
    # road.road_death_probability(road, cons, road, con)
    # Save road data 
    save_road_data(roads, road_csv, simulation_data["roads"])
    
    # Save con data 
    save_cons_data(cons, cons_csv, simulation_data["intersections"], roads)
    
    # Save weather data 
    save_weather_data(weather_csv, simulation_data["weather"])