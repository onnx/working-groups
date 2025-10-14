#ifndef CINDEX_H_INCLUDED

#include <stdlib.h>
#include <stdint.h>

int32_t cdim_size(int32_t* u, int32_t n);

int32_t* cdim_create_1(int32_t n);

int32_t* cdim_create_2(int32_t p, int32_t q);

int32_t coffset(int32_t* ks, int32_t* ds, int32_t n);

#define CINDEX_H_INCLUDED
#endif // CINDEX_H_INCLUDED
