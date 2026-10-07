#include "ctensorint32.h"
struct ctensor_i32;


struct ctensor_i32 ctensor_create_i32(int32_t * ds, int32_t n) {
  int32_t m;
  int32_t * vs;
  struct ctensor_i32 ctensor_i32;
  m = cdim_size(ds, n);
  vs = malloc(((uint32_t) m) * sizeof(int32_t));
  ctensor_i32.t_rank = !vs ? 0 : n;
  ctensor_i32.t_dims = ds;
  ctensor_i32.t_data = vs;
  return ctensor_i32;
}

void ctensor_clear_i32(struct ctensor_i32 r) {
  int32_t m, i, o;
  m = cdim_size(r.t_dims, r.t_rank);
  o = m - 1;
  if (0 <= o) {
    for (i = 0; ; ++i) {
      r.t_data[i] = (((int32_t) 0));
      if (i == o) {
        break;
      }
    }
  }
}

void ctensor_reset_i32(struct ctensor_i32 r, int32_t v) {
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

void ctensor_add_i32(struct ctensor_i32 a, struct ctensor_i32 b,
                     struct ctensor_i32 r) {
  int32_t m, i, o;
  m = cdim_size(r.t_dims, r.t_rank);
  o = m - 1;
  if (0 <= o) {
    for (i = 0; ; ++i) {
      r.t_data[i] = (int32_t)((uint32_t)a.t_data[i] + (uint32_t)b.t_data[i]);
      if (i == o) {
        break;
      }
    }
  }
}
