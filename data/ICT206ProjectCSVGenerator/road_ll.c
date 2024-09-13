#include "road_ll.h"

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <memory.h>

// Linked List stuff

int road_LinkedList_create(road_LinkedList* list) {
	// No data is provided, so set to null.
	list->root = NULL;

	// If we add stuff... add it here...
	return true;
}

int road_LinkedList_size(const road_LinkedList* const list) {
	if (list->root == NULL) {
		return 0;
	} else {
		// Find where it is null...
		struct road_LinkedListNode* node = list->root;
		size_t i = 1;

		while (node->next != NULL) {
			node = node->next;
			i++;
		}

		return i;
	}
}

int road_LinkedList_at(road_LinkedList* list, size_t i, int* data) {
	const size_t n = road_LinkedList_size(list);
	if (list->root == NULL || n >= i) {
		return false;
	} else {
		// Check for all values
		struct road_LinkedListNode* node = list->root;
		size_t j = 0;
		while (i != j) {
			if (node == NULL) {
				return false;
			}
			// Otherwise, increment and continue...
			node = node->next;
			j++;
		}

		// Set this node to the data
		*data = node->data;
		return true;
	}
}

int road_LinkedList_insert(road_LinkedList* list, int data) {
	if (list->root == NULL) {
		// Insert it at the beginning...
		list->root = (road_LinkedListNode*)malloc(sizeof(road_LinkedListNode));
		if (list->root != NULL) {
			list->root->data = data;
			list->root->next = NULL;
		}
	} else {
		// Find where it is null...
		struct road_LinkedListNode* node = list->root;
		while (node->next != NULL) {
			// Go to next
			node = node->next;
		}

		// Once we find it, insert some sort of data here.
		node->next = (struct road_LinkedListNode*)malloc(sizeof(struct road_LinkedListNode));
		node->next->data = data;
		node->next->next = NULL;
	}

	return true;
}

size_t road_LinkedList_search(road_LinkedList* list, int data) {
	// Check if root is NULL
	if (list->root == NULL) {
		// Then we failed
		return -1;
	} else {
		// Check for all values
		struct road_LinkedListNode* node = list->root;
		size_t i = 0;
		while (node != NULL) {
			// Check this...
			if (node->data == data) {
				// If it is
				return i;
			}

			// Otherwise, increment and continue...
			node = node->next;
			i++;
		}

		// If we found the end and failed...
		return -1;
	}
}

int road_LinkedList_remove(road_LinkedList* list, int data) {
	// Check if root is NULL
	if (list->root == NULL) {
		// Then it doesn't exist...
		return false;
	} else {
		// Check for all values
		if (list->root->data == data) {
			// Delete the root
			road_LinkedListNode* after = list->root->next;
			
			list->root->next = NULL;
			free(list->root);

			list->root = after;

			return true;
		}

		road_LinkedListNode* node = list->root;
		while (node->next != NULL) {
			// Check if next value is it.
			if (node->next->data == data) {
				// Keep next
				road_LinkedListNode* after = node->next->next;
				
				// Set to null to avoid mass freeing
				node->next->next = NULL;
				free(node->next);

				// Add
				node->next = after;
				return true;
			}

			// Set next
			node = node->next;
		}

		// If we found the end and failed...
		return false;
	}
}

void road_LinkedList_foreach(road_LinkedList* list, road_LinkedListFunc func) {
	if (list->root != NULL) {
		// Find where it is null...
		struct road_LinkedListNode* node = list->root;
		while (node != NULL) {
			// Go to next
			func(node->data);
			node = node->next;
		}
	}
}

void road_LinkedList_delete(road_LinkedList* list) {
	// If the data is not null...
	if (list->root != NULL) {
		// Free all the data... starting from end...
		size_t size = road_LinkedList_size(list);
		road_LinkedListNode** delarr = (road_LinkedListNode*)malloc(size * sizeof(road_LinkedListNode*));
		if (delarr != NULL || size == 0) {	
			// Read the LinkedList
			road_LinkedListNode** node = &(list->root);
			for (int i = 0; i < size; i++) {
				// Add element to array
				delarr[i] = *node;
				node = &((*node)->next);
			}

			for (int i = size - 1; i != 0; i--) {
				free(delarr[i]);
			}

			free(delarr);
		}
	}
}