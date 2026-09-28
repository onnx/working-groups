#include "ctensoruint8.h"
struct ctensor_ui8;


struct ctensor_ui8 ctensor_create_ui8(int32_t * ds, int32_t n) {
  int32_t m;
  uint8_t * vs;
  struct ctensor_ui8 ctensor_ui8;
  m = cdim_size(ds, n);
  vs = malloc(((uint32_t) m) * sizeof(uint8_t));
  ctensor_ui8.t_rank = !vs ? 0 : n;
  ctensor_ui8.t_dims = ds;
  ctensor_ui8.t_data = vs;
  return ctensor_ui8;
}

void ctensor_clear_ui8(struct ctensor_ui8 r) {
  int32_t m, i, o;
  m = cdim_size(r.t_dims, r.t_rank);
  o = m - 1;
  if (0 <= o) {
    for (i = 0; ; ++i) {
      r.t_data[i] = (((uint8_t) 0));
      if (i == o) {
        break;
      }
    }
  }
}

void ctensor_reset_ui8(struct ctensor_ui8 r, uint8_t v) {
  int32_t m, i, o;
  m = cdim_size(r.t_dims, r.t_rank);
  o = m - 1;
  if (0 <= o) {
    for (i = 0; ; ++i) {
      r.t_data[i] = v;
      if (i == o) {
        break;
      }
    }
  }
}

void ctensor_add_ui8(struct ctensor_ui8 a, struct ctensor_ui8 b,
                     struct ctensor_ui8 r) {
  int32_t m, i, o;
  m = cdim_size(r.t_dims, r.t_rank);
  o = m - 1;
  if (0 <= o) {
    for (i = 0; ; ++i) {
      r.t_data[i] = (uint8_t)(a.t_data[i] + b.t_data[i]);
      if (i == o) {
        break;
      }
    }
  }
}
