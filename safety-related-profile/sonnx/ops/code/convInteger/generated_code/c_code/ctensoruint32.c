#include "ctensoruint32.h"
struct ctensor_ui32;


struct ctensor_ui32 ctensor_create_ui32(int32_t * ds, int32_t n) {
  int32_t m;
  uint32_t * vs;
  struct ctensor_ui32 ctensor_ui32;
  m = cdim_size(ds, n);
  vs = malloc(((uint32_t) m) * sizeof(uint32_t));
  ctensor_ui32.t_rank = !vs ? 0 : n;
  ctensor_ui32.t_dims = ds;
  ctensor_ui32.t_data = vs;
  return ctensor_ui32;
}

void ctensor_clear_ui32(struct ctensor_ui32 r) {
  int32_t m, i, o;
  m = cdim_size(r.t_dims, r.t_rank);
  o = m - 1;
  if (0 <= o) {
    for (i = 0; ; ++i) {
      r.t_data[i] = (((uint32_t) 0));
      if (i == o) {
        break;
      }
    }
  }
}

void ctensor_reset_ui32(struct ctensor_ui32 r, uint32_t v) {
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

void ctensor_add_ui32(struct ctensor_ui32 a, struct ctensor_ui32 b,
                      struct ctensor_ui32 r) {
  int32_t m, i, o;
  m = cdim_size(r.t_dims, r.t_rank);
  o = m - 1;
  if (0 <= o) {
    for (i = 0; ; ++i) {
      r.t_data[i] = a.t_data[i] + b.t_data[i];
      if (i == o) {
        break;
      }
    }
  }
}
