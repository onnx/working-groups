"""
This file uses the Hypothesis library to generate a wide range of test cases
for the Matmul operation in ONNX.
"""
import os

import json
import numpy as np

from onnx import helper
import onnx.checker
from onnxruntime import InferenceSession


from hypothesis import given, settings
import hypothesis.extra.numpy as hnp
from hypothesis import strategies as st

if os.path.exists("generated_data.json"):
    os.remove("generated_data.json")

"""
Inputs/attributes details
"""
inputs_attributes = {
    "min_size_input_axis": 1, # If you generate UINT32/UINT64, you cant set this to 0.
    "max_size_input_axis": 10, # Adjust as needed
    "ONNXRuntime_Provider": "CPUExecutionProvider" # available providers are CPUExecutionProvider, CUDAExecutionProvider, DmlExecutionProvider 
}

"""
Matmul supported types
"""
matmul_types = {
    "CPUExecutionProvider": {
        "INT32": np.int32,
        "INT64": np.int64,
        "UINT32": np.uint32,
        "UINT64": np.uint64,
        "FP32": np.float32,
        "FP64": np.float64
    },
    "CUDAExecutionProvider": {
        "FP16": np.float16,
        "FP32": np.float32,
        "FP64": np.float64
    },
    "DmlExecutionProvider": {
        "FP16": np.float16,
        "FP32": np.float32
    }
}

"""
Store generated data
"""
generated_data = {
    "size_input_a": [],
    "size_input_b": []
}

"""
Function to generate valid matmul arguments
"""
@st.composite
def valid_matmul_args(draw):

    #---------------------------------------------------
    # Restrictions
    #---------------------------------------------------
    # Type Consistency

    all_valid_types = list(matmul_types.get(inputs_attributes["ONNXRuntime_Provider"]).keys())
    dtype_name = draw(st.sampled_from(all_valid_types))
    dtype = matmul_types[inputs_attributes["ONNXRuntime_Provider"]][dtype_name]

    if np.issubdtype(dtype, np.integer):
        min_value = np.iinfo(dtype).min
        max_value = np.iinfo(dtype).max
        a_numeric = st.integers(min_value=min_value, max_value=max_value)
    elif np.issubdtype(dtype, np.floating):
        min_value = np.finfo(dtype).min
        max_value = np.finfo(dtype).max
        a_numeric = st.floats(min_value=min_value, max_value=max_value)

    #---------------------------------------------------
    # Input A
    #---------------------------------------------------

    # a_shape is the shape of input tensor A
    # A [C1]
    a_rank = 2
    a_shape = []

    for _ in range(a_rank):
        dim = draw(st.integers(
            min_value=inputs_attributes["min_size_input_axis"],
            max_value=inputs_attributes["max_size_input_axis"]))
        a_shape.append(dim)

    # Create input tensor A 
    a = draw(hnp.arrays(dtype=dtype, shape=a_shape, elements=a_numeric))

    #---------------------------------------------------
    # Input B
    #---------------------------------------------------
    
    # b_shape is the shape of input tensor B
    # B [C1]
    b_rank = 2
    b_shape = [0] * b_rank
    
    # B [C2] -> A [C2]
    b_shape[0] = a_shape[1]

    dim  = draw(st.integers(
            min_value=inputs_attributes["min_size_input_axis"],
            max_value=inputs_attributes["max_size_input_axis"]))
    b_shape[1] = dim

    #Create input tensor B
    b = draw(hnp.arrays(dtype=dtype, shape=b_shape, elements=a_numeric))

    #---------------------------------------------------
    # Output Y
    #---------------------------------------------------
    
    # y_shape is the shape of output tensor Y
    # Y [C1]
    # Y [C2] -> A [C2]
    # Y [C2] -> B [C2]
    y_shape = [a_shape[0], b_shape[1]]

    return (a_shape, b_shape, a, b, dtype_name, y_shape)

"""
Function that runs the test
"""
@settings(max_examples=20000, deadline=None)
@given(valid_matmul_args())
def test_matmul(args):
    a_shape, b_shape, a, b, dtype_name, y_shape = args
    generated_data["size_input_a"].append(a_shape)
    generated_data["size_input_b"].append(b_shape)

    y = run_onnx_matmul(a_shape, b_shape, a, b, dtype_name, y_shape, inputs_attributes["ONNXRuntime_Provider"])
    check_constraints(a, b, y)


def teardown_module():
    """
    Function to write generated data to a json file
    """
    data = {
        "title": "Data generated for testing ONNX Matmul Operator",
        "min_size_input_a": inputs_attributes["min_size_input_axis"],
        "max_size_input_a": inputs_attributes["max_size_input_axis"],
        "size_input_a": generated_data["size_input_a"],
        "min_size_input_b": inputs_attributes["min_size_input_axis"],
        "max_size_input_b": inputs_attributes["max_size_input_axis"],
        "size_input_b": generated_data["size_input_b"]
    }

    with open("generated_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def run_onnx_matmul(a_shape, b_shape, a, b, dtype_name, y_shape, provider):
    """
    Function that runs the ONNX Matmul operation
    """

    # Create inputs
    a_onnx = helper.make_tensor_value_info('a',
                                      helper.np_dtype_to_tensor_dtype(a.dtype),
                                      list(a_shape))
    b_onnx = helper.make_tensor_value_info('b',
                                      helper.np_dtype_to_tensor_dtype(b.dtype),
                                      list(b_shape))

    node_def = helper.make_node(
        'MatMul',
        ['a', 'b'],
        ['y']
    )

    # Create the graph
    graph_def = helper.make_graph(
        [node_def],
        'test-matmul',
        [a_onnx, b_onnx],
        [helper.make_tensor_value_info('y',
                                       helper.np_dtype_to_tensor_dtype(a.dtype),
                                       y_shape)],
    )

    onnx_model = helper.make_model(graph_def)

    #Let's freeze the opset.
    del onnx_model.opset_import[:]
    opset = onnx_model.opset_import.add()
    opset.domain = ''
    opset.version = 13
    onnx_model.ir_version = 10

    # Verify the model
    onnx.checker.check_model(onnx_model)

    # Do inference
    sess = InferenceSession(onnx_model.SerializeToString(),
                                providers=[provider])

    y = sess.run(None, {'a': a, 'b': b})[0]

    for tensor in [a, b]:
        print("a shape:", tensor.shape)
        print("a values:", tensor)

    print("y shape:", y.shape)
    print("y values:", y)
    print("y data type:", y.dtype)
    return y

def matrix_multiplication (a,b): 
    """
    Function that performs matrix multiplication
    """
    a_rows = a.shape[0]
    b_cols = b.shape[1]
    
    y = np.zeros((a_rows, b_cols), dtype=a.dtype)
    for i in range (a_rows):
        for j in range(b_cols):
            sum = 0
            for k in range(a.shape[1]):
                sum += a[i][k] * b[k][j]
            y[i][j] = sum
    return y

def check_constraints(a, b, y):
    """
    Function that defines asserts for the constraints
    """

    # Inputs Constraints
    # A [C1]
    # B [C1]
    # Y [C1]
    assert len(a.shape) == len(b.shape) == len(y.shape) == 2

    # A [C2] - Shape Consistency
    # B [C2] -> A [C2]
    assert a.shape[1] == b.shape[0]

    # Type consistency
    assert a.dtype == b.dtype == y.dtype

    # A [C3] - Output Shape
    # B [C3] 
    # Y [C3] -> A [C3], B [C3]
    assert y.shape == (a.shape[0], b.shape[1])

    # Output Result Check
    y_expected = matrix_multiplication(a, b)
    # Note: Due to rounding errors the entries are compared with a tolerance.
    if not (np.isinf(y_expected).any() or np.isnan(y_expected).any()):
        assert np.allclose(y, y_expected, rtol=1e-05, atol=1e-08, equal_nan=True)

