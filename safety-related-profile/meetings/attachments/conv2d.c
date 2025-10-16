#include <stdio.h> // Include necessary headers
#include <stdlib.h> // For rand() function


// Define constants
#define F 2
#define OH 28
#define OW 28
#define IH 5
#define IW 5
#define C 3
#define KH 3
#define KW 3
#define STRIDES 1
#define DILATATION 1
#define PAD_LEFT 0
#define PAD_TOP 0

// Function prototype
void conv2D(const float* input, float* output, const float* kernel, const float* biases);

int main() {
    // Define input, output, kernel, and biases arrays
    float input[IH * IW * C];
    float output[OH * OW * F];
    float kernel[KH * KW * C * F];
    float biases[F];

    // Initialize input array with random values between 0 and 1
    for (int i = 0; i < IH * IW * C; i++) {
        input[i] = (float)rand() / RAND_MAX;
    }

    // Initialize kernel array with random values between -1 and 1
     for (int i = 0; i < KH * KW * C * F; i++) {
        kernel[i] = ((float)rand() / RAND_MAX) * 2 - 1;
    }

    // Initialize biases array with random values between -1 and 1
    for (int i = 0; i < F; i++) {
        biases[i] = ((float)rand() / RAND_MAX) * 2 - 1;
    }

    // Define and initialize output array
    for (int i = 0; i < (IH - KH + 1) * (IW - KW + 1) * F; i++) {
        output[i] = 0.0;
    }

    // Call conv2D function
    conv2D(input, output, kernel, biases);

    // Print the result
    printf("Result:\n");
    for (int f = 0; f < F; f++) {
        printf("Filter %d:\n", f);
        for (int i = 0; i < OH; i++) {
            for (int j = 0; j < OW; j++) {
                printf("%f ", output[i * OW * F + j * F + f]);
            }
            printf("\n");
        }
    }

    return 0;
}


// conv2D(
//     input : f32[IH, IW, C] @DRAM,
//     output : f32[OH, OW, F] @DRAM,
//     kernel : f32[KH, KW, C, F] @DRAM,
//     biases : f32[F] @DRAM
// )
void conv2D( const float* input, float* output, const float* kernel, const float* biases ) {
    for (size_t f = 0; f < F; f++) {
        for (size_t i = 0; i < OH; i++) {
            for (size_t j = 0; j < OW; j++) {
            output[i * OW * F + j * F + f] = 0.0;
                for (size_t c = 0; c < C; c++) {
                    for (size_t m = 0; m < KH; m++) {
                        for (size_t n = 0; n < KW; n++) {
                            if (0 <= i * STRIDES + m * DILATATION - PAD_LEFT && i * STRIDES + m * DILATATION - PAD_LEFT < IH && (0 <= j * STRIDES + n * DILATATION - PAD_TOP && j * STRIDES + n * DILATATION - PAD_TOP < IW)) {
                            output[i * OW * F + j * F + f] += input[(i * STRIDES + m * DILATATION - PAD_LEFT) * IW * C + (j * STRIDES + n * DILATATION - PAD_TOP) * C + c] * kernel[m * KW * C * F + n * C * F + c * F + f];
                            }
                        }
                    }
                }
                output[i * OW * F + j * F + f] += biases[f];
                }
        }
    }
}
