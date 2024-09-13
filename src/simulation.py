# road.py - Defines important classes to the system
#
# Author: Cameron Sims
# Date: 20/08/2024
#

# Required Imports ##########################

# Internal Imports
import display  # Used for printing and showing to user
import uinput   # Used for getting input from the user
import file     # Used for Reading Road Files
import road
import simulation # Used for running the simulation

# External Imports 
import random   # used to calculate death percentage
import json # Used to read simulation data

#############################################


# This is the variables for certain simulation data, these modify how the system will run and execute.
data = None

# This is where we set the data...
def data_init(dir):
    file = open(dir)
    return json.load(file)

# This is called so we save the data into this file 
def data_create(manifest):
    simulation.data = simulation.data_init(manifest)
    
# Re-generate driver
def driver_regenerate(roads, cons, driver, on_target):
    # This is the lowest ID of our roads.
    BIGGEST_CON_ID = min(cons)
    
    # This is the highest ID of our roads.
    SMALLEST_CON_ID = max(cons)
    
    # Floor and Cieling an ID
    FLOOR = BIGGEST_CON_ID    #.id
    CIELING = SMALLEST_CON_ID #.id
    
    # Generate random numbers for our target destination and the beginning destination for the driver.
    currentID = driver.target
    if currentID < SMALLEST_CON_ID or currentID > BIGGEST_CON_ID:
        currentID = random.randint(FLOOR, CIELING)
    
    targetID  = random.randint(FLOOR, CIELING)
    
    # loop until we find a new one
    while currentID == targetID:
        targetID = random.randint(FLOOR, CIELING)
    
    # Target and Current
    driver.current = currentID
    driver.target = targetID
    
    on_target(targetID)
    
    # find new path
    driver.path = road.find_destination(driver, roads, cons, currentID, targetID)

# This is the update function it modifies how a driver runs, it runs every tick...
# - road: is the node that the node is across
# - regen_f: is a function that regenerates the path finding
def driver_update(driver, roads, connections, on_crossed, on_target):
    # The ID that we are using 
    from_node = -1
    to_id = -1
    
    # If we only have one node in our path...
    if len(driver.path) < 2:
        # Set node IDs
        from_id = driver.current
        to_id = driver.path[0]
    else:
        # Use pathing
        from_id = driver.path[0]
        to_id = driver.path[1]
    
    # These are defines important for the function...
    from_node = connections[from_id]
    to_node   = connections[to_id]
    
    road_con = road.get_road_between(roads, from_node, to_node)
   
    # If the driver has finished their trip across a road...
    if driver.progress >= 1.00:
        # Then pop the beginning of the queue and find the next connection to go down
        if len(driver.path) > 1:
            # Add that a driver has crossed this node 
            on_crossed(driver.path[0])
            
            # Remove next
            driver.path.pop(0)
            driver.current = driver.path[0]
            
            # Now find a new target...
            # Set the target to the next node.
            driver.progress = 0.00
            
            # Check the intersections crash rate...
            # First we have to find the intersection that we're heading towards
            for cid in road_con.connections:
                con = connections[cid]
                if driver.current in con.connections:
                    # Roll the dice to see death
                    dice = random.uniform(data["prob_floor"], data["prob_ceil"])
                    difference = abs(dice - con.crash)
                    # If the difference is too large, don't count it.
                    # But if the difference is small, kill the driver
                    if difference < data["float_difference"]:
                        driver.died = True
                        # Log a new death that occured on the road.
                    break
        
        # If the driver is at their planned destination...
        if driver.target == driver.current:
            # Regenerate a driver
            driver_regenerate(roads, connections, driver, on_target)
    # If the progress has no finished
    else:
        # Add to the progress...
        road_length = road_con.length
        road_speed = road_con.speed
        current_position = driver.progress * road_length
        current_progress = road_speed / data["sim_minutes"]
        driver.progress = driver.progress + current_progress
    # End of Driver - Update Function

# Start the simulation   
def begin(roads, cons):
    # This is data for our driver, contains size and array of all drivers
    # This is not a set as we are going to edit every single driver every single simulation cycle
    # This will result in O(n), therefore we don't care if it is a set.
    drivers_n = uinput.get_driver_amount(display.print_error)
    drivers = {}
    
    # Get the amount of months we're running for (months * 30 * 24 = hours)
    sim_months = uinput.get_sim_time(display.print_error)
    sim_hours = sim_months * simulation.data["sim_hours"] # simulation.data["sim_days"]

    # This is where the simulation begins
    hours = sim_hours 
    
    # This is data for the simulation
    simulation_data = {
        "length": sim_hours * simulation.data["sim_minutes"],
        
        "intersections": {
            "nodes": [],
            "length": len(cons)
        },
        
        "roads": {
            "length": len(roads)
        },
    
        "drivers": {
            "start": drivers_n,
            "deaths": 0,
            "end": -1
        }
    }
    
    # Add all node values
    i = 0
    for c_id in cons:
        # Get connection
        con = cons[c_id]
        # Add value for node in sim data
        simulation_data["intersections"]["nodes"].append({ 
            "id": c_id, 
            "crossed": con.crossed,
            "targeted": con.targeted,
            "deaths": con.deaths 
        })
        # Increment 
        i += 1
    
    # Before we start the drivers, we must first initalise our lambda events 
    def on_crossed(node_id):
        simulation_data["intersections"]["nodes"][node_id - 1]["crossed"] += 1
    def on_target(node_id):
        simulation_data["intersections"]["nodes"][node_id - 1]["targeted"] += 1
    
    # Add the amount of drivers
    for i in range(drivers_n):
        id = i + 1
        driver = road.Driver(-1 , -1)                            # Create driver object
        driver_regenerate(roads, cons, driver, on_target)        # Generate a path...
        drivers.update({ id: driver })                           # Append to array
    
    # Run while we have hours to go...
    while hours > 0:
        # Show how much hours there is left to go 
        display.print_hours(hours)
        
        # This is every minute for an hour...
        for minute in range(simulation.data["sim_minutes"]):
            # Do some logic per tick... ##########################
            
            # Check drivers ######################################
            
            # Driver
            i = 0
            to_delete = []
            for id in drivers:
                # Get the driver object 
                driver = drivers[id]
                #print(driver.current, driver.target, driver.path, driver.progress)
                simulation.driver_update(driver, roads, cons, on_crossed, on_target)
                
                # Check if driver has died
                if driver.died:
                    # Queue driver for deletion
                    to_delete.append(id)
                    
                    # Increment deaths in that connection
                    node_id = driver.current
                    node = cons[node_id]
                    node.deaths += 1
                    simulation_data["intersections"]["nodes"][node_id - 1]["deaths"] += 1
                    
                    # Increment death total
                    simulation_data["drivers"]["deaths"] += 1
                i += 1
            
            # Remove the drivers from the array 
            for id in to_delete:
                drivers.pop(id)
            
            ######################################################=
        
        # Decrement the Hours
        hours = hours - 1
    
    # Save data due to end of simulation 
    
    simulation_data["drivers"]["end"] = len(drivers)
    
    return simulation_data;
    # End of simulation