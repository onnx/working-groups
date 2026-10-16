#ifndef CTENSORSOFTMAX_H_INCLUDED

#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <math.h>
#include "cindex.h"
#include "ctensor.h"

int same_dims(struct ctensor x, struct ctensor r);

int32_t product_dims_range(int32_t * dims, int32_t first, int32_t last);

int c_softmax(struct ctensor x, struct ctensor r, int32_t axis);

#define CTENSORSOFTMAX_H_INCLUDED
#endif // CTENSORSOFTMAX_H_INCLUDED
