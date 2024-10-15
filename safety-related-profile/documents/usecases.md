# Use case `Code generation` - `Robert Bosch GmbH`

## Description
We have developed a code generation tool that takes trained neural networks (float32 and int8) as input and generates code for a specific target platform. 
https://www.etas.com/en/products/embedded-ai-coder.php

ONNX files are the second input file format besides tflite.
We would like to ensure that our tool can correctly generate code for ONNX files that fulfill the functional safety profile.

## Models architecture
Any ONNX architecture that is relevant for customers and works on embedded hardware.

## Operators
At least Add, Mul, Sub, Dense, LSTM, Conv2D, DepthwiseConv2d, TransposeConv, LeakyRelu, Softmax, Tanh, Padding, all using float32 datatype.
For quantized models we so far recommend tflite.

# Use case `<name of the use case>` - `<provider>`

## Description
_Brief description of the use case. This description is optional, but providing a short description will make your need easier to understand._

## Models architecture
_Description of the model architecture(s). This can be provided explicitly (e.g., a Netron output), a reference to an existing model (e.g.,"Yolo Vx"), an ONNX file or a combination of these data_

## Operators
_List of operators_


