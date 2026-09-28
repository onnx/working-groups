#include "ctensorquantizelinear.h"

void ctensor_quantize_linear(struct ctensor x, float scale,
                             uint8_t zero_point, struct ctensor_ui8 r) {
  int32_t m, i, o, wz, c;
  float v;
  m = cdim_size(r.t_dims, r.t_rank);
  o = m - 1;
  if (0 <= o) {
    for (i = 0; ; ++i) {
      v = x.t_data[i];
      wz = ((int32_t) zero_point);
      c = (((int32_t) fmin(255.0, fmax(0.0, (double) rintf((v / scale)) + (double) (wz)))));
      r.t_data[i] = (((uint8_t) c));
      if (i == o) {
        break;
      }
    }
  }
}
