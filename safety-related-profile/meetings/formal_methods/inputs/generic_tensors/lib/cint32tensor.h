#ifndef CINT32TENSOR_H_INCLUDED

#include <stdlib.h>
#include <stdint.h>
#include "cindex.h"
#include <math.h>

struct ctensor {
  int32_t t_rank;
  int32_t * t_dims;
  int32_t * t_data;
};

struct ctensor ctensor_create(int32_t * ds, int32_t n);

void ctensor_clear(struct ctensor r, int32_t cbackground);

void ctensor_reset(struct ctensor r, int32_t v, int32_t cbackground);

#define CINT32TENSOR_H_INCLUDED
#endif // CINT32TENSOR_H_INCLUDED
