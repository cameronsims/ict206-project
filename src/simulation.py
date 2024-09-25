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
    BIGGEST_CON_ID = max(cons)
    
    # This is the highest ID of our roads.
    SMALLEST_CON_ID = min(cons)
    
    # Floor and Cieling an ID
    FLOOR = SMALLEST_CON_ID    #.id
    CIELING = BIGGEST_CON_ID #.id
    
    # Generate random numbers for our target destination and the beginning destination for the driver.
    currentID = driver.target
    
    while currentID == -1 or currentID < SMALLEST_CON_ID or currentID > BIGGEST_CON_ID:
        currentID = random.randint(FLOOR, CIELING)
        
        # If the driver is cautious...
        if driver.behaviour != road.Behaviour.RECKLESS:
            # And means guaranteed death...
            node = cons[currentID]
            
            # Do not select this node...
            if node.crash > 0.5:
                currentID = -1
    
    # Set our target ID
    targetID = currentID
    while currentID == targetID or (targetID < SMALLEST_CON_ID or targetID > BIGGEST_CON_ID):
        # Get the ID
        targetID = random.randint(FLOOR, CIELING)
        
        # If the driver is cautious...
        if driver.behaviour != road.Behaviour.RECKLESS:
            # And means guaranteed death...
            node = cons[targetID]
            
            # Do not select this node...
            if node.crash > 0.5:
                targetID = -1
    
    # Target and Current
    driver.current = currentID
    driver.target = targetID
    
    on_target(targetID)
    
    # find new path, we want to create a copy to prevent modifying the original 
    path_to_dest = road.find_destination(driver, roads, cons, currentID, targetID)
    driver.path = list(path_to_dest)
    
    # Add the next road.
    this_id = driver.current
    next_id = 0
    
    # If there is something in the queue
    if len(driver.path) > 0:
        next_id = driver.path[0]
    # If we only have one thing left, there is only one jump to make...
    else:
        next_id = driver.target
    
    # Get the nodes
    this_node = cons[this_id]
    next_node = cons[next_id]
    
    # Set the road...
    driver.on_road = road.get_road_between(roads, this_node, next_node)
    # print(driver.id, this_id, next_id, driver.path)
    driver.on_road.drivers += 1

# We will generate the crash likely hoods here in this singleton
class Road_Statistics:
    floor = None 
    ceil = None
    
    def generate(connections):
        floor_id = min(connections, key=lambda con_id: connections[con_id].crash)
        floor_crash = connections[floor_id].crash
        Road_Statistics.floor = floor_crash / 10
        
        ciel_id = max(connections, key=lambda con_id: connections[con_id].crash)
        ciel_crash = connections[ciel_id].crash
        ceil = ciel_crash * 10000
        
        if ceil >= 1.00:
            ceil = 1.00
        
        Road_Statistics.ceil = ceil

# This is the update function it modifies how a driver runs, it runs every tick...
# - road: is the node that the node is across
# - regen_f: is a function that regenerates the path finding
def driver_update(driver, roads, connections, on_crossed, on_target, on_start, on_end):
    # The ID that we are using 
    from_id = driver.current 
    to_id = -1
    
    # If we only have one node in our path...
    if len(driver.path) == 1:
        # Set node IDs
        to_id = driver.path[0]
    elif len(driver.path) > 1:
        # Use pathing
        from_id = driver.path[0]
        to_id = driver.path[1]
    else:
        to_id = driver.target
    
    # These are defines important for the function...
    from_node = connections[from_id]
    to_node   = connections[to_id]
    
    # Get the connection between two roads...
    road_con = driver.on_road # road.get_road_between(roads, from_node, to_node)
   
    # If the driver has finished their trip across a road...
    if driver.progress >= 1.00:
        # Then pop the beginning of the queue and find the next connection to go down
        on_end(road_con.id)
        
        # This is so we actually have the current node in the driver object 
        # Check the intersections crash rate...
        # First we have to find the intersection that we're heading towards
        floor = Road_Statistics.floor
        ceil = Road_Statistics.ceil
        diff = data["float_difference"]
        
        # If we have more nodes we need to visit...
        path_left = len(driver.path)
        
        if path_left > 1:
            # Get nodes 
            this = driver.path[0]
            next = driver.path[1]
            
            driver.path.pop(0)
            
            on_crossed(this)
            driver.current = this
            
            driver.on_road = road.get_road_between(roads, connections[this], connections[next])
            
            # Decrement the amount of drivers on the previous 
            if road_con.drivers > 0:
                road_con.drivers -= 1
        # If we have one or zero
        else:
            # Then set our 
            driver_regenerate(roads, connections, driver, on_target)
            on_start(driver.on_road.id)
        
        rolled_death = road.calculate_survival(driver, road_con, connections, floor, ceil, diff)
        
        # Set the driver death...
        if rolled_death:
            # If the driver died return the function, it wastes clock cycles
            # print(driver.current, driver.target, driver.on_road.id, driver.path)
            driver.died = rolled_death
            
            # # Get the road that the driver died on.
            # r = driver.on_road
            # 
            # # Get the node that they didn't arrive at.
            # for con_id in r.connections:
            #     # If it is not the user.
            #     if con_id != driver.current:
            #         # Set the current value to this node they died at.
            #         driver.current = con_id
            #         break
            # 
            # return
            
        # Now find a new target...
        # Set the target to the next node.
        driver.progress = 0.00
        
        
    # If the progress has no finished
    else:
        # Add to the progress...
        road_length = road_con.length
        road_speed  = road_con.speed
        
        mins_to_hrs = simulation.data["sim_minutes"]
        progress = road_speed / (mins_to_hrs * road_length)
        
        driver.progress += progress
    # End of Driver - Update Function

# Start the simulation   
def begin(roads, cons):
    # Find optimal paths 
    display.print_start_optimal_path()
    road.find_optimal_paths(roads, cons)
    display.print_end_optimal_path()

    # This is data for our driver, contains size and array of all drivers
    # This is not a set as we are going to edit every single driver every single simulation cycle
    # This will result in O(n), therefore we don't care if it is a set.
    drivers_n = uinput.get_driver_amount(display.print_error)
    drivers = {}
    
    # Get the amount of months we're running for (months * 30 * 24 = hours)
    sim_months = uinput.get_sim_time(display.print_error)
    sim_days = sim_months * simulation.data["sim_days"]
    sim_hours = sim_days * simulation.data["sim_hours"] 

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
            "vertex": [],
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
        
    # For all road values 
    i = 0
    for r_id in roads:
        # Add value for node.
        simulation_data["roads"]["vertex"].append({
            "id": r_id,
            "entered": 0,
            "exited": 0
        })
    
    # Generate our floor and ceiling for crash generator...
    Road_Statistics.generate(cons)
    
    
    # Before we start the drivers, we must first initalise our lambda events 
    def on_crossed(node_id):
        simulation_data["intersections"]["nodes"][node_id - 1]["crossed"] += 1
    
    def on_target(node_id):
        simulation_data["intersections"]["nodes"][node_id - 1]["targeted"] += 1
    
    # When we enter a road id
    def on_start(road_id):
        simulation_data["roads"]["vertex"][road_id - 1]["entered"] += 1
    
    def on_end(road_id):
        simulation_data["roads"]["vertex"][road_id - 1]["exited"] += 1
    
    # When a driver dies
    def on_driverDeath(driver):
        # Increment deaths in that connection
        node_id = driver.current
        r = driver.on_road
           
        # Get the ID
        node = cons[node_id]
        
        # Make the connection they died on more dangerous 
        node.deaths += 1
        node.crash += 1/(len(cons)*simulation_data["drivers"]["start"])
        
        simulation_data["intersections"]["nodes"][node_id - 1]["deaths"] += 1
        simulation_data["drivers"]["deaths"] += 1   # Increment death total
        
        # Update the likely hood of death...
        Road_Statistics.generate(cons)
    
    
    
    
    
    
    
    
    # Add the amount of drivers
    for i in range(drivers_n):
        id = i + 1
        driver = road.Driver(-1 , -1)                            # Create driver object
        driver_regenerate(roads, cons, driver, on_target)        # Generate a path...
        
        # Once we've generated the driver...
        # We will set current 
        drivers.update({ id: driver })                           # Append to array
        
    road.set_drivern(drivers_n)
    
    # Amount of iterations per hour...
    minute_hour = range(data["sim_minutes"])
    
    # Run while we have hours to go...
    while hours > 0:
        # Show how much hours there is left to go 
        display.print_hours(hours)
        
        # Used so we don't delete during iteration
        to_delete = set()
        
        # This is every minute for an hour...
        for minute in minute_hour:
            # Do some logic per tick... ##########################
            
            # Check drivers ######################################
            for id in drivers:
                # If not in set
                if not id in to_delete:
                    # Get the driver object 
                    driver = drivers[id]
                    # If driver is not dead...
                    if not driver.died:
                        driver_update(driver, roads, cons, on_crossed, on_target, on_start, on_end)
                    else:
                        to_delete.add(id)
            
            ######################################################=
        
        # Kill all that died 
        if len(to_delete) > 0:
            i = 0
            for id in to_delete:
                driver = drivers[id]
                on_driverDeath(driver)
                
                # Modify our formula 
                r = driver.on_road 
                r.drivers -= 1
                
                # Check if last
                if len(to_delete) - 1 == i:
                    road.set_drivern(len(drivers))
                
                # Remove it from the driver array...
                del drivers[id]
                
                # Increment 
                i += 1
            
            road.drop_saftey_cache()
            killed_before_refresh = False
        
        # Decrement the Hours
        hours = hours - 1
    
    # Save data due to end of simulation 
    
    simulation_data["drivers"]["end"] = len(drivers)
    
    return simulation_data;
    # End of simulation