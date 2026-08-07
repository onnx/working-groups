#ifndef CTENSORINT_H_INCLUDED

#include "cindex.h"

struct ctensorint {
  int32_t t_rank;
  int32_t * t_dims;
  int32_t * t_data;
};

struct ctensorint mk_ctensorint(int32_t r, int32_t * d, int32_t * v);

struct ctensorint ctensor_create(int32_t * ds, int32_t n);

void ctensor_clear(struct ctensorint r);

void ctensor_reset(struct ctensorint r, int32_t v);

#define CTENSORINT_H_INCLUDED
#endif // CTENSORINT_H_INCLUDED
