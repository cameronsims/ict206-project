# display.py - Functions relating to displaying to user
#
# Author: Cameron Sims
# Date: 14/08/2024
#

# Console Imports
import colorama as clr  # Used for colouring the console

def default_colour():
    print(clr.Fore.WHITE + clr.Back.BLACK)

def print_signature():
    print(clr.Fore.WHITE + clr.Back.BLUE + "+---------------------------------------+")
    print("|                                       |")
    print("| ICT206 - Intelligent Systems: Project |")
    print("|        Cameron Sims (34829454)        |")
    print("|                                       |")
    print("+---------------------------------------+")
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
    
def print_hours(hours): 
    print("There are " + str(hours) + " hours left!")
    
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