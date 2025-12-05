#ifndef CTENSOR_H_INCLUDED

#include <stdlib.h>
#include <stdint.h>
#include "cindex.h"

struct ctensor {
  int32_t t_rank;
  int32_t* t_dims;
  double* t_data;
};

struct ctensor ctensor_create(int32_t* ds, int32_t n);

void ctensor_clear(struct ctensor r);

void ctensor_reset(struct ctensor r, double v);

void ctensor_where(struct ctensor cond, struct ctensor a, struct ctensor b,
                   struct ctensor r);

void ctensor_add(struct ctensor a, struct ctensor b, struct ctensor r);

void ctensor_conv2d(struct ctensor x, struct ctensor w, struct ctensor b,
                    int32_t pad_top, int32_t pad_bottom, int32_t pad_left,
                    int32_t pad_right, int32_t dil_h, int32_t dil_w,
                    int32_t str_h, int32_t str_w, struct ctensor output);

#define CTENSOR_H_INCLUDED
#endif // CTENSOR_H_INCLUDED
