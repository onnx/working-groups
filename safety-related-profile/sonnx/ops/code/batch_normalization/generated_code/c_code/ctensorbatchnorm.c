#include "ctensorbatchnorm.h"

void ctensor_batchnorm(struct ctensor x, struct ctensor scale,
                       struct ctensor input_mean, struct ctensor input_var,
                       struct ctensor bias, double eps, struct ctensor r) {
  int32_t n_size, c_size, spatial, nc, stride, n, o, c, o1;
  int32_t flat;
  double mu, sigma, g, b, v;
  int32_t s, o2;
  n_size = x.t_dims[0];
  c_size = scale.t_dims[0];
  spatial = cdim_size(r.t_dims, r.t_rank);
  nc = n_size * c_size;
  stride = spatial / nc;
  flat = 0;
  o = n_size - 1;
  if (0 <= o) {
    for (n = 0; ; ++n) {
      o1 = c_size - 1;
      if (0 <= o1) {
        for (c = 0; ; ++c) {
          mu = input_mean.t_data[c];
          sigma = input_var.t_data[c];
          g = scale.t_data[c];
          b = bias.t_data[c];
          o2 = stride - 1;
          if (0 <= o2) {
            for (s = 0; ; ++s) {
              v = x.t_data[flat];
              r.t_data[flat] = g * ((v - mu) / (sqrt((sigma + eps)))) + b;
              flat = flat + 1;
              if (s == o2) {
                break;
              }
            }
          }
          if (c == o1) {
            break;
          }
        }
      }
      if (n == o) {
        break;
      }
    }
  }
}
