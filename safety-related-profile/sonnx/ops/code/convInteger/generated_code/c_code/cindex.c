#include "cindex.h"

int32_t cdim_size(int32_t * u, int32_t n) {
  int32_t p;
  int32_t i, o;
  p = 1;
  o = n - 1;
  if (0 <= o) {
    for (i = 0; ; ++i) {
      p = p * u[i];
      if (i == o) {
        break;
      }
    }
  }
  return p;
}

int32_t * cdim_create_1(int32_t n) {
  int32_t * cd;
  cd = malloc(1U * sizeof(int32_t));
  if (cd) {
    cd[0] = n;
  }
  return cd;
}

int32_t * cdim_create_2(int32_t p, int32_t q) {
  int32_t * cd;
  cd = malloc(2U * sizeof(int32_t));
  if (cd) {
    cd[0] = p;
    cd[1] = q;
  }
  return cd;
}

int32_t coffset(int32_t * ks, int32_t * ds, int32_t n) {
  int32_t p;
  int32_t i, o, d, k;
  p = 0;
  o = n - 1;
  if (0 <= o) {
    for (i = 0; ; ++i) {
      d = ds[i];
      k = ks[i];
      if (0 <= k && k < d) {
        p = p * d + k;
      } else {
        return -1;
      }
      if (i == o) {
        break;
      }
    }
  }
  return p;
}
