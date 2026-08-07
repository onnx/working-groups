#ifndef CTENSORLEAKYRELU_H_INCLUDED

#include <stdlib.h>
#include <stdint.h>
#include "cindex.h"
#include "ctensor.h"

void ctensor_leaky_relu(double alpha, struct ctensor x, struct ctensor r);

#define CTENSORLEAKYRELU_H_INCLUDED
#endif // CTENSORLEAKYRELU_H_INCLUDED
