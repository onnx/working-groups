#include "ctensorint8.h"
struct ctensor_i8;


struct ctensor_i8 ctensor_create_i8(int32_t * ds, int32_t n) {
  int32_t m;
  int8_t * vs;
  struct ctensor_i8 ctensor_i8;
  m = cdim_size(ds, n);
  vs = malloc(((uint32_t) m) * sizeof(int8_t));
  ctensor_i8.t_rank = !vs ? 0 : n;
  ctensor_i8.t_dims = ds;
  ctensor_i8.t_data = vs;
  return ctensor_i8;
}

void ctensor_clear_i8(struct ctensor_i8 r) {
  int32_t m, i, o;
  m = cdim_size(r.t_dims, r.t_rank);
  o = m - 1;
  if (0 <= o) {
    for (i = 0; ; ++i) {
      r.t_data[i] = (((int8_t) 0));
      if (i == o) {
        break;
      }
    }
  }
}

void ctensor_reset_i8(struct ctensor_i8 r, int8_t v) {
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

void ctensor_add_i8(struct ctensor_i8 a, struct ctensor_i8 b,
                    struct ctensor_i8 r) {
  int32_t m, i, o;
  m = cdim_size(r.t_dims, r.t_rank);
  o = m - 1;
  if (0 <= o) {
    for (i = 0; ; ++i) {
      r.t_data[i] = (int8_t)((int)a.t_data[i] + (int)b.t_data[i]);
      if (i == o) {
        break;
      }
    }
  }
}
