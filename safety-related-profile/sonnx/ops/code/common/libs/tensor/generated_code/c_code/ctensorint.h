#ifndef CTENSORINT_H_INCLUDED

#include "cindex.h"

struct ctensorint ctensor_create(int32_t * ds, int32_t n);

void ctensor_clear(struct ctensorint r);

void ctensor_reset(struct ctensorint r, int32_t v);

#define CTENSORINT_H_INCLUDED
#endif // CTENSORINT_H_INCLUDED
