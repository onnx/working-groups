"""
Pad ONNX example.
"""
import numpy as np

from onnx import helper, TensorProto
import onnx.checker
import onnx.printer
from onnxruntime import InferenceSession


# Create inputs
x = helper.make_tensor_value_info('x', TensorProto.FLOAT, [8, 8])
pads = helper.make_tensor_value_info('pads', TensorProto.INT64, [4])

# Create a node (Pad) with input/outputs
pad_node = helper.make_node(
    'Pad',
    ['x', 'pads'],
    ['x_padded'],
    mode='constant'
)

# Create the graph
graph_def = helper.make_graph(
    [pad_node],
    'test-pad',
    [x, pads],
    [helper.make_tensor_value_info('x_padded', TensorProto.FLOAT, [1, 1, 4, 4])],
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
x = np.ones((8, 8), dtype=np.float32)
pads_values = [2,1,2,2]

x_padded = sess.run(None, {'x': x, 'pads': pads_values})[0]

print("Output:")
print(x_padded)
