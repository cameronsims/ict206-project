#ifndef CONNECTION_H
#define CONNECTION_H

#include <stdint.h>
#include <stddef.h>

#define CONNECTION_FILE_NAME "../connections.csv"
#define CONNECTION_FILE_HEAD "id,colour,crash\n"

typedef struct {
	uint8_t r,
		    g,
		    b;
} connection_colour;

int connection_generate(int connection_amount);
int connection_getAmount(int road_amount);

#endif