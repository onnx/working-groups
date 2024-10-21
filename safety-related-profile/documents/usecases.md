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




# Use case `Visual Detection` - `Thales AVS`

## Description
The use case is an example of visual-based detection, with the AI algorithm utilized being of the 'Computer Vision' type, such as YOLO.
For performance reasons, for example the chosen example will use MobileNetSSDv2, converted into an ONNX file.
It is sometimes necessary to perform tracking using a skeleton or to predict fluctuations in values through regression or to make time-series predictions.


## Models architecture
MobileNetSSDv2 is a lightweight, efficient deep learning model designed for object detection tasks.
It combines the MobileNetV2 architecture, which is known for its efficiency and performance in mobile and embedded device applications, with the Single Shot MultiBox Detector (SSD) framework, which is used for detecting objects in images.
MobileNetV2 uses depthwise separable convolutions, which significantly reduce the number of parameters and computational cost compared to traditional convolutional neural networks.
This makes it highly suitable for real-time applications on devices with limited computational resources.

The SSD framework enables the model to detect objects at different scales and aspect ratios by applying multiple convolutional filters to the input image and generating a series of bounding boxes around the detected objects.
MobileNetSSDv2 is particularly popular for its balance between accuracy and speed, making it well-suited for a variety of real-time object detection applications, including autonomous driving, robotics, and augmented reality.
The Netron application shows the following operators for MobileNet-SSDv2. Note that YOLOv8 also provides skeleton capabilities, which is why some additional operators are also interesting for YOLOv8, or for segmentation capability. Additionally, a classic inference layer can be added after this type of detection, and some more operators could be interesting for a complete functionality

## Operators
### MobileNetSSDv2, when converted into an ONNX (Open Neural Network Exchange) format, utilizes a variety of operators that are supported by the ONNX framework.
While the specific list of operators can depend on the implementation details and the framework used (like TensorFlow, PyTorch, etc.), common operators for MobileNetSSDv2 in ONNX typically include:
1) Conv: Convolution operator.
2) Add: Element-wise addition.
3) Concat: Concatenation of tensors.
4) Transpose: Permuting the dimensions of tensors.
5) Shape: Getting the shape of a tensor.
6) Softmax: Softmax activation function.
7) Mul: Element-wise multiplication.
8) Slice: Slicing the tensor along a specific axis.
9) Clip: Clipping tensor values to a specified min and max.
10) Exp: Exponential function.
11) Div: Element-wise division.
12) Gather: Gathering elements along an axis.
13) Reshape: Reshaping of tensors.
14) Unsqueeze: Inserting single-dimensional entries to the shape.
These operators allow MobileNetSSDv2 to perform the necessary computations for feature extraction, processing, and final object detection tasks.

### For yolov8 in more the onnx operators are :
15) Sigmoid: Sigmoid activation function.
16) MaxPool: Max Pooling.
17) Resize: Scaling the size of images.
18) Sub: Element-wise substraction.

### For Classic inference layer (and advanced regression or prediction) in more than the previous operators it is necessary to add :
19) LeakyRelu: Leaky Rectified Linear Unit.
20) Relu: Rectified Linear Unit activation.
21) Pad: Padding around the tensor.
22) ReduceMean: Computing the mean of elements along a specified axis.
23) Log: Logarithm function.
24) Gemm: General Matrix Multiplication.
25) MatMul: Matrix Multiplication.
26) Flatten: Flattening a tensor into a 2D matrix.
27) HardSwish - Applies the Hard Swish activation function.
28) Min - Performs element-wise minimum of two tensors.
29) Max - Performs element-wise maximum of two tensors.
30) Abs - Applies the absolute value element-wise on the input tensor.
31) GRU - Gated Recurrent Unit, a type of recurrent neural network (RNN) layer.
32) LSTM - Long Short-Term Memory, another type of recurrent neural network (RNN) layer.



# Use case `<name of the use case>` - `<provider>`

## Description
_Brief description of the use case. This description is optional, but providing a short description will make your need easier to understand._

## Models architecture
_Description of the model architecture(s). This can be provided explicitly (e.g., a Netron output), a reference to an existing model (e.g.,"Yolo Vx"), an ONNX file or a combination of these data_

## Operators
_List of operators_
