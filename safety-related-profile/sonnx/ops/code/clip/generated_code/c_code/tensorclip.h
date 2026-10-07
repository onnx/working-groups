#ifndef TENSORCLIP_H_INCLUDED

#include <stdlib.h>
#include <stdint.h>
#include "cindex.h"
#include "ctensor.h"

void ctensor_clip(struct ctensor x, struct ctensor l, struct ctensor m,
                  struct ctensor r);

#define TENSORCLIP_H_INCLUDED
#endif // TENSORCLIP_H_INCLUDED
