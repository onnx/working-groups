#ifndef CTENSOR_H_INCLUDED

#include <stdlib.h>
#include <stdint.h>
#include "cindex.h"

struct ctensor {
  int32_t t_rank;
  int32_t * t_dims;
  double * t_data;
};

struct ctensor ctensor_create(int32_t * ds, int32_t n);

void ctensor_clear(struct ctensor r);

void ctensor_reset(struct ctensor r, double v);

#define CTENSOR_H_INCLUDED
#endif // CTENSOR_H_INCLUDED
