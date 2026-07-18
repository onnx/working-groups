#include "copconv2d.h"
struct __coords_from_X_p_result;


struct __coords_from_X_p_result coords_from_x_p(struct ctensor x,
                                                int32_t * x_p_coords,
                                                int32_t pad_top,
                                                int32_t pad_left) {
  int flag;
  int32_t b, c, n, m, x_coords;
  int32_t * x_coords_array;
  struct __coords_from_X_p_result result, result1, result2;
  flag = 0;
  b = x_p_coords[0];
  c = x_p_coords[1];
  n = x_p_coords[2] - pad_top;
  m = x_p_coords[3] - pad_left;
  x_coords_array = malloc(((uint32_t) 4) * sizeof(int32_t));
  if (x_coords_array) {
    flag = 1;
    x_coords_array[0] = b;
    x_coords_array[1] = c;
    x_coords_array[2] = n;
    x_coords_array[3] = m;
    x_coords = coffset(x_coords_array, x.t_dims, x.t_rank);
    if (x_coords >= 0) {
      result.__field_0 = x.t_data[x_coords];
      result.__field_1 = flag;
      return result;
    } else {
      result1.__field_0 = ((double) 0.0);
      result1.__field_1 = flag;
      return result1;
    }
  } else {
    flag = 0;
    result2.__field_0 = ((double) 0.0);
    result2.__field_1 = flag;
    return result2;
  }
}
struct __w_cools_calculate_result;


struct __w_cools_calculate_result w_cools_calculate(struct ctensor x,
                                                    struct ctensor w,
                                                    int32_t c, int32_t i,
                                                    int32_t n, int32_t m,
                                                    int32_t y_h, int32_t y_w,
                                                    int32_t str_h,
                                                    int32_t str_w,
                                                    int32_t dil_h,
                                                    int32_t dil_w,
                                                    int32_t pad_top,
                                                    int32_t pad_left) {
  int flag;
  double sum;
  int32_t * x_coords_array;
  int32_t * w_coords_array;
  int32_t cols, jj, o, x_h, x_w;
  double x_val;
  int aux_flag;
  struct __coords_from_X_p_result struct_res;
  int32_t w_coords;
  double w_val;
  struct __w_cools_calculate_result result, result1, result2;
  flag = 0;
  sum = ((double) 0.0);
  x_coords_array = malloc(((uint32_t) 4) * sizeof(int32_t));
  w_coords_array = malloc(((uint32_t) 4) * sizeof(int32_t));
  cols = w.t_dims[3];
  if (x_coords_array && w_coords_array) {
    flag = 1;
    o = cols - 1;
    if (0 <= o) {
      for (jj = 0; ; ++jj) {
        x_h = y_h * str_h + i * dil_h;
        x_w = y_w * str_w + jj * dil_w;
        x_coords_array[0] = n;
        x_coords_array[1] = c;
        x_coords_array[2] = x_h;
        x_coords_array[3] = x_w;
        struct_res = coords_from_x_p(x, x_coords_array, pad_top, pad_left);
        x_val = struct_res.__field_0;
        aux_flag = struct_res.__field_1;
        if (aux_flag) {
          w_coords_array[0] = m;
          w_coords_array[1] = c;
          w_coords_array[2] = i;
          w_coords_array[3] = jj;
          w_coords = coffset(w_coords_array, w.t_dims, w.t_rank);
          w_val = w.t_data[w_coords];
          sum = sum + x_val * w_val;
        } else {
          flag = 0;
          result.__field_0 = ((double) 0.0);
          result.__field_1 = flag;
          return result;
        }
        if (jj == o) {
          break;
        }
      }
    }
    result1.__field_0 = sum;
    result1.__field_1 = flag;
    return result1;
  } else {
    flag = 0;
    result2.__field_0 = ((double) 0.0);
    result2.__field_1 = flag;
    return result2;
  }
}
struct __w_lines_calculate_result;


struct __w_lines_calculate_result w_lines_calculate(struct ctensor x,
                                                    struct ctensor w,
                                                    int32_t c, int32_t n,
                                                    int32_t m, int32_t y_h,
                                                    int32_t y_w,
                                                    int32_t str_h,
                                                    int32_t str_w,
                                                    int32_t dil_h,
                                                    int32_t dil_w,
                                                    int32_t pad_top,
                                                    int32_t pad_left) {
  int32_t i;
  int flag;
  double sum;
  int32_t ii, o;
  double value;
  int aux_flag;
  struct __w_cools_calculate_result struct_res;
  struct __w_lines_calculate_result result, result1;
  i = w.t_dims[2];
  flag = 0;
  sum = ((double) 0.0);
  o = i - 1;
  if (0 <= o) {
    for (ii = 0; ; ++ii) {
      struct_res = w_cools_calculate(x, w, c, ii, n, m, y_h, y_w, str_h,
                   str_w, dil_h, dil_w, pad_top, pad_left);
      value = struct_res.__field_0;
      aux_flag = struct_res.__field_1;
      if (aux_flag) {
        flag = 1;
        sum = sum + value;
      } else {
        flag = 0;
        result.__field_0 = ((double) 0.0);
        result.__field_1 = flag;
        return result;
      }
      if (ii == o) {
        break;
      }
    }
  }
  result1.__field_0 = sum;
  result1.__field_1 = flag;
  return result1;
}
struct __w_channels_calculate_result;


struct __w_channels_calculate_result w_channels_calculate(struct ctensor x,
                                                          struct ctensor w,
                                                          int32_t n,
                                                          int32_t m,
                                                          int32_t y_h,
                                                          int32_t y_w,
                                                          int32_t str_h,
                                                          int32_t str_w,
                                                          int32_t dil_h,
                                                          int32_t dil_w,
                                                          int32_t pad_top,
                                                          int32_t pad_left) {
  int32_t c;
  int flag;
  double sum;
  int32_t cc, o;
  double value;
  int aux_flag;
  struct __w_lines_calculate_result struct_res;
  struct __w_channels_calculate_result result, result1;
  c = w.t_dims[1];
  flag = 0;
  sum = ((double) 0.0);
  o = c - 1;
  if (0 <= o) {
    for (cc = 0; ; ++cc) {
      struct_res = w_lines_calculate(x, w, cc, n, m, y_h, y_w, str_h, str_w,
                   dil_h, dil_w, pad_top, pad_left);
      value = struct_res.__field_0;
      aux_flag = struct_res.__field_1;
      if (aux_flag) {
        flag = 1;
        sum = sum + value;
      } else {
        flag = 0;
        result.__field_0 = ((double) 0.0);
        result.__field_1 = flag;
        return result;
      }
      if (cc == o) {
        break;
      }
    }
  }
  result1.__field_0 = sum;
  result1.__field_1 = flag;
  return result1;
}

int cconv(struct ctensor x, struct ctensor w, struct ctensor r,
          int32_t str_h, int32_t str_w, int32_t dil_h, int32_t dil_w,
          int32_t pad_top, int32_t pad_left, int32_t pad_bottom,
          int32_t pad_right) {
  int32_t n, m, y_h, y_w, nn, o, mm, o1, y_hh, o2, y_ww, o3;
  int32_t * r_coords_array;
  double value;
  int flag;
  struct __w_channels_calculate_result struct_res;
  int32_t r_coords;
  n = r.t_dims[0];
  m = r.t_dims[1];
  y_h = r.t_dims[2];
  y_w = r.t_dims[3];
  r_coords_array = malloc(((uint32_t) 4) * sizeof(int32_t));
  if (r_coords_array) {
    o = n - 1;
    if (0 <= o) {
      for (nn = 0; ; ++nn) {
        r_coords_array[0] = nn;
        o1 = m - 1;
        if (0 <= o1) {
          for (mm = 0; ; ++mm) {
            r_coords_array[1] = mm;
            o2 = y_h - 1;
            if (0 <= o2) {
              for (y_hh = 0; ; ++y_hh) {
                r_coords_array[2] = y_hh;
                o3 = y_w - 1;
                if (0 <= o3) {
                  for (y_ww = 0; ; ++y_ww) {
                    r_coords_array[3] = y_ww;
                    struct_res = w_channels_calculate(x, w, nn, mm, y_hh,
                                 y_ww, str_h, str_w, dil_h, dil_w, pad_top,
                                 pad_left);
                    value = struct_res.__field_0;
                    flag = struct_res.__field_1;
                    if (flag) {
                      r_coords = coffset(r_coords_array, r.t_dims, r.t_rank);
                      r.t_data[r_coords] = value;
                    } else {
                      return 0;
                    }
                    if (y_ww == o3) {
                      break;
                    }
                  }
                }
                if (y_hh == o2) {
                  break;
                }
              }
            }
            if (mm == o1) {
              break;
            }
          }
        }
        if (nn == o) {
          break;
        }
      }
    }
    return 1;
  } else {
    return 0;
  }
}
