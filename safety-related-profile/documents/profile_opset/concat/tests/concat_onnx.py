#!/usr/bin/env python3  
# -*- coding: utf-8 -*- 
# ----------------------------------------------------------------------------
# Created By  : Salome Marty Laurent  
# Created Date: 08/04/2025
# version ='1.0'
# ---------------------------------------------------------------------------

""" This file was designed to caracterize and test the ONNX operator: Concat

Five main tests are defined: 
    - Concat with one input tensor (line 24)
    - Concat with scalar inputs (line 83)
    - Concat with input matrixes (line 152)
    - Concat with 4D tensors inputs (line 223)
    - Concat with 4D tensors in a reverse order (line 296)"""  


# ---------------------------------------------------------------------------

import onnxruntime
import onnx
import numpy

# ---------------------------------------------------------------------------

""" ONNX Concat operator: test with one input tensor """
# ---------------------------------------------------------------------------

# Create inputs
x = onnx.helper.make_tensor_value_info('x', onnx.helper.TensorProto.FLOAT, [2,3])


# Create a node (Conv) with input/outputs
node_def = onnx.helper.make_node(
    'Concat', # node name
    ['x'], # inputs
    ['c'], # output
    axis=0, # Axis 0
)

# Create the graph
graph_def = onnx.helper.make_graph(
    [node_def],
    'test-concat',
    [x],
    [onnx.helper.make_tensor_value_info('c', onnx.helper.TensorProto.FLOAT, [2,3])],
)

onnx_model = onnx.helper.make_model(graph_def)

# Let's freeze the opset.
del onnx_model.opset_import[:]
opset = onnx_model.opset_import.add()
opset.domain = ''
opset.version = 15
onnx_model.ir_version = 8

# Verify the model
onnx.checker.check_model(onnx_model)
print("\n Test with one input: \n")
# Print a human-readable representation of the graph
print(onnx.helper.printable_graph(onnx_model.graph))

# Do inference
sess = onnxruntime.InferenceSession(onnx_model.SerializeToString(),
                        providers=["CPUExecutionProvider"])

# Initialize tensors
x = 1* numpy.ones((2,3), dtype=numpy.float32)



c = sess.run(None, {'x': x})[0]

print("X shape:", x.shape)
print("X:", x)

print("C shape:", c.shape)
print("C:", c)


# ---------------------------------------------------------------------------

""" ONNX Concat operator: test with scalar inputs """

# ---------------------------------------------------------------------------

# Create inputs
x = onnx.helper.make_tensor_value_info('x', onnx.helper.TensorProto.FLOAT, [1])
y = onnx.helper.make_tensor_value_info('y', onnx.helper.TensorProto.FLOAT, [1])
z = onnx.helper.make_tensor_value_info('z', onnx.helper.TensorProto.FLOAT, [1])


# Create a node (Conv) with input/outputs
node_def = onnx.helper.make_node(
    'Concat', # node name
    ['x', 'y', 'z'], # inputs
    ['c'], # output
    axis=0, # Axis 0
)

# Create the graph
graph_def = onnx.helper.make_graph(
    [node_def],
    'test-concat',
    [x, y, z],
    [onnx.helper.make_tensor_value_info('c', onnx.helper.TensorProto.FLOAT, [3])],
)

onnx_model = onnx.helper.make_model(graph_def)

# Let's freeze the opset.
del onnx_model.opset_import[:]
opset = onnx_model.opset_import.add()
opset.domain = ''
opset.version = 15
onnx_model.ir_version = 8

# Verify the model
onnx.checker.check_model(onnx_model)
print("\n Test with scalar inputs: \n")
# Print a human-readable representation of the graph
print(onnx.helper.printable_graph(onnx_model.graph))

# Do inference
sess = onnxruntime.InferenceSession(onnx_model.SerializeToString(),
                        providers=["CPUExecutionProvider"])

# Initialize tensors
x = 1* numpy.ones((1), dtype=numpy.float32)
y = 2* numpy.ones((1), dtype=numpy.float32)
z = 3* numpy.ones((1), dtype=numpy.float32)


c = sess.run(None, {'x': x, 'y':y, 'z': z})[0]

print("X shape:", x.shape)
print("X:", x)

print("Y shape:", y.shape)
print("Y:", y)

print("Z shape:",
      z.shape)
print("Z:", z)

print("C shape:", c.shape)
print("C:", c)


# ---------------------------------------------------------------------------

""" ONNX Concat operator: test with input matrixes """

# ---------------------------------------------------------------------------


# Create inputs
x = onnx.helper.make_tensor_value_info('x', onnx.helper.TensorProto.FLOAT, [2, 3])
y = onnx.helper.make_tensor_value_info('y', onnx.helper.TensorProto.FLOAT, [4, 3])
z = onnx.helper.make_tensor_value_info('z', onnx.helper.TensorProto.FLOAT, [3, 3])


# Create a node (Conv) with input/outputs
node_def = onnx.helper.make_node(
    'Concat', # node name
    ['x', 'y', 'z'], # inputs
    ['c'], # output
    axis=0, # Axis 0
)

# Create the graph
graph_def = onnx.helper.make_graph(
    [node_def],
    'test-concat',
    [x, y, z],
    [onnx.helper.make_tensor_value_info('c', onnx.helper.TensorProto.FLOAT, [9, 3])],
)

onnx_model = onnx.helper.make_model(graph_def)

# Let's freeze the opset.
del onnx_model.opset_import[:]
opset = onnx_model.opset_import.add()
opset.domain = ''
opset.version = 15
onnx_model.ir_version = 8

# Verify the model
onnx.checker.check_model(onnx_model)

print("\n Test with input matrixes: \n")
# Print a human-readable representation of the graph
print(onnx.helper.printable_graph(onnx_model.graph))

# Do inference
sess = onnxruntime.InferenceSession(onnx_model.SerializeToString(),
                        providers=["CPUExecutionProvider"])

# Initialize tensors
x = 1* numpy.ones((2, 3), dtype=numpy.float32)
y = 2* numpy.ones((4, 3), dtype=numpy.float32)
z = 3* numpy.ones((3, 3), dtype=numpy.float32)


c = sess.run(None, {'x': x, 'y':y, 'z': z})[0]

print("X shape:", x.shape)
print("X:", x)

print("Y shape:", y.shape)
print("Y:", y)

print("Z shape:",
      z.shape)
print("Z:", z)

print("C shape:", c.shape)
print("C:", c)


# ---------------------------------------------------------------------------

""" ONNX Concat operator: test with 4D tensors inputs  """

# ---------------------------------------------------------------------------

# Create inputs
x = onnx.helper.make_tensor_value_info('x', onnx.helper.TensorProto.FLOAT, [1, 1, 3, 2])
y = onnx.helper.make_tensor_value_info('y', onnx.helper.TensorProto.FLOAT, [1, 3, 3, 2])
z = onnx.helper.make_tensor_value_info('z', onnx.helper.TensorProto.FLOAT, [1, 2, 3, 2])
w = onnx.helper.make_tensor_value_info('w', onnx.helper.TensorProto.FLOAT, [1, 4, 3, 2])


# Create a node (Conv) with input/outputs
node_def = onnx.helper.make_node(
    'Concat', # node name
    ['x', 'y', 'z', 'w'], # inputs
    ['c'], # output
    axis=1, # Axis 1
)

# Create the graph
graph_def = onnx.helper.make_graph(
    [node_def],
    'test-concat',
    [x, y, z, w],
    [onnx.helper.make_tensor_value_info('c', onnx.helper.TensorProto.FLOAT, [1, 10, 3, 2])],
)

onnx_model = onnx.helper.make_model(graph_def)

# Let's freeze the opset.
del onnx_model.opset_import[:]
opset = onnx_model.opset_import.add()
opset.domain = ''
opset.version = 15
onnx_model.ir_version = 8

# Verify the model
onnx.checker.check_model(onnx_model)

print("\n Test with 4D tensor inputs: \n")
# Print a human-readable representation of the graph
print(onnx.helper.printable_graph(onnx_model.graph))

# Do inference
sess = onnxruntime.InferenceSession(onnx_model.SerializeToString(),
                        providers=["CPUExecutionProvider"])

# Initialize tensors
x = 3* numpy.ones((1, 1, 3, 2), dtype=numpy.float32)
y = 4* numpy.ones((1, 3, 3, 2), dtype=numpy.float32)
z = 5* numpy.ones((1, 2, 3, 2), dtype=numpy.float32)
w = 6* numpy.ones((1, 4, 3, 2), dtype=numpy.float32)

c = sess.run(None, {'x': x, 'y':y, 'z': z, 'w': w})[0]

print("X shape:", x.shape)
print("X:", x)

print("Y shape:", y.shape)
print("Y:", y)

print("Z shape:",
      z.shape)
print("Z:", z)

print("W shape:", w.shape)
print("W:", w)

print("C shape:", c.shape)
print("C:", c)

# ---------------------------------------------------------------------------

""" ONNX Concat operator: test with 4D tensors inputs in a reverse order """

# ---------------------------------------------------------------------------

# Create inputs
x = onnx.helper.make_tensor_value_info('x', onnx.helper.TensorProto.FLOAT, [1, 1, 3, 2])
y = onnx.helper.make_tensor_value_info('y', onnx.helper.TensorProto.FLOAT, [1, 3, 3, 2])
z = onnx.helper.make_tensor_value_info('z', onnx.helper.TensorProto.FLOAT, [1, 2, 3, 2])
w = onnx.helper.make_tensor_value_info('w', onnx.helper.TensorProto.FLOAT, [1, 4, 3, 2])

# Create a node (Conv) with input/outputs
node_def_reverse = onnx.helper.make_node(
    'Concat', # node name
    ['w', 'z', 'y', 'x'], # inputs
    ['c_reverse'], # output
    axis=1, # Axis 1
)

# Create the graph
graph_def_reverse = onnx.helper.make_graph(
    [node_def_reverse],
    'test-concat-reverse',
    [w, z, y, x],
    [onnx.helper.make_tensor_value_info('c_reverse', onnx.helper.TensorProto.FLOAT, [1, 10, 3, 2])],
)

onnx_model_reverse = onnx.helper.make_model(graph_def_reverse)

# Let's freeze the opset.
del onnx_model_reverse.opset_import[:]
opset = onnx_model_reverse.opset_import.add()
opset.domain = ''
opset.version = 15
onnx_model_reverse.ir_version = 8

# Verify the model
onnx.checker.check_model(onnx_model_reverse)

print("\n Test with 4D tensor inputs in a reverse order: \n")
# Print a human-readable representation of the graph
print(onnx.helper.printable_graph(onnx_model_reverse.graph))

# Do inference
sess = onnxruntime.InferenceSession(onnx_model_reverse.SerializeToString(),
                        providers=["CPUExecutionProvider"])

# Initialize tensors
x = 3* numpy.ones((1, 1, 3, 2), dtype=numpy.float32)
y = 4* numpy.ones((1, 3, 3, 2), dtype=numpy.float32)
z = 5* numpy.ones((1, 2, 3, 2), dtype=numpy.float32)
w = 6* numpy.ones((1, 4, 3, 2), dtype=numpy.float32)

c_reverse = sess.run(None, {'w': w, 'z':z, 'y': y, 'x': x})[0]

print("W shape:", w.shape)
print("W:", w)

print("Z shape:", z.shape)
print("Z:", y)

print("Y shape:",
      y.shape)
print("Y:", z)

print("X shape:", x.shape)
print("X:", x)

print("C shape:", c_reverse.shape)
print("C:", c_reverse)
