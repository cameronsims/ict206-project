#include "connection.h"

#include <stdio.h>
#include <stdbool.h>

#include "random.h"

int connection_generate(int connection_amount) {
	// Get Connection.csv
	FILE* conf = fopen(CONNECTION_FILE_NAME, "w");

	// If we cannot read the file...
	if (conf == NULL) {
		// Tell user something went wrong
		printf("ERROR: Cannot write to road.csv!\n");
		return false;
	}

	// Print the head
	fprintf(conf, CONNECTION_FILE_HEAD);

	// Create a new hex
	connection_colour clr;
	clr.r = 0xFF;
	clr.g = 0x00;
	clr.b = 0xCC;

	// Generate all connections
	for (int i = 0; i < connection_amount; i++) {
		// Generate a new color
		clr.r = random_generateInt(0, 0xFF);
		clr.g = random_generateInt(0, 0xFF);
		clr.b = random_generateInt(0, 0xFF);
		// Numbers
		const int id = i + 1;
		const int colour = clr.r * 0x10000 + clr.g * 0x100 + clr.b;
		const double percent = random_generateFloat(0.000001, 0.000090);

		// Print a value
		fprintf(conf, "%d,%06x,%0.06f\n", id, colour, percent);
	}

	return true;
}

int connection_getAmount(int road_amount) {
	// Ask how much intersections
	int value = -1;
	while (value < 1 || value > road_amount) {
		// Ask user 
		printf("How much intersections would you like?: ");
		// Get the input 
		int status = scanf("%d", &value);
		// Get from console
		if (!status || (value < 0 || value > road_amount)) {
			// If we did not get a valid input...
			printf("Please input a valid integer such that 0<=x<=%d\n", road_amount);
			value = -1;
		}
	}

	// Return connection
	return value;
}
