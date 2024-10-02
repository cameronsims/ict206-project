# ICT206 - Project
### Created by Cameron Sims 

## How to install properly
### Install Pyvis 
Install Pyvis to show network HTML
https://pyvis.readthedocs.io/en/latest/

### Install Network X
Install NetworkX for functionality with Pyvis
https://networkx.org/documentation/stable/index.html

## How The Simulation Works
The program is a simulation of "roads" where there are several "drivers" who will "drive" across these road nodes over the course of a period of time.
The drivers will decide on a node to drive towards, once they reach this node they will select a new node this will repeat until death or simulation ends.
An amount of variables will be calculated depending on what rules and variables are input (for example a high-fatality rate on one vehicle will cause significantly more deaths than a low-fatality rate).
There are a number of events (crashes, deaths, etc) which can happen on any road node. These will alter how the Artifical Intelligence will function and how the simulation plays out.
The drivers use A* path finding to find their way to the node, these are saved in a big map which stores the distances. If the driver wishes for the safest way, and a driver dies. All paths are then recalculated on the tick after.

## How To Change The Simulation
### Roads and Connections
In the "data" directory, there is connections.csv and roads.csv which have the vertexes and nodes of the simulation. You can create vertexes by adding a new row in the file and giving it appropriate column data. You can create new nodes by adding a new row in the connections file. Each road must refer to a "from" and "to" node which are the connections between road intersections.
### Weather
Weather and it's effects can be modified in the weather.csv file, new additions must also be added in the Enum. Extra behaviour must be added into the actual program itself.
Also in the "data" directory, is "sim_data.json" which modifies certain variables to do with the simulation, it is not suggested to edit these as they are usually static variables.