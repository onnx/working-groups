#include "ctensorleakyrelu.h"

void ctensor_leaky_relu(double alpha, struct ctensor x, struct ctensor r) {
  int32_t m, i, o;
  double v;
  m = cdim_size(r.t_dims, r.t_rank);
  o = m - 1;
  if (0 <= o) {
    for (i = 0; ; ++i) {
      v = x.t_data[i];
      r.t_data[i] = ((double) 0.0) <= v ? v : alpha * v;
      if (i == o) {
        break;
      }
    }
  }
}
