# @title Standard convolution (3 channels)
import numpy
from onnx import *
from onnx import helper
import onnx.checker
from onnxruntime import InferenceSession

# Create inputs
x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [1, 1, 2, 2])
w = helper.make_tensor_value_info('w', TensorProto.FLOAT, [2, 1, 1, 1])
b = helper.make_tensor_value_info('b', TensorProto.FLOAT, [2])

# Create a node (Conv) with input/outputs
node_def = helper.make_node(
    'Conv', # node name
    ['x', 'w', 'b'], # inputs
    ['y'], # outputs
    dilations=[1,1],
    kernel_shape=[1,1],
    pads=[0, 0, 0, 0],
    strides=[1, 1],
    auto_pad='NOTSET',
    group=1, # Standard convolution
)

# Create the graph
graph_def = helper.make_graph(
    [node_def],
    'test-conv',
    [x, w, b],
    [helper.make_tensor_value_info('y', TensorProto.FLOAT, [1, 1, 4, 4])],
)

onnx_model = helper.make_model(graph_def)

# Let's freeze the opset.
del onnx_model.opset_import[:]
opset = onnx_model.opset_import.add()
opset.domain = ''
opset.version = 15
onnx_model.ir_version = 8

# Verify the model
onnx.checker.check_model(onnx_model)

# Print a human-readable representation of the graph
print(onnx.helper.printable_graph(onnx_model.graph))

# Do inference
sess = InferenceSession(onnx_model.SerializeToString(),
                        providers=["CPUExecutionProvider"])

# Initialize tensors
x = numpy.ones((1, 1, 2, 2), dtype=numpy.float32)
w = numpy.ones((2, 1, 1, 1), dtype=numpy.float32)
b = numpy.array([5.0,5.0], dtype=numpy.float32)

y = sess.run(None, {'x': x, 'w':w, 'b': b})[0]

print("X shape:", x.shape)
print("X:", x)

print("W shape:", w.shape)
print("W:", w)

print("B shape:",
      b.shape)
print("B:", b)

print("Y shape:", y.shape)
print("Y:", y)
