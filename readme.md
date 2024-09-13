### ICT206 - Project
# Created by Cameron Sims 

## How to install properly
Install Pyvis to show network
https://pyvis.readthedocs.io/en/latest/

## How The Simulation Works
The program is a simulation of "roads" where there are several "drivers" who will "drive" across these road nodes over the course of a period of time.
The drivers will decide on a node to drive towards, once they reach this node they will select a new node this will repeat until death or simulation ends.
An amount of variables will be calculated depending on what rules and variables are input (for example a high-fatality rate on one vehicle will cause significantly more deaths than a low-fatality rate).
There are a number of events (crashes, deaths, etc) which can happen on any road node. These will alter how the Artifical Intelligence will function and how the simulation plays out.

## How To Change The Simulation
# Files
There is a variable file (located in ./data/variables.txt) which is important as it defines important behaviour and statistical probablity. Changing any one of these variables will alter how the simulation will function, and likelyhoods of events happening.
If any file that is required for running is not existant or contains illogical data, the simulation will either quit and tell you that it requires a file or needs modification of a value.