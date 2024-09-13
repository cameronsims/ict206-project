#ifndef ROAD_H
#define ROAD_H

#include "road_ll.h"

#include <stddef.h>


#define ROAD_FILE_NAME "../roads.csv"
#define ROAD_FILE_HEAD "id,name,length,speed,from,to\n"
#define ROAD_NAME_BUFFER 16
#define ROAD_NAME_FORMAT "Road #%d"

int road_getAmount();
int road_generate(int road_amount, int connection_amount);

size_t road_isInArray(int* arr, size_t n, int value);

#endif