# weather.py - The weather, dictates how much crashes and speed
#
# Author: Cameron Sims
# Date: 27/09/2024
#

from enum import Enum
import random

# The weather enumeration.
class Weather(Enum):
    NORMAL = 0
    RAINING = 1
    HAIL = 2
    THUNDERSTORM = 3
    SNOWING = 4
    WINDY = 5
    SAND_STORM = 6
    
# This is a static variable that relates to the percentages of the weather...
# Used because Enums suck in python.
WEATHER_ARR = [ "NORMAL", "RAINING", "HAIL", "THUNDERSTORM", "SNOWING", "WINDY", "SAND_STORM" ]
WEATHER_N = len(WEATHER_ARR)
Weather.percentages = list( range(WEATHER_N) )  
Weather.speed_modifiers = list( range(WEATHER_N) ) 
Weather.crash_modifiers = list( range(WEATHER_N) ) 

# Gets how the drivers speed will be impacted.
def speed_modifier(w):
    return Weather.speed_modifiers[w.value]

# Gets how the death probability will be impacted
def death_modifier(w):
    return Weather.crash_modifiers[w.value]



# Gets the weather (index of WEATHER_ARR)
def get_weather():
    a = Weather.percentages
    x = random.uniform(0.00, 1.00)
    
    # If it is smaller than start and zero
    if 0 <= x <= a[0]:
        return Weather(0)
    
    # For all in the range...
    for i in range(WEATHER_N - 1):
        # If a[i] <= x < a[i + 1]
        if a[i] <= x and x < a[i + 1]:
            return Weather(i + 1)
    return Weather(WEATHER_N - 1)

# This is the Time enum.
class Time(Enum):
    EARLY_MORNING = 0
    MORNING = 1
    EVENING = 2
    NIGHT = 3
TIME_ARR = ["EARLY_MORNING", "MORNING", "EVENING", "NIGHT"]
TIME_N = len(TIME_ARR)

# This calculates what time of day we're at 
def time_of_day(hour):
    # Get the hour in the day.
    rel_hr = hour % 24
    
    # 00-06: Early-Morning
    # 07-12: Morning
    # 13-18: Evening
    # 19-23: Night
    
    # If it is early morning
    if rel_hr < 7:
        return Time.EARLY_MORNING
    # If it is morning
    elif rel_hr < 13:
        return Time.MORNING
    # If it is in the evening
    elif rel_hr < 19:
        return Time.EVENING
    # If it is late night
    else:
        return Time.NIGHT