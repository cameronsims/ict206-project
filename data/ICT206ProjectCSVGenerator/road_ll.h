#ifndef ROAD_LL_H
#define ROAD_LL_H

#include <stdint.h>
#include <stddef.h>

struct road_LinkedListNode {
	int data;
	struct road_LinkedListNode* next;
};

typedef struct road_LinkedListNode road_LinkedListNode;

typedef struct {
	road_LinkedListNode* root;
} road_LinkedList;

typedef void(*road_LinkedListFunc)(int);

int    road_LinkedList_create(road_LinkedList* list);
int    road_LinkedList_size(const road_LinkedList* const list);

int    road_LinkedList_at(road_LinkedList* list, size_t i, int* data);

int    road_LinkedList_insert(road_LinkedList* list, int data);
size_t road_LinkedList_search(road_LinkedList* list, int data);
int    road_LinkedList_remove(road_LinkedList* list, int data);

void   road_LinkedList_foreach(road_LinkedList* list, road_LinkedListFunc func);
void   road_LinkedList_delete(road_LinkedList* list);

#endif