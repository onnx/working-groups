#include "ctensor.h"
struct ctensor;


struct ctensor ctensor_create(int32_t* ds, int32_t n) {
  int32_t m;
  double* vs;
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

void ctensor_conv2d(struct ctensor x, struct ctensor w, struct ctensor b,
                    int32_t pad_top, int32_t pad_bottom, int32_t pad_left,
                    int32_t pad_right, int32_t dil_h, int32_t dil_w,
                    int32_t str_h, int32_t str_w, struct ctensor output) {
  int32_t n_batches, c_in, h_in, w_in, m_out, kh, kw, h_out, w_out,
          pad_top_i, pad_left_i, dil_h_i, dil_w_i, str_h_i, str_w_i;
  int32_t* x_coords;
  int32_t* w_coords;
  int32_t* b_coords;
  int32_t* output_coords;
  int32_t n, o, m, o1, oh, o2, ow, o3, c, o4, k_h, o5, k_w, o6, ih, iw,
          padded_ih, padded_iw;
  double conv_sum;
  double x_val, w_val, bias_val, final_val;
  int32_t x_offset, w_offset, b_offset, output_offset;
  n_batches = x.t_dims[0];
  c_in = x.t_dims[1];
  h_in = x.t_dims[2];
  w_in = x.t_dims[3];
  m_out = w.t_dims[0];
  kh = w.t_dims[2];
  kw = w.t_dims[3];
  h_out = output.t_dims[2];
  w_out = output.t_dims[3];
  pad_top_i = pad_top;
  pad_left_i = pad_left;
  dil_h_i = dil_h;
  dil_w_i = dil_w;
  str_h_i = str_h;
  str_w_i = str_w;
  x_coords = (malloc(((uint32_t) 4) * sizeof(int32_t)));
  w_coords = (malloc(((uint32_t) 4) * sizeof(int32_t)));
  b_coords = (malloc(((uint32_t) 1) * sizeof(int32_t)));
  output_coords = (malloc(((uint32_t) 4) * sizeof(int32_t)));
  if (x_coords && (w_coords && (b_coords && output_coords))) {
    o = n_batches - 1;
    if (0 <= o) {
      for (n = 0; ; ++n) {
        o1 = m_out - 1;
        if (0 <= o1) {
          for (m = 0; ; ++m) {
            o2 = h_out - 1;
            if (0 <= o2) {
              for (oh = 0; ; ++oh) {
                o3 = w_out - 1;
                if (0 <= o3) {
                  for (ow = 0; ; ++ow) {
                    conv_sum = ((double) 0.0);
                    o4 = c_in - 1;
                    if (0 <= o4) {
                      for (c = 0; ; ++c) {
                        o5 = kh - 1;
                        if (0 <= o5) {
                          for (k_h = 0; ; ++k_h) {
                            o6 = kw - 1;
                            if (0 <= o6) {
                              for (k_w = 0; ; ++k_w) {
                                ih = oh * str_h_i + k_h * dil_h_i;
                                iw = ow * str_w_i + k_w * dil_w_i;
                                padded_ih = ih - pad_top_i;
                                padded_iw = iw - pad_left_i;
                                if ((0 <= padded_ih) && ((padded_ih < h_in) && 
                                                         ((0 <= padded_iw) && (padded_iw < w_in)))) {
                                  x_coords[0] = n;
                                  x_coords[1] = c;
                                  x_coords[2] = padded_ih;
                                  x_coords[3] = padded_iw;
                                  x_offset = coffset(x_coords, x.t_dims, 4);
                                  if (x_offset >= 0) {
                                    x_val = x.t_data[x_offset];
                                  } else {
                                    x_val = ((double) 0.0);
                                  }
                                } else {
                                  x_val = ((double) 0.0);
                                }
                                w_coords[0] = m;
                                w_coords[1] = c;
                                w_coords[2] = k_h;
                                w_coords[3] = k_w;
                                w_offset = coffset(w_coords, w.t_dims, 4);
                                if (w_offset >= 0) {
                                  w_val = w.t_data[w_offset];
                                } else {
                                  w_val = ((double) 0.0);
                                }
                                (*(&conv_sum) = ((*(&conv_sum)) + x_val * w_val));
                                if (k_w == o6) {
                                  break;
                                }
                              }
                            }
                            if (k_h == o5) {
                              break;
                            }
                          }
                        }
                        if (c == o4) {
                          break;
                        }
                      }
                    }
                    b_coords[0] = m;
                    b_offset = coffset(b_coords, b.t_dims, 1);
                    if (b_offset >= 0) {
                      bias_val = b.t_data[b_offset];
                    } else {
                      bias_val = ((double) 0.0);
                    }
                    final_val = (*(&conv_sum)) + bias_val;
                    output_coords[0] = n;
                    output_coords[1] = m;
                    output_coords[2] = oh;
                    output_coords[3] = ow;
                    output_offset = coffset(output_coords, output.t_dims, 4);
                    if (output_offset >= 0) {
                      output.t_data[output_offset] = final_val;
                    }
                    if (ow == o3) {
                      break;
                    }
                  }
                }
                if (oh == o2) {
                  break;
                }
              }
            }
            if (m == o1) {
              break;
            }
          }
        }
        if (n == o) {
          break;
        }
      }
    }
  } else {
    return;
  }
}
