#ifndef COPCONV2D_H_INCLUDED

#include <stdlib.h>
#include <stdint.h>
#include "cindex.h"
#include "ctensor.h"

struct __coords_from_X_p_result {
  double __field_0;
  int __field_1;
};

struct __coords_from_X_p_result coords_from_x_p(struct ctensor x,
                                                int32_t * x_p_coords,
                                                int32_t pad_top,
                                                int32_t pad_left);

struct __w_cools_calculate_result {
  double __field_0;
  int __field_1;
};

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
                                                    int32_t pad_left);

struct __w_lines_calculate_result {
  double __field_0;
  int __field_1;
};

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
                                                    int32_t pad_left);

struct __w_channels_calculate_result {
  double __field_0;
  int __field_1;
};

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
                                                          int32_t pad_left);

int cconv(struct ctensor x, struct ctensor w, struct ctensor r,
          int32_t str_h, int32_t str_w, int32_t dil_h, int32_t dil_w,
          int32_t pad_top, int32_t pad_left, int32_t pad_bottom,
          int32_t pad_right);

#define COPCONV2D_H_INCLUDED
#endif // COPCONV2D_H_INCLUDED
