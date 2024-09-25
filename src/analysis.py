# analysis.py - Used to give suggestions on how to fix the road.
#
# Author: Cameron Sims
# Date: 19/09/2024
#

import display 
import road

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
    
    print("In the simulation the population is", pop_dec_percent, "percent of the starting population (", pop_start, "->", pop_end, ")")
    
    
    if len(nodes_with_deaths) > 0:
        # Show the total deaths
        print("There was a total of", pop_deaths, "death(s) overall, these deaths were caused at the following intersection ids:")
        # Generate the two deaths...
        for con_id in nodes_with_deaths:
            # Connection ID 
            con = cons[con_id]
            print("    Node ID:", con_id, "had a total of", cons[con_id].deaths, "deaths")
    else:
        print("No deaths occured on the road network.")

def perform_analysis(roads, cons, simulation_data):
    # Seperate simulation and results 
    print()
    
    # State that the analysis is beginning
    display.print_analysis_signature()
    
    # Save session data 
    driver_data = simulation_data["drivers"]
    driver_deaths = driver_data["deaths"]
    
    show_pop_data(roads, cons, simulation_data)
    
    # Tell issues to do with the value 
    for con_id in cons:
        # Get on in question 
        con = cons[con_id]
        
        print("Node ID:", con_id, "( Deaths:", con.deaths, ")")
        has_issues = False
        
        # Give advice for this node, and its roads
        for r_id in con.connections:
            r = roads[r_id]
            p_index = road.death_probability(cons, con, r)
            
            print("    Road ID:")
            
            # P Index is large and big chance for death
            if p_index > 0.005:
                print("       ", r_id, "has a large chance (", p_index, ") of crashing into this node.")
                has_issues = True
                
                # Now lets check why this is so high...
            
            # Print the index for formula...
            n = len(cons)
            b = len(con.connections)
            c = 1
            d = road.death_probability.d
            x = con.crash
            
            numer = str(x) + " * e^[log10(a * " + str(b * n) + ") * " + str(x - c) + "]"
            denom = "[" + str(x - c) + " / (" + str(d + 1) + " * a) + " + str(c) + "]"
            
            print("        p(a) = (" + numer + ") / " + str(denom) + ", { a = # of drivers on connecting road(s) }")
            
        # If the value is disproportionally high
        mean_deaths_per_con = driver_deaths / len(cons)
        if con.deaths > mean_deaths_per_con:
            print("    This node has significantly high amount of deaths proportonally.")
            has_issues = True
        
        # If there is no issues...
        if not has_issues:
            print("    This node has no issues, and crashing likely hood as low.")
    
    # Make a new line after
    print()