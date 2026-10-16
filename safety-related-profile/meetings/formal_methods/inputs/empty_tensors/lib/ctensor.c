#include "ctensor.h"
struct ctensor;


struct ctensor ctensor_create(int32_t * ds, int32_t n) {
  int32_t m;
  double * vs;
  struct ctensor ctensor;
  m = cdim_size(ds, n);
  vs = malloc(((uint32_t) m) * sizeof(double));
  ctensor.t_rank = !vs ? 0 : n;
  ctensor.t_dims = ds;
  ctensor.t_data = vs;
  return ctensor;
}

void ctensor_clear(struct ctensor r) {
  int32_t m, i, o;
  m = cdim_size(r.t_dims, r.t_rank);
  o = m - 1;
  if (0 <= o) {
    for (i = 0; ; ++i) {
      r.t_data[i] = ((double) 0.0);
      if (i == o) {
        break;
      }
    }
  }
}

void ctensor_reset(struct ctensor r, double v) {
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

void ctensor_where(struct ctensor cond, struct ctensor a, struct ctensor b,
                   struct ctensor r) {
  int32_t m, i, o;
  m = cdim_size(r.t_dims, r.t_rank);
  o = m - 1;
  if (0 <= o) {
    for (i = 0; ; ++i) {
      r.t_data[i] = ((double) 0.0) < cond.t_data[i] ? a.t_data[i] : b.t_data[i];
      if (i == o) {
        break;
      }
    }
  }
}
