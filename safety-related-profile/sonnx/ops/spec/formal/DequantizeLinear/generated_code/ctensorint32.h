#ifndef CTENSORINT32_H_INCLUDED

#include "cindex.h"

struct ctensor_i32 {
  int32_t t_rank;
  int32_t * t_dims;
  int32_t * t_data;
};

struct ctensor_i32 ctensor_create_i32(int32_t * ds, int32_t n);

void ctensor_clear_i32(struct ctensor_i32 r);

void ctensor_reset_i32(struct ctensor_i32 r, int32_t v);

void ctensor_add_i32(struct ctensor_i32 a, struct ctensor_i32 b,
                     struct ctensor_i32 r);

#define CTENSORINT32_H_INCLUDED
#endif // CTENSORINT32_H_INCLUDED
