#include "ctensorsoftmax.h"

int same_dims(struct ctensor x, struct ctensor r) {
  int ok;
  int32_t i, o;
  if (!(x.t_rank == r.t_rank)) {
    return 0;
  } else {
    ok = 1;
    o = x.t_rank - 1;
    if (0 <= o) {
      for (i = 0; ; ++i) {
        if (!(x.t_dims[i] == r.t_dims[i])) {
          ok = 0;
        }
        if (i == o) {
          break;
        }
      }
    }
    return ok;
  }
}

int32_t product_dims_range(int32_t * dims, int32_t first, int32_t last) {
  int32_t p;
  int32_t i, o;
  p = 1;
  o = last - 1;
  if (first <= o) {
    for (i = first; ; ++i) {
      p = p * dims[i];
      if (i == o) {
        break;
      }
    }
  }
  return p;
}

int c_softmax(struct ctensor x, struct ctensor r, int32_t axis) {
  int32_t rank, axis_size, inner, outer, o, o1, inn, o2, base, a, o3, off;
  double m, sum;
  double v, shifted, e, shifted1, e1;
  int32_t a1, o4, off1, a2, o5, off2;
  if (x.t_rank <= 0) {
    return 0;
  } else {
    if (axis < 0) {
      return 0;
    } else {
      if (axis >= x.t_rank) {
        return 0;
      } else {
        if (!same_dims(x, r)) {
          return 0;
        } else {
          rank = x.t_rank;
          axis_size = x.t_dims[axis];
          if (axis_size <= 0) {
            return 0;
          } else {
            inner = product_dims_range(x.t_dims, axis + 1, rank);
            outer = product_dims_range(x.t_dims, 0, axis);
            o1 = outer - 1;
            if (0 <= o1) {
              for (o = 0; ; ++o) {
                o2 = inner - 1;
                if (0 <= o2) {
                  for (inn = 0; ; ++inn) {
                    base = o * axis_size * inner + inn;
                    m = x.t_data[base];
                    o3 = axis_size - 1;
                    if (1 <= o3) {
                      for (a = 1; ; ++a) {
                        off = base + a * inner;
                        v = x.t_data[off];
                        if (m < v) {
                          m = v;
                        }
                        if (a == o3) {
                          break;
                        }
                      }
                    }
                    sum = (0.0);
                    o4 = axis_size - 1;
                    if (0 <= o4) {
                      for (a1 = 0; ; ++a1) {
                        off1 = base + a1 * inner;
                        shifted = x.t_data[off1] - m;
                        e = (exp(shifted));
                        sum = sum + e;
                        if (a1 == o4) {
                          break;
                        }
                      }
                    }
                    o5 = axis_size - 1;
                    if (0 <= o5) {
                      for (a2 = 0; ; ++a2) {
                        off2 = base + a2 * inner;
                        shifted1 = x.t_data[off2] - m;
                        e1 = (exp(shifted1));
                        r.t_data[off2] = e1 / sum;
                        if (a2 == o5) {
                          break;
                        }
                      }
                    }
                    if (inn == o2) {
                      break;
                    }
                  }
                }
                if (o == o1) {
                  break;
                }
              }
            }
            return 1;
          }
        }
      }
    }
  }
}
