#include "road.h"
#include "random.h"

#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>

int road_getAmount() {
	// Ask user how much rows they'd like for their file
	int value = -1;
	// Loop while we don't have a valid value
	while (value < 1) {
		// Ask user
		printf("How much roads would you like?: ");

		// Get from the input
		int status = scanf("%d", &value);

		// Get from console
		if (!status || (value < 0 || value > 256)) {
			// If we did not get a valid input...
			printf("Please input a valid integer such that 1<=x<=256\n");
			value = -1;
		}
	}

	// Return connection
	return value;
}

int road_generate(int road_amount, int connection_amount) {
	// Get Road.csv
	FILE* roadf = fopen(ROAD_FILE_NAME, "w");

	// If we cannot read the file...
	if (roadf == NULL) {
		// Tell user something went wrong
		printf("ERROR: Cannot write to road.csv!\n");
		return false;
	}

	// File works fine...

	// Before we do anything, we need to make sure every node connects to one another.
	// So we will create an array for this.
	//
	// Since we have x amount of roads and y amount of connections where y is always smaller than x.
	// We can set some rules in place.
	//
	// All nodes must connect somehow, so we will first assign all the nodes, and then allow extra connections
	//

	// road_LinkedList notTried;
	// road_LinkedList_create(&notTried);
	// 
	// // Insert all IDS
	// for (int i = 0; i < connection_amount; i++) {
	// 	const id = i + 1;
	// 	road_LinkedList_insert(&notTried, id);
	// }
	// 
	// size_t n = road_LinkedList_size(&notTried);
	
	// Print the head of the CSV file
	fprintf(roadf, ROAD_FILE_HEAD);

	// This is an array, all numbers must be in here at least once
	int* freq = (int*)malloc(connection_amount * sizeof(int)); // Frequency Array
	if (freq == NULL) {
		return false;
	}

	// Set all frequencies to one...
	for (int i = 0; i < connection_amount; i++) {
		freq[i] = 2;
	}

	// Now if we've got more connections to make...
	size_t overdraw = road_amount - connection_amount;
	for (int i = 0; i < overdraw; i++) {
		int left = random_generateInt(0, connection_amount), 
		    right = random_generateInt(0, connection_amount);
		
		// Increment frequencies
		freq[left]++;
		freq[right]++;
		printf("%d %d\n", left, right);
	}


	// Output data perline...
	for (int i = 0; i < road_amount; i++) {
		// This is the ID of this entry
		const int id = i + 1;

		// Print to string buffer
		char name[ROAD_NAME_BUFFER];
		name[ROAD_NAME_BUFFER - 1] = '\0';

		// Generate speed and length of road
		double length = random_generateInt(1, 10) * 10.0,
			   speed = random_generateInt(5, 12) * 10.0;

		int from = -1, to = -1;

		int fromIndex = random_generateInt(0, connection_amount - 1), toIndex = random_generateInt(0, connection_amount - 1);

		// Get some value from the freqency array...
		while (fromIndex == toIndex) {
			do {
				fromIndex = random_generateInt(0, connection_amount - 1);
			} while (freq[fromIndex] < 1);
			
			do {
				toIndex = random_generateInt(0, connection_amount - 1);
			} while (freq[toIndex] < 1);
		}

		freq[fromIndex]--;
		freq[toIndex]--;

		// Now set the id
		from = fromIndex + 1;
		to = toIndex + 1;

		sprintf(name, ROAD_NAME_FORMAT, id);

		fprintf(roadf, "%d,%s,%0.02f,%0.2f,%d,%d\n", id, name, length, speed, from, to);
	}


	// Tell user successfully read
	printf("Road file has successfully been read!\n");

	// Close the file to save forever, and free up some memory 
	//road_LinkedList_delete(&notTried);
	free(freq);
	fclose(roadf);

	return true;
}

size_t road_isInArray(int* arr, size_t n, int value) {
	for (int i = 0; i < n; i++) {
		if (arr[i] == value) {
			return i;
		}
	}
	return n;
}