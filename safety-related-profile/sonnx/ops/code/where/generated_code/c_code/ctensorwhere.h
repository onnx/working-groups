#ifndef CTENSORWHERE_H_INCLUDED

#include <stdlib.h>
#include <stdint.h>
#include "cindex.h"
#include "ctensor.h"

void ctensor_where(struct ctensor cond, struct ctensor a, struct ctensor b,
                   struct ctensor r);

#define CTENSORWHERE_H_INCLUDED
#endif // CTENSORWHERE_H_INCLUDED
