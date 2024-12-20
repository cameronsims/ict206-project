# death.py - Death Calculation
#
# Author: Cameron Sims
# Date: 27/09/2024
#

import random
import math

# This gets the probability to beat.
def death_probability(cons, node, r):

    difference = abs(death_probability.time_mod - death_probability.weather_mod)
    maximum = max(death_probability.time_mod, death_probability.weather_mod)
    modifier = maximum + difference / 2

    n = len(cons)
    a = r.drivers + 1         # Plus one since we just decremented it 
    b = len(node.connections)
    c = 1                     # How much we wish to shift it to the left on the graph
    d = death_probability.d   # Static Variable.
    x = modifier * node.crash            # This is the node that the driver is at.
    
    # Before we do anything, do some bounds checking 
    if x <= 0.0:
        return 0.0
    
    if x >= 1.0:
        return 1.0
    
    denom = (d - a + 1)
    
    if denom == 0:
        denom = 1
       
    if a != 0:
        abn = a*b*pow(n, b/a)
    else:
        abn = b*pow(n, b)
    
    if not abn > 0:
        abn = 1
        
    logabn = math.log(abn)
    
    gx = x * math.exp(logabn*(x - c))
    hx = ((x - c) / denom) + c
    
    # Get final function
    fx = gx * hx
    
    #print(fx, x)
    
    # If somehow our function is larger than 1.00, it won't matter as
    # 1.00 is the max we're measuring and it will be as big as possible
    
    return fx

# This is done in weather modifiers
death_probability.weather_mod = 1.0
death_probability.time_mod = 1.0

# This is a hacky way of setting a global variable, but this is nessassary for the calculation 
# and I don't really feel like passing the amount of drivers everyehere.
def set_drivern(n):
    death_probability.d = n
def get_drivern():
    return death_probability.d 
death_probability.d = 1

# This calculates how the driver crash calculation works 
def calculate_survival(driver, roads, cons, prob_floor, prob_ceil, prob_difference):
    # Get on road.
    r = driver.on_road
    
    # Get other node
    start_node = cons[ driver.current ]
    end_node = None 
    for con_id in r.connections:
        if con_id != start_node.id:
            # Set this, break loop
            end_node = cons[con_id]
            break
    
    if start_node.crash < prob_difference:
        return False
    
    if start_node.crash > (1.00 - prob_difference):
        return True
    
    # We're going to be using this formula...
    # > https://www.desmos.com/calculator/zokuyjyzvt
    fx = death_probability(cons, start_node, r)
    
    # Check if our dice rolled lower 
    dice = random.uniform(prob_floor, prob_ceil)
    
    dies = (dice < fx + prob_difference)
    
    # If fx is within the acceptable difference 
    return dies