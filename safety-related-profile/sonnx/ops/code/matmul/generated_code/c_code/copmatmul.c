#include "copmatmul.h"

int matmul(struct ctensor a, struct ctensor b, struct ctensor r) {
  int32_t rows, cols, iter;
  int flag;
  double sum;
  int32_t * a_coords_array;
  int32_t * b_coords_array;
  int32_t * r_coords_array;
  int32_t i, o, j, o1, k, o2, a_coords, b_coords, r_coords;
  double a_val, b_val;
  rows = a.t_dims[0];
  cols = b.t_dims[1];
  iter = a.t_dims[1];
  flag = 0;
  sum = ((double) 0.0);
  a_coords_array = malloc(((uint32_t) 2) * sizeof(int32_t));
  b_coords_array = malloc(((uint32_t) 2) * sizeof(int32_t));
  r_coords_array = malloc(((uint32_t) 2) * sizeof(int32_t));
  if (a_coords_array && (b_coords_array && r_coords_array)) {
    flag = 1;
    o = rows - 1;
    if (0 <= o) {
      for (i = 0; ; ++i) {
        o1 = cols - 1;
        if (0 <= o1) {
          for (j = 0; ; ++j) {
            o2 = iter - 1;
            if (0 <= o2) {
              for (k = 0; ; ++k) {
                a_coords_array[0] = i;
                a_coords_array[1] = k;
                b_coords_array[0] = k;
                b_coords_array[1] = j;
                a_coords = coffset(a_coords_array, a.t_dims, a.t_rank);
                b_coords = coffset(b_coords_array, b.t_dims, b.t_rank);
                a_val = a.t_data[a_coords];
                b_val = b.t_data[b_coords];
                sum = sum + a_val * b_val;
                if (k == o2) {
                  break;
                }
              }
            }
            r_coords_array[0] = i;
            r_coords_array[1] = j;
            r_coords = coffset(r_coords_array, r.t_dims, r.t_rank);
            r.t_data[r_coords] = sum;
            sum = ((double) 0.0);
            if (j == o1) {
              break;
            }
          }
        }
        if (i == o) {
          break;
        }
      }
    }
    return flag;
  } else {
    return flag;
  }
}
