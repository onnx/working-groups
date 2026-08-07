#include "copflatten.h"

void flatten(struct ctensor x, struct ctensor r, int32_t axis) {
  int32_t m, i, o;
  m = cdim_size(r.t_dims, r.t_rank);
  o = m - 1;
  if (0 <= o) {
    for (i = 0; ; ++i) {
      r.t_data[i] = x.t_data[i];
      if (i == o) {
        break;
      }
    }
  }
}
