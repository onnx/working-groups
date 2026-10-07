#ifndef CTENSORUINT32_H_INCLUDED

#include "cindex.h"

struct ctensor_ui32 {
  int32_t t_rank;
  int32_t * t_dims;
  uint32_t * t_data;
};

struct ctensor_ui32 ctensor_create_ui32(int32_t * ds, int32_t n);

void ctensor_clear_ui32(struct ctensor_ui32 r);

void ctensor_reset_ui32(struct ctensor_ui32 r, uint32_t v);

void ctensor_add_ui32(struct ctensor_ui32 a, struct ctensor_ui32 b,
                      struct ctensor_ui32 r);

#define CTENSORUINT32_H_INCLUDED
#endif // CTENSORUINT32_H_INCLUDED
