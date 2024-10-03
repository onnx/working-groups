# TOOLS and UTILITIES

This directory contains some tools and utilities developed by the WG to support its activities.

## Prerequisites

install dependencies

`pip install -r requirements.txt`

## Run example for LeNet5

`inv depend`

Expected result for LeNet5:

```
onnx.__version__='1.16.1', opset=21, IR_VERSION=10

Operator dependencies:
AveragePool             v19
Conv            v11
Gemm            v13
Reshape         v21
Softmax         v13
Tanh            v13
```

## [onnx_depend.py](onnx_depend.py) 

The script prints the onnx Nodes' Opererator dependencies for opset 'ai.onnx'.

`python -m onnx_depend --model_path <model>.onnx`