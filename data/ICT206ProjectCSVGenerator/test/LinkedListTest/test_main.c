#include "../../road_ll.h"

#include <stdio.h>
#include <stdlib.h>

void print(int data) {
	printf("%d ", data);
}

int main() {

	road_LinkedList list;

	road_LinkedList_create(&list);

	road_LinkedList_foreach(&list, print);

	size_t n = road_LinkedList_size(&list);
	printf("\nSIZE: %llu\n", n);

	for (int i = 0; i < 10; i++) {
		int status = road_LinkedList_insert(&list, i);
		if (!status) {
			return 1;
		}
	}

	road_LinkedList_foreach(&list, print);

	n = road_LinkedList_size(&list);
	printf("\nSIZE: %llu\n", n);

	for (int i = 0; i < 10; i++) {
		size_t value = road_LinkedList_search(&list, i);
		if (value > n) {
			printf("Can't find \"%d\"\n", i);
			return 2;
		}
	}

	road_LinkedList_foreach(&list, print);

	n = road_LinkedList_size(&list);
	printf("\nSIZE: %llu\n", n);

	const int arr[3] = { 3, 6, 9 };
	for (int i = 0; i < 3; i++) {
		int status = road_LinkedList_remove(&list, arr[i]);
		if (!status) {
			return 3;
		} else {
			road_LinkedList_foreach(&list, print);
			n = road_LinkedList_size(&list);
			printf("\nSIZE: %llu\n", n);
		}
	}

	printf("\n\n");

	for (int i = 0; i < 10; i++) {
		road_LinkedList_foreach(&list, print);
		int status = road_LinkedList_remove(&list, i);
		printf("\n");
		road_LinkedList_foreach(&list, print);
		if (!status) {
			n = road_LinkedList_size(&list);
			printf("\nSIZE: %llu\n", n);
		}
		printf("\nNEXT DELETION!\n");
	}

	road_LinkedList_delete(&list);

	return 0;
}