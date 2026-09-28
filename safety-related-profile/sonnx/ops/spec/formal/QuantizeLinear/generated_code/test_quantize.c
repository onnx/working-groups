#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#include <string.h>
#include "ctensor.h"
#include "ctensoruint8.h"
#include "ctensorquantizelinear.h"

/* ---- Independent reference implementation (double precision) ---- */

/* Returns the round-half-to-even result as a double (never casts to a
 * bounded integer type), so it stays correct no matter how large |x| is.
 * Tie-parity only needs an exact integer cast when f is small enough for
 * that cast to be safe; for astronomically large f the tie is irrelevant
 * anyway since the final clamp to [0,255] will dominate the result. */
static double ref_round_half_even_d(double x) {
    double f = floor(x);
    double r = x - f;
    if (r < 0.5) return f;
    if (r > 0.5) return f + 1.0;
    if (fabs(f) < 9.0e15) {              /* safe range for long long cast */
        long long fi = (long long) f;
        return (fi % 2 == 0) ? f : f + 1.0;
    }
    return f;                             /* tie irrelevant at this magnitude */
}

static int ref_quantize(float v, float scale, int zero_point) {
    double q = (double) v / (double) scale;
    double rounded = ref_round_half_even_d(q);
    double result = rounded + (double) zero_point;
    if (result < 0.0) return 0;
    if (result > 255.0) return 255;
    return (int) result;                  /* safe: bounded to [0,255] here */
}

typedef struct { int pass, fail, total; } Stats;

static void check(Stats *s, const char *name, float v, float scale, uint8_t zp, uint8_t got) {
    int expected = ref_quantize(v, scale, zp);
    s->total++;
    if ((int) got == expected) {
        s->pass++;
    } else {
        s->fail++;
        printf("FAIL [%-22s] v=%.9g scale=%.9g zp=%d -> got=%d expected=%d\n",
               name, (double) v, (double) scale, zp, got, expected);
    }
}

struct Case { const char *name; float v; float scale; uint8_t zp; };

int main(void) {
    Stats s = {0, 0, 0};

    int32_t dims1[1] = {1};
    struct ctensor x = ctensor_create(dims1, 1);
    struct ctensor_ui8 r = ctensor_create_ui8(dims1, 1);

    struct Case cases[] = {
        {"nominal_mid",          5.0f,      1.0f,    128},
        {"zero",                 0.0f,      1.0f,    128},
        {"tie_2.5",               2.5f,      1.0f,    0},
        {"tie_3.5",               3.5f,      1.0f,    0},
        {"tie_-2.5",             -2.5f,      1.0f,    128},
        {"tie_-3.5",             -3.5f,      1.0f,    128},
        {"neg_saturate",       -1000.0f,     1.0f,    0},
        {"pos_saturate",        1000.0f,     1.0f,    0},
        {"pos_saturate_zp255",  1000.0f,     1.0f,    255},
        {"neg_saturate_zp255", -1000.0f,     1.0f,    255},
        {"exact_255",            255.0f,     1.0f,    0},
        {"exact_0",                0.0f,     1.0f,    0},
        {"just_above_255.5",     255.5f,     1.0f,    0},
        {"just_below_-0.5",       -0.5f,     1.0f,    0},
        {"small_scale",             1.0f,    0.001f,  0},
        {"large_scale",        1000000.0f,   1000.0f, 0},
        {"neg_input_pos_zp",       -5.0f,    2.0f,    10},
        {"fraction_1.3",            1.3f,    0.5f,    0},
        {"fraction_1.7",            1.7f,    0.5f,    0},
        {"extreme_overflow",       1e30f,    1e-30f,  0},
        {"extreme_overflow_neg",  -1e30f,    1e-30f,  0},
        {"nan_guard",               0.0f,    1.0f,    0},
    };

    for (size_t i = 0; i < sizeof(cases) / sizeof(cases[0]); i++) {
        x.t_data[0] = cases[i].v;
        ctensor_quantize_linear(x, cases[i].scale, cases[i].zp, r);
        check(&s, cases[i].name, cases[i].v, cases[i].scale, cases[i].zp, r.t_data[0]);
    }

    /* Randomized fuzz test over a realistic float32 domain */
    srand(42);
    int rand_total = 200000;
    int overflow_events = 0;
    for (int i = 0; i < rand_total; i++) {
        float v     = ((float) rand() / RAND_MAX) * 2000.0f - 1000.0f;  /* [-1000, 1000] */
        float scale = ((float) rand() / RAND_MAX) * 9.99f + 0.01f;      /* [0.01, 10]   */
        uint8_t zp  = (uint8_t) (rand() % 256);

        double math_val = (double) v / (double) scale;
        if (math_val > 2e9 || math_val < -2e9) overflow_events++;

        x.t_data[0] = v;
        ctensor_quantize_linear(x, scale, zp, r);
        char name[32];
        snprintf(name, sizeof(name), "fuzz#%d", i);
        check(&s, name, v, scale, zp, r.t_data[0]);
    }

    /* Targeted fuzz near the int32 wraparound boundary: this is exactly the
       zone the Why3 proof needed an extra 'no-overflow' hypothesis for. */
    int wrap_mismatches = 0;
    for (int i = 0; i < 50000; i++) {
        float v     = ((float) rand() / RAND_MAX) * 2e10f - 1e10f;   /* huge magnitude */
        float scale = ((float) rand() / RAND_MAX) * 0.999f + 0.001f; /* [0.001, 1] */
        uint8_t zp  = (uint8_t) (rand() % 256);

        x.t_data[0] = v;
        ctensor_quantize_linear(x, scale, zp, r);
        int expected = ref_quantize(v, scale, zp);
        if ((int) r.t_data[0] != expected) wrap_mismatches++;
    }

    printf("\n=== RESULTS ===\n");
    printf("Total cases: %d   Pass: %d   Fail: %d\n", s.total, s.pass, s.fail);
    printf("Fuzz range [-1000,1000]: %d values could exceed +-2e9 pre-clamp (overflow risk zone): %d\n",
           rand_total, overflow_events);
    printf("Extreme-magnitude wraparound test (50000 cases, |v| up to 1e10): mismatches = %d\n",
           wrap_mismatches);

    /* Multi-element tensor: check indexing / no off-by-one across a real array */
    {
        int32_t dims[1] = {8};
        struct ctensor xm = ctensor_create(dims, 1);
        struct ctensor_ui8 rm = ctensor_create_ui8(dims, 1);
        float vals[8] = {-300.0f, -1.0f, -0.5f, 0.0f, 0.5f, 1.0f, 127.4f, 300.0f};
        for (int i = 0; i < 8; i++) xm.t_data[i] = vals[i];
        ctensor_quantize_linear(xm, 1.0f, 128, rm);
        printf("\nMulti-element tensor test (scale=1.0, zero_point=128):\n");
        int mfail = 0;
        for (int i = 0; i < 8; i++) {
            int expected = ref_quantize(vals[i], 1.0f, 128);
            printf("  v=%9.3f -> got=%3d expected=%3d %s\n",
                   (double) vals[i], rm.t_data[i], expected,
                   (rm.t_data[i] == expected) ? "OK" : "MISMATCH");
            if (rm.t_data[i] != expected) mfail++;
        }
        if (mfail) printf("Multi-element test: %d mismatches\n", mfail);
        free(xm.t_data);
        free(rm.t_data);
    }

    free(x.t_data);
    free(r.t_data);

    return (s.fail || wrap_mismatches) ? 1 : 0;
}