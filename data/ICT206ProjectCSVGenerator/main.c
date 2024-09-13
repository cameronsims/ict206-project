// Author: Cameron Sims
// Date: 20/08/2024

#include "connection.h"
#include "road.h"
#include "random.h"

// Program begins here!
int main(int argc, char** argv) {

	// Generate a new seed, helps us make random generation
	random_generateSeed();

	
	// Only check if we have one argument
	if (argc < 2) {
		// Ask user how much rows they'd like for their file
		const int road_amount = road_getAmount();

		// Ask how much intersections
		const int connection_amount = connection_getAmount(road_amount);

		// Generate road
		int road_status = road_generate(road_amount, connection_amount);
		if (!road_status) {
			return 1;
		}

		// Generate road
		int connection_status = connection_generate(connection_amount);
		if (!connection_status) {
			return 1;
		}
	}

	// Return success
	return 0;
}