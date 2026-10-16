#ifndef CTENSORDEQUANTIZELINEAR_H_INCLUDED

#include <math.h>
#include "ctensor.h"
#include "ctensorint32.h"

void ctensor_dequantize_linear(struct ctensor_i32 x, float scale,
                               int32_t zero_point, struct ctensor r);

#define CTENSORDEQUANTIZELINEAR_H_INCLUDED
#endif // CTENSORDEQUANTIZELINEAR_H_INCLUDED
