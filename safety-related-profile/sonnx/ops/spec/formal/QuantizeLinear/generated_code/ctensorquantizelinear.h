#ifndef CTENSORQUANTIZELINEAR_H_INCLUDED

#include <math.h>
#include "ctensor.h"
#include "ctensoruint8.h"

void ctensor_quantize_linear(struct ctensor x, float scale,
                             uint8_t zero_point, struct ctensor_ui8 r);

#define CTENSORQUANTIZELINEAR_H_INCLUDED
#endif // CTENSORQUANTIZELINEAR_H_INCLUDED
