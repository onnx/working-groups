#ifndef CTENSORINT8_H_INCLUDED

#include "cindex.h"

struct ctensor_i8 {
  int32_t t_rank;
  int32_t * t_dims;
  int8_t * t_data;
};

struct ctensor_i8 ctensor_create_i8(int32_t * ds, int32_t n);

void ctensor_clear_i8(struct ctensor_i8 r);

void ctensor_reset_i8(struct ctensor_i8 r, int8_t v);

void ctensor_add_i8(struct ctensor_i8 a, struct ctensor_i8 b,
                    struct ctensor_i8 r);

#define CTENSORINT8_H_INCLUDED
#endif // CTENSORINT8_H_INCLUDED
