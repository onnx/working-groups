#ifndef CTENSORMUL_H_INCLUDED

#include <stdlib.h>
#include <stdint.h>
#include "cindex.h"
#include "ctensor.h"

void ctensor_mul(struct ctensor a, struct ctensor b, struct ctensor r);

#define CTENSORMUL_H_INCLUDED
#endif // CTENSORMUL_H_INCLUDED
