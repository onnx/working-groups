#include "ctensorint.h"
struct ctensorint;


struct ctensorint mk_ctensorint(int32_t r, int32_t * d, int32_t * v) {
  struct ctensorint ctensorint;
  ctensorint.t_rank = r;
  ctensorint.t_dims = d;
  ctensorint.t_data = v;
  return ctensorint;
}

struct ctensorint ctensor_create(int32_t * ds, int32_t n) {
  int32_t m;
  int32_t * vs;
  m = cdim_size(ds, n);
  vs = malloc(((uint32_t) m) * sizeof(int32_t));
  return mk_ctensorint(!vs ? 0 : n, ds, vs);
}

void ctensor_clear(struct ctensorint r) {
  int32_t m, i, o;
  m = cdim_size(r.t_dims, r.t_rank);
  o = m - 1;
  if (0 <= o) {
    for (i = 0; ; ++i) {
      r.t_data[i] = 0;
      if (i == o) {
        break;
      }
    }
  }
}

void ctensor_reset(struct ctensorint r, int32_t v) {
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
