#!/usr/bin/env python3  
# -*- coding: utf-8 -*- 
# ----------------------------------------------------------------------------
# Created By  : Salome Marty Laurent  
# Created Date: 08/04/2025
# version ='1.0'
# ---------------------------------------------------------------------------

""" This file was designed to caracterize and test the ONNX operator: Concat

Five main tests are defined: 
    - Concat with two empty tensors as scalar values (28)
    - Concat with one input tensor (line 100)
    - Concat with vector inputs (line 166)
    - Concat with input matrixes (line 236)
    - Concat with 3D tensors inputs (line 306 )
    - Concat with 4D tensors inputs (line 416 )
    - Concat with 4D tensors in a reverse order (line 489)
    - Concat with string matrixes (line 545 )
    - Concat with boolean matrixes (line 630 )
    - Concat with complex64 matrixes (line 709 )
    - Concat with complex128 matrixes (line 808 )"""  


# ---------------------------------------------------------------------------

import onnxruntime
import onnx
import numpy

print(onnxruntime.__version__)

# ---------------------------------------------------------------------------

""" ONNX Concat operator: test two empty tensors as scalar values """

# ---------------------------------------------------------------------------

x_val_info = onnx.helper.make_tensor_value_info('x', onnx.helper.TensorProto.FLOAT, [])
y_val_info = onnx.helper.make_tensor_value_info('y', onnx.helper.TensorProto.FLOAT, [])


# Create a node (Concat) with input/outputs
node_def = onnx.helper.make_node(
    'Concat', 
    ['x', 'y'], 
    ['c'], 
    axis=0, 
)


graph_def = onnx.helper.make_graph(
    [node_def],
    'test-concat-scalars',
    [x_val_info, y_val_info], 
    [onnx.helper.make_tensor_value_info('c', onnx.helper.TensorProto.FLOAT, [2])], 
)

onnx_model = onnx.helper.make_model(graph_def, producer_name='onnx-scalar-concat-test')

# Set Opset
del onnx_model.opset_import[:]
opset = onnx_model.opset_import.add()
opset.domain = ''
opset.version = 15 
onnx_model.ir_version = 8 

# Verify the model
try:
    onnx.checker.check_model(onnx_model)
except onnx.checker.ValidationError as e:
    print(f"ONNX model invalid: {e}")


print("\nTest with scalar inputs for Concat (axis=0):\n")
print(onnx.helper.printable_graph(onnx_model.graph))

# Initialize tensors
x_np = numpy.array(1.0, dtype=numpy.float32) 
y_np = numpy.array(2.0, dtype=numpy.float32) 


# Do inference with try-except block
try:
    print("\nAttempting to create InferenceSession and run...")
    sess = onnxruntime.InferenceSession(onnx_model.SerializeToString(),
                                        providers=["CPUExecutionProvider"])
    
    c_result = sess.run(None, {'x': x_np, 'y': y_np})[0]

    print("\nInference successful (if this line is reached).")
    print("Output C shape:", c_result.shape)
    print("Output C value:", c_result)

   
except onnxruntime.capi.onnxruntime_pybind11_state.Fail as e:
    print("\n--- ONNX Runtime Execution Error Caught ---")
    print(f"Error Type: {type(e)}")
    print(f"Error Message: {e}")
    print("This error is expected if ONNX Runtime's Concat shape inferencer not validates axis for rank-0 inputs.")
    
except Exception as e:
    print("\n--- An Unexpected Error Occurred ---")
    print(f"Error Type: {type(e)}")
    print(f"Error Message: {e}")

print("\nScript execution continued after inference attempt.")



# ---------------------------------------------------------------------------

""" ONNX Concat operator: test with one input tensor """

# ---------------------------------------------------------------------------

# Create inputs
x = onnx.helper.make_tensor_value_info('x', onnx.helper.TensorProto.FLOAT, [1])



# Create a node (Concat) with input/outputs
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
    [onnx.helper.make_tensor_value_info('c', onnx.helper.TensorProto.FLOAT, [1])],
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



c = sess.run(None, {'x': x})[0]

print("X shape:", x.shape)
print("X:", x)

print("C shape:", c.shape)
print("C:", c)


# ---------------------------------------------------------------------------

""" ONNX Concat operator: test with vector inputs """

# ---------------------------------------------------------------------------

# Create inputs
x = onnx.helper.make_tensor_value_info('x', onnx.helper.TensorProto.FLOAT, [1])
y = onnx.helper.make_tensor_value_info('y', onnx.helper.TensorProto.FLOAT, [1])
z = onnx.helper.make_tensor_value_info('z', onnx.helper.TensorProto.FLOAT, [1])


# Create a node (Concat) with input/outputs
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


# Create a node (Concat) with input/outputs
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


x = numpy.array([[1, 2, 3],
                 [4, 5, 6]], dtype=numpy.float32)


y = numpy.array([[7,  8,  9],
                 [10, 11, 12],
                 [13, 14, 15],
                 [16, 17, 18]], dtype=numpy.float32)


z = numpy.array([[20, 21, 22],
                 [23, 24, 25],
                 [26, 27, 28]], dtype=numpy.float32)


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

""" ONNX Concat operator: test with 3D inputs tensors """

# ---------------------------------------------------------------------------


# Create inputs
x = onnx.helper.make_tensor_value_info('x', onnx.helper.TensorProto.FLOAT, [2, 3, 4])
y = onnx.helper.make_tensor_value_info('y', onnx.helper.TensorProto.FLOAT, [2, 3, 4])


# Create a node (Concat) with input/outputs
node_def_4D = onnx.helper.make_node(
    'Concat', # node name
    ['x', 'y'], # inputs
    ['c'], # output
    axis=2, # Axis 2
)


# Create the graph
graph_def_4D = onnx.helper.make_graph(
    [node_def_4D],
    'test-concat',
    [x, y],
    [onnx.helper.make_tensor_value_info('c', onnx.helper.TensorProto.FLOAT, [2, 3, 8])],
)

onnx_model = onnx.helper.make_model(graph_def_4D)

# Let's freeze the opset.
del onnx_model.opset_import[:]
opset = onnx_model.opset_import.add()
opset.domain = ''
opset.version = 15
onnx_model.ir_version = 8

# Verify the model
onnx.checker.check_model(onnx_model)

print("\n Test with 3D input tensors: \n")
# Print a human-readable representation of the graph
print(onnx.helper.printable_graph(onnx_model.graph))

# Do inference
sess = onnxruntime.InferenceSession(onnx_model.SerializeToString(),
                        providers=["CPUExecutionProvider"])

# Initialize tensors
x = numpy.array([
    [ 
        [ 1.00, 2.00, 3.00, 10.00 ],
        [ 4.00, 5.00, 6.00, 11.00 ],
        [ 7.00, 8.00, 9.00, 12.00 ]
    ],
    [ 
        [ 11.00, 12.00, 13.00, 20.00 ],
        [ 14.00, 15.00, 16.00, 21.00 ],
        [ 17.00, 18.00, 19.00, 22.00 ]
    ]
], dtype=numpy.float32) 


y = numpy.array([
    [ 
        [ 101.00, 102.00, 103.00, 110.00 ],
        [ 104.00, 105.00, 106.00, 120.00 ],
        [ 107.00, 108.00, 109.00, 130.00 ]
    ],
    [ 
        [ 111.00, 112.00, 113.00, 120.00 ],
        [ 114.00, 115.00, 116.00, 121.00 ],
        [ 117.00, 118.00, 119.00, 122.00 ]
    ]
], dtype=numpy.float32)


c = sess.run(None, {'x': x, 'y':y})[0]

print("X shape:", x.shape)
print("X:", x)

print("Y shape:", y.shape)
print("Y:", y)


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


# Create a node (Concat) with input/outputs
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

# Create a node (Concat) with input/outputs
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

# ---------------------------------------------------------------------------

""" ONNX Concat operator: test with string input matrixes """

# ---------------------------------------------------------------------------


x_val_info = onnx.helper.make_tensor_value_info('x', onnx.TensorProto.STRING, [2, 3])
y_val_info = onnx.helper.make_tensor_value_info('y', onnx.TensorProto.STRING, [2, 3])

# Output 'c' will be a [4,3] string tensor when concatenating along axis=0
output_shape = [4, 3]
c_val_info = onnx.helper.make_tensor_value_info('c', onnx.TensorProto.STRING, output_shape)

# Create the Concat Node
node_def_string = onnx.helper.make_node(
    'Concat',       # node name
    ['x', 'y'],     # inputs
    ['c'],          # output
    axis=0,         # Concatenate along the first axis (rows)
)

# 3. Create the Graph
graph_def_string = onnx.helper.make_graph(
    [node_def_string],
    'test-concat-strings', 
    [x_val_info, y_val_info],   
    [c_val_info],          
)

# 4. Create the Model
onnx_model = onnx.helper.make_model(graph_def_string, producer_name='onnx-string-concat-test')

# 5. Set Opset
del onnx_model.opset_import[:]
opset = onnx_model.opset_import.add()
opset.domain = ''
opset.version = 15 
onnx_model.ir_version = 8


onnx.checker.check_model(onnx_model)



print("\nTest with 2D string input tensors for Concat (axis=0):\n")
print(onnx.helper.printable_graph(onnx_model.graph))

# Initialize NumPy Tensors with Python strings

x_np = numpy.array([
    ['Alpha', 'Beta', 'Gamma'],
    ['Delta', 'Epsilon', 'Zeta']
], dtype=object)

y_np = numpy.array([
    ['Eta', 'Theta', 'Iota'],
    ['Kappa', 'Lambda', 'Mu']
], dtype=object)

print("\nInput X shape:", x_np.shape, "\nX value:\n", x_np)
print("\nInput Y shape:", y_np.shape, "\nY value:\n", y_np)

#Do Inference with try-except block

print("\nAttempting to create InferenceSession and run...")
sess = onnxruntime.InferenceSession(onnx_model.SerializeToString(),
                                        providers=["CPUExecutionProvider"])
    
  
c_result = sess.run(None, {'x': x_np, 'y': y_np})[0]

print("\nInference successful.")
print("Output C shape:", c_result.shape)
print("Output C value:\n", c_result)

# Verify the result
expected_c = numpy.array([
    ['Alpha', 'Beta', 'Gamma'],
    ['Delta', 'Epsilon', 'Zeta'],
    ['Eta', 'Theta', 'Iota'],
    ['Kappa', 'Lambda', 'Mu']
], dtype=object)

   
# ---------------------------------------------------------------------------

""" ONNX Concat operator: test with boolean input matrixes """

# ---------------------------------------------------------------------------

x_val_info = onnx.helper.make_tensor_value_info('x', onnx.TensorProto.BOOL, [2, 3])
y_val_info = onnx.helper.make_tensor_value_info('y', onnx.TensorProto.BOOL, [2, 3])


concat_axis = 1
output_shape = [2, 6]
c_val_info = onnx.helper.make_tensor_value_info('c', onnx.TensorProto.BOOL, output_shape)

# Create the Concat Node
node_def_bool = onnx.helper.make_node(
    'Concat',       # node name
    ['x', 'y'],     # inputs
    ['c'],          # output
    axis=concat_axis, 
)

# Create the Graph
graph_def_bool = onnx.helper.make_graph(
    [node_def_bool],
    'test-concat-booleans', 
    [x_val_info, y_val_info],   
    [c_val_info],          
)

print("\n")
print("\nTest with 2D boolean input tensors for Concat (axis=1):\n")
# Create the Model
onnx_model = onnx.helper.make_model(graph_def_bool, producer_name='onnx-boolean-concat-test')

# Set Opset
del onnx_model.opset_import[:]
opset = onnx_model.opset_import.add()
opset.domain = ''
opset.version = 15 # Concat for booleans is well-supported
onnx_model.ir_version = 8

# Verify the Model

onnx.checker.check_model(onnx_model)



print(onnx.helper.printable_graph(onnx_model.graph))

# Initialize NumPy Tensors with boolean values
x_np = numpy.array([
    [True, False, True],
    [False, True, False]
], dtype=bool)

y_np = numpy.array([
    [False, False, True],
    [True, True, False]
], dtype=bool)

print("\nInput X shape:", x_np.shape, "\nX value:\n", x_np)
print("\nInput Y shape:", y_np.shape, "\nY value:\n", y_np)


sess = onnxruntime.InferenceSession(onnx_model.SerializeToString(),
                                        providers=["CPUExecutionProvider"])
    
c_result = sess.run(None, {'x': x_np, 'y': y_np})[0]

print("\nInference successful.")
print("Output C shape:", c_result.shape)
print("Output C value:\n", c_result)

expected_c = numpy.array([
    [True, False, True, False, False, True],
    [False, True, False, True, True, False]
], dtype=bool)

# ---------------------------------------------------------------------------

""" ONNX Concat operator: test with complex64 input matrixes """

# ---------------------------------------------------------------------------

x_val_info = onnx.helper.make_tensor_value_info('x', onnx.TensorProto.COMPLEX64, [2, 2])
y_val_info = onnx.helper.make_tensor_value_info('y', onnx.TensorProto.COMPLEX64, [3, 2])


concat_axis = 0
output_shape = [5, 2]
c_val_info = onnx.helper.make_tensor_value_info('c', onnx.TensorProto.COMPLEX64, output_shape)

# Create the Concat Node
node_def_complex = onnx.helper.make_node(
    'Concat',       
    ['x', 'y'],     
    ['c'],          
    axis=concat_axis, # Concatenate along the specified axis
)

# Create the Graph
graph_def_complex = onnx.helper.make_graph(
    [node_def_complex],
    'test-concat-complex', 
    [x_val_info, y_val_info],   
    [c_val_info],          
)

# Create the Model

onnx_model = onnx.helper.make_model(graph_def_complex, producer_name='onnx-complex-concat-test')

# Set Opset
del onnx_model.opset_import[:]
opset = onnx_model.opset_import.add()
opset.domain = ''
opset.version = 15 # Concat for complex types is supported
onnx_model.ir_version = 8


onnx.checker.check_model(onnx_model)
   
print(f"\nTest with 2D complex input tensors for Concat (axis={concat_axis}):\n")
print(onnx.helper.printable_graph(onnx_model.graph))

# Initialize NumPy Tensors with complex values

x_np = numpy.array([
    [1+2j, 3+4j],
    [5+6j, 7+8j]
], dtype=numpy.complex64)

y_np = numpy.array([
    [9+10j, 11+12j],
    [13+14j, 15+16j],
    [17+18j, 19+20j]
], dtype=numpy.complex64)

print("\nInput X shape:", x_np.shape, "\nX value:\n", x_np)
print("\nInput Y shape:", y_np.shape, "\nY value:\n", y_np)

# Do Inference 

try:
    print("\nAttempting to create InferenceSession and run...")
    sess = onnxruntime.InferenceSession(onnx_model.SerializeToString(),
                                        providers=["CPUExecutionProvider"])
    
    c_result = sess.run(None, {'x': x_np, 'y': y_np})[0]

    print("\nInference successful.")
    print("Output C shape:", c_result.shape)
    print("Output C value:\n", c_result)

    # Verify the result
    expected_c = numpy.array([
        [1+2j, 3+4j],
        [5+6j, 7+8j],
        [9+10j, 11+12j],
        [13+14j, 15+16j],
        [17+18j, 19+20j]
    ], dtype=numpy.complex64)

except onnxruntime.capi.onnxruntime_pybind11_state.Fail as e:
    print("\n--- ONNX Runtime Execution Error Caught ---")
    print(f"Error Type: {type(e)}")
    print(f"Error Message: {e}")
   
except Exception as e:
    print("\n--- An Unexpected Error Occurred During Inference ---")
    print(f"Error Type: {type(e)}")
    print(f"Error Message: {e}")
    import traceback
    traceback.print_exc()

# ---------------------------------------------------------------------------

""" ONNX Concat operator: test with complex128 input matrixes """

# ---------------------------------------------------------------------------

x_val_info = onnx.helper.make_tensor_value_info('x', onnx.TensorProto.COMPLEX128, [2, 2])
y_val_info = onnx.helper.make_tensor_value_info('y', onnx.TensorProto.COMPLEX128, [3, 2])


concat_axis = 0
output_shape = [5, 2]
c_val_info = onnx.helper.make_tensor_value_info('c', onnx.TensorProto.COMPLEX128, output_shape)

# Create the Concat Node
node_def_complex = onnx.helper.make_node(
    'Concat',       # node name
    ['x', 'y'],     # inputs
    ['c'],          # output
    axis=concat_axis, 
)

# Create the Graph
graph_def_complex = onnx.helper.make_graph(
    [node_def_complex],
    'test-concat-complex128', 
    [x_val_info, y_val_info],   
    [c_val_info],          
)

# 4. Create the Model
onnx_model = onnx.helper.make_model(graph_def_complex, producer_name='onnx-complex128-concat-test')

# 5. Set Opset
del onnx_model.opset_import[:]
opset = onnx_model.opset_import.add()
opset.domain = ''
opset.version = 15 # Concat for complex types is supported
onnx_model.ir_version = 8

# 6. Verify the Model
try:
    onnx.checker.check_model(onnx_model)
    print("ONNX model with complex128 inputs is valid.")
except onnx.checker.ValidationError as e:
    print(f"ONNX model invalid: {e}")
    exit(1) # Exit if model check fails

print(f"\nTest with 2D complex128 input tensors for Concat (axis={concat_axis}):\n")
print(onnx.helper.printable_graph(onnx_model.graph))

# 7. Initialize NumPy Tensors with complex values
# dtype=numpy.complex128 corresponds to onnx.TensorProto.COMPLEX128
x_np = numpy.array([
    [1+2j, 3+4j],
    [5+6j, 7+8j]
], dtype=numpy.complex128)

y_np = numpy.array([
    [9+10j, 11+12j],
    [13+14j, 15+16j],
    [17+18j, 19+20j]
], dtype=numpy.complex128)

print("\nInput X shape:", x_np.shape, "\nX value:\n", x_np)
print("\nInput Y shape:", y_np.shape, "\nY value:\n", y_np)

# Do Inference with try-except block
try:
    print("\nAttempting to create InferenceSession and run...")
    sess = onnxruntime.InferenceSession(onnx_model.SerializeToString(),
                                        providers=["CPUExecutionProvider"])
    
    c_result = sess.run(None, {'x': x_np, 'y': y_np})[0]

    print("\nInference successful.")
    print("Output C shape:", c_result.shape)
    print("Output C value:\n", c_result)

    # Verify the result
    expected_c = numpy.array([
        [1+2j, 3+4j],
        [5+6j, 7+8j],
        [9+10j, 11+12j],
        [13+14j, 15+16j],
        [17+18j, 19+20j]
    ], dtype=numpy.complex128)

    
except onnxruntime.capi.onnxruntime_pybind11_state.Fail as e:
    print("\n--- ONNX Runtime Execution Error Caught ---")
    print(f"Error Type: {type(e)}")
    print(f"Error Message: {e}")
   
except Exception as e:
    print("\n--- An Unexpected Error Occurred During Inference ---")
    print(f"Error Type: {type(e)}")
    print(f"Error Message: {e}")
    import traceback
    traceback.print_exc()


print("\nScript execution finished.")
