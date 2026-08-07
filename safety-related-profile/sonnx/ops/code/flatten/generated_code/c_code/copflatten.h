#ifndef COPFLATTEN_H_INCLUDED

#include <stdlib.h>
#include <stdint.h>
#include "cindex.h"
#include "ctensor.h"

void flatten(struct ctensor x, struct ctensor r, int32_t axis);

#define COPFLATTEN_H_INCLUDED
#endif // COPFLATTEN_H_INCLUDED
