#ifndef CTENSORUINT8_H_INCLUDED

#include "cindex.h"

struct ctensor_ui8 {
  int32_t t_rank;
  int32_t * t_dims;
  uint8_t * t_data;
};

struct ctensor_ui8 ctensor_create_ui8(int32_t * ds, int32_t n);

void ctensor_clear_ui8(struct ctensor_ui8 r);

void ctensor_reset_ui8(struct ctensor_ui8 r, uint8_t v);

void ctensor_add_ui8(struct ctensor_ui8 a, struct ctensor_ui8 b,
                     struct ctensor_ui8 r);

#define CTENSORUINT8_H_INCLUDED
#endif // CTENSORUINT8_H_INCLUDED
