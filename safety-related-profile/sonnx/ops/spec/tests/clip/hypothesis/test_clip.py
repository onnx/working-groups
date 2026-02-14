"""
This file uses the Hypothesis library to generate a wide range of test cases
for the Clip operation in ONNX.
"""
import os

import json
import numpy as np
import ml_dtypes

from onnx import helper
import onnx.checker
from onnxruntime import InferenceSession
import onnx.reference


import tensorflow as tf

from hypothesis import given, settings
import hypothesis.extra.numpy as hnp
from hypothesis import strategies as st

if os.path.exists("generated_data.json"):
    os.remove("generated_data.json")

"""
Inputs/attributes details
"""
inputs_attributes = {
    "min_shape_size_input_x": 0, # Adjust as needed
    "max_shape_size_input_x": 4, # Adjust as needed
    "min_size_input_axis": 1, # Dimension should always be positive (no zero dimensions)
    "max_size_input_axis": 10, # Adjust as needed
    "ONNXRuntime_Provider": "CPUExecutionProvider" # available providers are CPUExecutionProvider, CUDAExecutionProvider, DmlExecutionProvider 
}

"""
Clip supported types
"""
clip_types = {
    "CPUExecutionProvider": {
        "INT8": np.int8,
        "INT32": np.int32,
        "UINT8": np.uint8,
        "UINT32": np.uint32,
        "UINT64": np.uint64,
        "FP16": np.float16,
        "FP32": np.float32,
        "FP64": np.float64
    },
    "CUDAExecutionProvider": {
        "INT8": np.int8,
        "INT64": np.int64,
        "UINT8": np.uint8,
        "UINT64": np.uint64,
        "FP16": np.float16,
        "FP32": np.float32,
        "FP64": np.float64,
    },
    "DmlExecutionProvider": {
        "INT8": np.int8,
        "INT16": np.int16,
        "INT32": np.int32,
        "INT64": np.int64,
        "UINT8": np.uint8,
        "UINT16": np.uint16,
        "UINT32": np.uint32,
        "UINT64": np.uint64,
        "FP16": np.float16,
        "FP32": np.float32,
    }
}

"""
Store generated data
"""
generated_data = {
    "shape_size_input_x" : [],
    "size_input_axis": [],
    "l_tensor": [],
    "m_tensor": []
}

"""
Function to generate valid clip arguments
"""
@st.composite
def valid_clip_args(draw):

    #---------------------------------------------------
    # Restrictions
    #---------------------------------------------------
    # X [C2] - Type Consistency

    all_valid_types = list(clip_types.get(inputs_attributes["ONNXRuntime_Provider"]).keys())
    dtype_name = draw(st.sampled_from(all_valid_types))
    dtype = clip_types[inputs_attributes["ONNXRuntime_Provider"]][dtype_name]

    if np.issubdtype(dtype, np.integer):
        min_value = np.iinfo(dtype).min
        max_value = np.iinfo(dtype).max
        a_numeric = st.integers(min_value=min_value, max_value=max_value)
    elif np.issubdtype(dtype, np.floating):
        min_value = np.finfo(dtype).min
        max_value = np.finfo(dtype).max
        a_numeric = st.floats(min_value=min_value, max_value=max_value)

    #---------------------------------------------------
    # Input X
    #---------------------------------------------------
    
    # shape_size_input_x is the number of dimensions of input tensor X
    shape_size_input_x = draw(st.integers(
        min_value=inputs_attributes["min_shape_size_input_x"],
        max_value=inputs_attributes["max_shape_size_input_x"]))

    # x_shape is the shape of input tensor X
    x_shape = []
    for _ in range(shape_size_input_x):
        dim = draw(st.integers(
            min_value=inputs_attributes["min_size_input_axis"],
            max_value=inputs_attributes["max_size_input_axis"]))
        x_shape.append(dim)

    # Create input tensor X 
    # X [C2]
    x = draw(hnp.arrays(dtype=dtype, shape=x_shape, elements=a_numeric))

    #---------------------------------------------------
    # Input L
    #---------------------------------------------------

    # Create input tensor L
    # L [C1] -> X [C2]
    l = draw(hnp.arrays(dtype=dtype, shape=[], elements=a_numeric))

    #---------------------------------------------------
    # Input M
    #---------------------------------------------------

    # Create input tensor M
    # M [C1] -> X [C2]
    m = draw(hnp.arrays(dtype=dtype, shape=[], elements=a_numeric))

    #---------------------------------------------------
    # Output Y
    #---------------------------------------------------

    # Y [C1] -> X [C1]
    y_shape = x_shape

    return (x_shape, x, l, m, dtype_name, y_shape)

"""
Function that runs the test
"""
@settings(max_examples=20000, deadline=None)
@given(valid_clip_args())
def test_clip(args):
    x_shape, x, l, m, dtype_name, y_shape = args

    generated_data["shape_size_input_x"].append(len(x_shape))
    generated_data["size_input_axis"].append(x_shape)
    generated_data["l_tensor"].append(l)
    generated_data["m_tensor"].append(m)

    y = run_onnx_clip(x_shape, x, l, m, dtype_name, y_shape, inputs_attributes["ONNXRuntime_Provider"])
    check_constraints(x, l, m, y)


def teardown_module():
    """
    Function to write generated data to a json file
    """
    data = {
        "title": "Data generated for testing ONNX Clip Operator",
        "min_shape_size_input_x": inputs_attributes["min_shape_size_input_x"],
        "max_shape_size_input_x": inputs_attributes["max_shape_size_input_x"],
        "shape_size_input_x": generated_data["shape_size_input_x"],
        "min_size_input_axis": inputs_attributes["min_size_input_axis"],
        "max_size_input_axis": inputs_attributes["max_size_input_axis"],
        "size_input_axis": generated_data["size_input_axis"],
        "l_tensor": generated_data["l_tensor"],
        "m_tensor": generated_data["m_tensor"]
    }

    with open("generated_data.json", "w", encoding="utf-8") as f:
        # Process data before writing to file
        data["l_tensor"] = [(arr.tolist(), str(arr.dtype)) for arr in generated_data["l_tensor"]]
        data["m_tensor"] = [(arr.tolist(), str(arr.dtype)) for arr in generated_data["m_tensor"]]
        json.dump(data, f, indent=4)


def run_onnx_clip(x_shape, x, l, m, dtype_name, y_shape, provider):
    """
    Function that runs the ONNX Clip operation
    """

    # Create inputs
    x_onnx = helper.make_tensor_value_info('x',
                                      helper.np_dtype_to_tensor_dtype(x.dtype),
                                      list(x_shape))
    l_onnx = helper.make_tensor_value_info('l',
                                      helper.np_dtype_to_tensor_dtype(l.dtype),
                                      [])
    m_onnx = helper.make_tensor_value_info('m',
                                      helper.np_dtype_to_tensor_dtype(m.dtype),
                                      [])

    node_def = helper.make_node(
        'Clip',
        ['x', 'l', 'm'],
        ['y']
    )

    # Create the graph
    graph_def = helper.make_graph(
        [node_def],
        'test-clip',
        [x_onnx, l_onnx, m_onnx],
        [helper.make_tensor_value_info('y',
                                       helper.np_dtype_to_tensor_dtype(x.dtype),
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

    y = sess.run(None, {'x': x, 'l': l, 'm': m})[0]

    for tensor in [x, l, m]:
        print("x shape:", tensor.shape)
        print("x values:", tensor)

    print("y shape:", y.shape)
    print("y values:", y)
    print("y data type:", y.dtype)
    return y

def check_constraints(x, l, m, y):
    """
    Function that defines asserts for the constraints
    """

    # Inputs Constraints
    # X [C1] - Shape consistency
    # Y [C1] -> X [C1]
    assert x.shape == y.shape

    #X [C2] - Type consistency
    # L [C1] -> X [C2]
    # M [C1] -> X [C2]
    # Y [C3] -> X [C2]
    assert x.dtype == y.dtype == l.dtype == m.dtype

    # Output Constraints
    # Y [C2]
    if l <= m:
        for value in np.nditer(y):
            assert l <= value <= m
    else:
        np.all(y == m)
