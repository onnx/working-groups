#include "ctensoradd.h"

void ctensor_add(struct ctensor a, struct ctensor b, struct ctensor r) {
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
