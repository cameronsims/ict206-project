# display.py - Functions relating to displaying to user
#
# Author: Cameron Sims
# Date: 14/08/2024
#

# Console Imports
import colorama as clr  # Used for colouring the console

def default_colour_code():
    return clr.Style.NORMAL + clr.Fore.WHITE + clr.Back.BLACK

def default_colour():
    print(default_colour_code(), end="")
    
def node_colour_code():
    return clr.Fore.WHITE + clr.Back.RED

def road_colour_code():
    return clr.Fore.WHITE + clr.Back.BLUE
    
def formula_colour_code():
    return clr.Style.DIM + clr.Fore.WHITE + clr.Back.BLUE
    
def get_formula_string():
    prior = formula_colour_code()
    after = default_colour_code()
    print(prior + "a: # of near drivers, w: weather modifier" + after)

def print_signature():
    colour = clr.Fore.WHITE + clr.Back.BLUE
    defclr = default_colour_code()
    print(colour + "+---------------------------------------+" + defclr)
    print(colour + "|                                       |" + defclr)
    print(colour + "| ICT206 - Intelligent Systems: Project |" + defclr)
    print(colour + "|        Cameron Sims (34829454)        |" + defclr)
    print(colour + "|                                       |" + defclr)
    print(colour + "+---------------------------------------+" + defclr)
    default_colour()
    
def print_analysis_signature():
    colour = clr.Fore.YELLOW + clr.Back.RED
    defclr = default_colour_code()
    print()
    print(colour + "+---------------------------------------+" + defclr)
    print(colour + "|                                       |" + defclr)
    print(colour + "|          Performing Analysis          |" + defclr)
    print(colour + "|                                       |" + defclr)
    print(colour + "+---------------------------------------+" + defclr)
    default_colour()
    
def print_error(str):
    print(clr.Fore.WHITE + clr.Back.RED + "! ERROR: " + str)
    default_colour()
    
def print_connection_begin():
    print("+ Reading Connections...")
    
def print_connection_end():
    print("- Connections Read!")

def print_pyvis_begin():
    print("+ Creating Python Graph:")
    
def print_pyvis_end():    
    print("- Python Graph Has Concluded!")
    
def print_hours(start_hours, hours, start_population, population, weather_str): 
    hours_str = str(hours)
    print("There are " + hours_str + " hours left!", end=" ")
    print('(' + hours_str + '/' + str(start_hours) + ")", end=" ")
    print('(' + str(population) + "/" + str(start_population) + ')', end=" ")
    print("(" + weather_str + ")")
 

 
def print_formula(n, b, c, d, x):
    
    rnd_to = 3
    numer = "w*" + str(round(x, 2)) + "e^[" + str(round(x - c, rnd_to)) + "log10(" + str(round(b * n, rnd_to)) + "a)]"
    denom = "[" + str(round(x - c, rnd_to)) + " / (" + str(round(d + 1, rnd_to)) + "a) + " + str(round(c, rnd_to)) + "]"
            
    print("    p(a) = (" + numer + ") / " + str(denom), "|", get_formula_string())
    
    
    
def print_pops(pop_dec_percent, pop_start, pop_end):
    print("In the simulation the population is", pop_dec_percent, "percent of the starting population (", pop_start, "->", pop_end, ")")



def print_deaths(pop_deaths):
    print("There was a total of", pop_deaths, "death(s) overall, these deaths were caused at the following intersection ids:")
    
def print_deaths_on_node(node_id, deaths):
    print("    Node ID:", node_id, "had a total of", deaths, "deaths")

def print_no_deaths_on_any_node():
    print("No deaths occured on the road network.")

def print_node_head(con_id, deaths):
    print(node_colour_code() + "Node ID:", con_id, "( Deaths:", deaths, ")" + default_colour_code())

def print_road_head(r_id):
    print("    " + road_colour_code() + "Road ID:", str(r_id) + default_colour_code())
    
def print_road_big_danger(p_index):
    print("        This road has a large chance (", p_index, ") of crashing into this node.")
    
def print_node_big_danger():
    print("    This node has significantly high amount of deaths proportonally.")
    
def print_node_no_issues():
    print("    This node has no issues, and crashing likely hood as low.")
    
def print_driver_behaviour_deaths(name, deaths, pops):
    print(name + ":", deaths, "from", pops)
    
    
    
def print_start_optimal_path():
    print("Calculating optimal paths...")

def print_end_optimal_path():
    print("Calculated all paths...")
    
def print_results(simulation_data):
    print("Simulation Results:")
    def get_indent(it):
        # Indent amount 
        indent = ""
        for i in range(it):
            indent += "   "
        return indent
    
    def print_needed(data):
        if type(data) is dict:
            return True
        if type(data) is list:
            return True 
        return False
    
    def print_type(data, it):
        indent = get_indent(it)
        
        if type(data) is dict:
            print(indent + '{')
            print_obj(data, it + 1)
            print(indent + '}')
            
        elif type(data) is list:
            print(indent + '[')
            print_arr(data, it + 1)
            print(indent + ']')
            
        else:
            print(indent + str(data))
    
    def print_arr(arr, it):
        # For all values...
        for value in arr:
            print_type(value, it)
        
    def print_obj(obj, it):
        # Indent amount 
        indent = get_indent(it)
        
        # Print object key and value 
        for key, value in obj.items():
            # The name of the value 
            name = indent + str(key).title() + ": "
            
            # Check if the value is an object  
            if (print_needed(value)):
                print(name)
                print_type(value, it)
            else:
                print(name + str(value))
    
    print_type(simulation_data, 0)
    
    #print("  Drivers:")
    #print("      Population (Start): ", simulation_data["drivers"]["start"])
    #print("      Population (End):   ", simulation_data["drivers"]["end"])
    #print("      Total Deaths:       ", simulation_data["drivers"]["deaths"])
    #print("  Roads:")
    #print("      Amount:             ", simulation_data["roads"]["length"])
    #print("  Intersections:")
    #print("      Amount:             ", simulation_data["intersections"]["length"])


