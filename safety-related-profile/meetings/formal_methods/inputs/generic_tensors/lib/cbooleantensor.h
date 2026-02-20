#ifndef CBOOLEANTENSOR_H_INCLUDED

#include <stdlib.h>
#include <stdint.h>
#include "cindex.h"
#include <math.h>

struct ctensor {
  int32_t t_rank;
  int32_t * t_dims;
  int * t_data;
};

struct ctensor ctensor_create(int32_t * ds, int32_t n);

void ctensor_clear(struct ctensor r, int cbackground);

void ctensor_reset(struct ctensor r, int v, int cbackground);

#define CBOOLEANTENSOR_H_INCLUDED
#endif // CBOOLEANTENSOR_H_INCLUDED
