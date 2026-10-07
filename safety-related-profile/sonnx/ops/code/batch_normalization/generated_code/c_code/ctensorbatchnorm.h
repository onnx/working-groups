#ifndef CTENSORBATCHNORM_H_INCLUDED

#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <math.h>
#include "cindex.h"
#include "ctensor.h"

void ctensor_batchnorm(struct ctensor x, struct ctensor scale,
                       struct ctensor input_mean, struct ctensor input_var,
                       struct ctensor bias, double eps, struct ctensor r);

#define CTENSORBATCHNORM_H_INCLUDED
#endif // CTENSORBATCHNORM_H_INCLUDED
