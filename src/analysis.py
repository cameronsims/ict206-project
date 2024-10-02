# analysis.py - Used to give suggestions on how to fix the road.
#
# Author: Cameron Sims
# Date: 19/09/2024
#

import display 
import road
import death

def get_intersections_with_deaths(cons):
    # This is the array we're using to gather
    nodes = []
    for con_id in cons:
        # Connection 
        c = cons[con_id]
        
        # If the connection has a death add it...
        if c.deaths > 0:
            nodes.append(con_id)
    # Return the result 
    return nodes

def show_pop_data(roads, cons, simulation_data):
    # Save session data 
    driver_data = simulation_data["drivers"]
    
    # Get pop data
    pop_start = driver_data["start"] 
    pop_deaths = driver_data["deaths"]
    pop_end = driver_data["end"] 
    
    # Show decrease percent
    pop_dec_percent = 100 * (pop_end / pop_start)
    
    # Get nodes with deaths in them
    nodes_with_deaths = get_intersections_with_deaths(cons)
    
    display.print_pops(pop_dec_percent, pop_start, pop_end)
    
    
    if len(nodes_with_deaths) > 0:
        # Show the total deaths
        display.print_deaths(pop_deaths)
        
        # Generate the two deaths...
        for con_id in nodes_with_deaths:
            # Connection ID 
            con = cons[con_id]
            display.print_deaths_on_node(con_id, cons[con_id].deaths)
    else:
        display.print_no_deaths_on_any_node()

def show_driver_behaviour(simulation_data):
    driver_behav = simulation_data["drivers"]["behaviours"]
    for bname in driver_behav:
        type = driver_behav[bname]
        display.print_driver_behaviour_deaths(bname, type["deaths"], type["population"])

def perform_analysis(roads, cons, simulation_data):
    
    # State that the analysis is beginning
    display.print_analysis_signature()
    
    # Save session data 
    driver_data = simulation_data["drivers"]
    driver_deaths = driver_data["deaths"]
    
    show_pop_data(roads, cons, simulation_data)
    show_driver_behaviour(simulation_data)
    
    # Tell issues to do with the value 
    for con_id in cons:
        # Get on in question 
        con = cons[con_id]
        
        display.print_node_head(con_id, con.deaths)
        has_issues = False
        
        # CALCULATE VALUES 
        n = len(cons)
        b = len(con.connections)
        c = 1
        d = death.death_probability.d
        x = con.crash
        display.print_formula(n, b, c, d, x)
        
        # Give advice for this node, and its roads
        for r_id in con.connections:
            r = roads[r_id]
            
            p_index = death.death_probability(cons, con, r)
            display.print_road_head(r_id)
        
            # P Index is large and big chance for death
            if p_index > 0.005:
                display.print_road_big_danger(p_index)
                has_issues = True
            
        # If the value is disproportionally high
        mean_deaths_per_con = driver_deaths / len(cons)
        if con.deaths > mean_deaths_per_con:
            display.print_node_big_danger()
            has_issues = True
        
        # If there is no issues...
        if not has_issues:
            display.print_node_no_issues()