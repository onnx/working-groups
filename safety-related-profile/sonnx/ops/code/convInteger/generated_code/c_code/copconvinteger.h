#ifndef COPCONVINTEGER_H_INCLUDED

#include "cindex.h"
#include "ctensorint32.h"
#include "ctensorint8.h"
#include "ctensoruint8.h"

struct __coords_from_X_p_result {
  int32_t __field_0;
  int __field_1;
};

struct __coords_from_X_p_result coords_from_x_p(struct ctensor_ui8 x,
                                                uint8_t x_zero,
                                                int32_t * x_p_coords,
                                                int32_t pad_top,
                                                int32_t pad_left);

struct __w_cools_calculate_result {
  int32_t __field_0;
  int __field_1;
};

struct __w_cools_calculate_result w_cools_calculate(struct ctensor_ui8 x,
                                                    struct ctensor_i8 w,
                                                    uint8_t x_zero,
                                                    int8_t w_zero, int32_t c,
                                                    int32_t i, int32_t n,
                                                    int32_t m, int32_t y_h,
                                                    int32_t y_w,
                                                    int32_t str_h,
                                                    int32_t str_w,
                                                    int32_t dil_h,
                                                    int32_t dil_w,
                                                    int32_t pad_top,
                                                    int32_t pad_left);

struct __w_lines_calculate_result {
  int32_t __field_0;
  int __field_1;
};

struct __w_lines_calculate_result w_lines_calculate(struct ctensor_ui8 x,
                                                    struct ctensor_i8 w,
                                                    uint8_t x_zero,
                                                    int8_t w_zero, int32_t c,
                                                    int32_t n, int32_t m,
                                                    int32_t y_h, int32_t y_w,
                                                    int32_t str_h,
                                                    int32_t str_w,
                                                    int32_t dil_h,
                                                    int32_t dil_w,
                                                    int32_t pad_top,
                                                    int32_t pad_left);

struct __w_channels_calculate_result {
  int32_t __field_0;
  int __field_1;
};

struct __w_channels_calculate_result w_channels_calculate(struct ctensor_ui8 x,
                                                          struct ctensor_i8 w,
                                                          uint8_t x_zero,
                                                          int8_t w_zero,
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

int cconvinteger(struct ctensor_ui8 x, struct ctensor_i8 w, uint8_t x_zero,
                 int8_t w_zero, struct ctensor_i32 r, int32_t str_h,
                 int32_t str_w, int32_t dil_h, int32_t dil_w,
                 int32_t pad_top, int32_t pad_left, int32_t pad_bottom,
                 int32_t pad_right);

#define COPCONVINTEGER_H_INCLUDED
#endif // COPCONVINTEGER_H_INCLUDED
