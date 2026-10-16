#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

#include "cindex.h"
#include "ctensoruint8.h"
#include "ctensorint8.h"
#include "ctensorint32.h"
#include "copconvinteger.h"

int main(void) {
    /* Input x: shape [N=1, C=1, H=3, W=3], values 1..9, x_zero = 0 */
    int32_t *x_dims = malloc(4 * sizeof(int32_t));
    x_dims[0] = 1; x_dims[1] = 1; x_dims[2] = 3; x_dims[3] = 3;
    struct ctensor_ui8 x = ctensor_create_ui8(x_dims, 4);
    uint8_t x_vals[9] = {1,2,3, 4,5,6, 7,8,9};
    for (int i = 0; i < 9; i++) x.t_data[i] = x_vals[i];
    uint8_t x_zero = 0;

    /* Weight w: shape [M=1, C=1, Kh=2, Kw=2], identity-ish, w_zero = 0 */
    int32_t *w_dims = malloc(4 * sizeof(int32_t));
    w_dims[0] = 1; w_dims[1] = 1; w_dims[2] = 2; w_dims[3] = 2;
    struct ctensor_i8 w = ctensor_create_i8(w_dims, 4);
    int8_t w_vals[4] = {1,0, 0,1};
    for (int i = 0; i < 4; i++) w.t_data[i] = w_vals[i];
    int8_t w_zero = 0;

    /* Output r: shape [N=1, M=1, Yh=2, Yw=2], stride 1, dilation 1, no padding */
    int32_t *r_dims = malloc(4 * sizeof(int32_t));
    r_dims[0] = 1; r_dims[1] = 1; r_dims[2] = 2; r_dims[3] = 2;
    struct ctensor_i32 r = ctensor_create_i32(r_dims, 4);

    int ok = cconvinteger(x, w, x_zero, w_zero, r,
                           /*str_h*/1, /*str_w*/1,
                           /*dil_h*/1, /*dil_w*/1,
                           /*pad_top*/0, /*pad_left*/0,
                           /*pad_bottom*/0, /*pad_right*/0);

    if (!ok) {
        fprintf(stderr, "cconvinteger failed\n");
        return 1;
    }

    printf("Result (expected 6 8 12 14):\n");
    for (int i = 0; i < 4; i++) {
        printf("%d ", r.t_data[i]);
    }
    printf("\n");

    int32_t expected[4] = {6, 8, 12, 14};
    int pass = 1;
    for (int i = 0; i < 4; i++) {
        if (r.t_data[i] != expected[i]) pass = 0;
    }
    printf(pass ? "TEST PASSED\n" : "TEST FAILED\n");

    free(x.t_data); free(x_dims);
    free(w.t_data); free(w_dims);
    free(r.t_data); free(r_dims);

    return pass ? 0 : 1;
}