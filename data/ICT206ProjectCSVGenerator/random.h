#ifndef RANDOM_H
#define RANDOM_H

#include <stddef.h>

void random_generateSeed();
int random_generateInt(int floor, int ciel);
double random_generateFloat(double floor, double ciel);

#endif