#include "random.h"

#include <stdlib.h>
#include <time.h>

#include <stdint.h>
#include <math.h>

void random_generateSeed() {
	// Create a new seed, this will help us make more random numbers
	time_t timestamp = time(NULL);
	srand(timestamp);
}

int random_generateInt(int floor, int ciel) {
	// Now we will get the difference between the integers
	const int DIFFERENCE = abs(ciel - floor);

	// Get the random number
	int random = rand();

	// Divide
	int random_range = random % DIFFERENCE;

	// Add floor
	int random_floor = random_range + floor;

	return random_floor;
}

double random_generateFloat(double floor, double ciel) {
	

	// This is a C-define of the highest number possible
	// This is useful in floats as it helps caps our number.
	const int16_t RANDOM_MAX = RAND_MAX;	// 0x7FFF = 32767
	const float RANDOM_MAX_FLOAT = (double)RANDOM_MAX;

	// Get the difference between our floats
	const double DIFFERENCE = fabs(ciel - floor);

	// Since we want to get all possible, we can divide the value
	//     with our maximum, we can get a floating point value which is
	//     at the highest point of our difference
	const double DENOMINATOR = RANDOM_MAX_FLOAT / DIFFERENCE;

	// This is our random number, converted to a double precision float.
	double random = (double)rand();

	// Now we will divide our random by our denomiator.
	double random_range = random / DENOMINATOR;

	// Now we will add values to our floating point so now the value is 
	//     at least at its minimum
	double random_final = random_range + floor;

	// Return the random
	return random_final;
}