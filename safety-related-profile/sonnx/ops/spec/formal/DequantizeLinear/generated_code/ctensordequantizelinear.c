#include "ctensordequantizelinear.h"

void ctensor_dequantize_linear(struct ctensor_i32 x, float scale,
                               int32_t zero_point, struct ctensor r) {
  int32_t m, i, o, d;
  m = cdim_size(r.t_dims, r.t_rank);
  o = m - 1;
  if (0 <= o) {
    for (i = 0; ; ++i) {
      d = (int32_t)((uint32_t)x.t_data[i] - (uint32_t)zero_point);
      r.t_data[i] = (((float) d)) * scale;
      if (i == o) {
        break;
      }
    }
  }
}
