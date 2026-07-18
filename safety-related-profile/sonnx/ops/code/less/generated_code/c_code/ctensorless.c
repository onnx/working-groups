#include "ctensorless.h"

void ctensor_less(struct ctensor x, struct ctensor y, struct ctensor r) {
  int32_t m, i, o;
  m = cdim_size(r.t_dims, r.t_rank);
  o = m - 1;
  if (0 <= o) {
    for (i = 0; ; ++i) {
      r.t_data[i] = x.t_data[i] < y.t_data[i] ? ((double) 1.0) : ((double) 0.0);
      if (i == o) {
        break;
      }
    }
  }
}
