#ifndef COPMATMUL_H_INCLUDED

#include <stdlib.h>
#include <stdint.h>
#include "cindex.h"
#include "ctensor.h"

int matmul(struct ctensor a, struct ctensor b, struct ctensor r);

#define COPMATMUL_H_INCLUDED
#endif // COPMATMUL_H_INCLUDED
