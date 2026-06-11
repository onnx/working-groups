#include "tensorclip.h"

void ctensor_clip(struct ctensor x, struct ctensor l, struct ctensor m,
                  struct ctensor r) {
  int32_t n, i, o;
  double l_background, m_background;
  n = cdim_size(r.t_dims, r.t_rank);
  l_background = l.t_data[0];
  m_background = m.t_data[0];
  o = n - 1;
  if (0 <= o) {
    for (i = 0; ; ++i) {
      r.t_data[i] = infix_dtlsls(m_background,
                    infix_dtgtgt(x.t_data[i], l_background));
      if (i == o) {
        break;
      }
    }
  }
}
