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
    "min_shape_size_input_x": 1,
    "max_shape_size_input_x": 4,
    "min_size_input_axis": 1,
    "max_size_input_axis": 10
}

"""
Clip supported types
"""
# TODO we try to convert, but ONNXruntime does not run. ONNXruntime supports bfloat16?
# ONNX clip reference implementation supports bfloat16.

clip_types = {
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
    "FP64": np.float64,
    "BFLOAT16": ml_dtypes.bfloat16
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

    # Generate input tensor shape
    shape_size_input_tensor_x = draw(st.integers(
        min_value=inputs_attributes["min_shape_size_input_x"],
        max_value=inputs_attributes["max_shape_size_input_x"]))

    x_shape = []
    # Generate each dimension of the input tensor shape
    for _ in range(shape_size_input_tensor_x):
        dim = draw(st.integers(
            min_value=inputs_attributes["min_size_input_axis"],
            max_value=inputs_attributes["max_size_input_axis"]))
        x_shape.append(dim)

    # Generate type of inputs tensors
    dtype_name = draw(st.sampled_from(list(clip_types.keys())))
    dtype = clip_types[dtype_name]

    if np.issubdtype(dtype, np.integer):
        min_value = np.iinfo(dtype).min
        max_value = np.iinfo(dtype).max
        elements_strategy = st.integers(min_value=min_value, max_value=max_value)
    elif np.issubdtype(dtype, np.floating):
        min_value = np.finfo(dtype).min
        max_value = np.finfo(dtype).max
        elements_strategy = st.floats(min_value=min_value, max_value=max_value)
    elif dtype == ml_dtypes.bfloat16:
        min_value = float(ml_dtypes.finfo(clip_types["BFLOAT16"]).min)
        max_value = float(ml_dtypes.finfo(clip_types["BFLOAT16"]).max)
        elements_strategy = st.floats(min_value=min_value, max_value=max_value)

    # Create inputs tensors
    if dtype_name == "BFLOAT16":
        # X [C2]
        temp_tensor = draw(hnp.arrays(dtype=np.float32, shape=x_shape, elements=elements_strategy))
        tf_tensor = tf.cast(tf.constant(temp_tensor), tf.bfloat16)
        x = tf_tensor.numpy()
        # L [C1] -> X [C2]
        temp_tensor = draw(hnp.arrays(dtype=np.float32, shape=(), elements=elements_strategy))
        tf_tensor = tf.cast(tf.constant(temp_tensor), tf.bfloat16)
        l = tf_tensor.numpy()
        # M [C1] -> X [C2]
        temp_tensor = draw(hnp.arrays(dtype=np.float32, shape=(), elements=elements_strategy))
        tf_tensor = tf.cast(tf.constant(temp_tensor), tf.bfloat16)
        m = tf_tensor.numpy()
    else:
        # X [C2]
        x = draw(hnp.arrays(dtype=dtype, shape=x_shape, elements=elements_strategy))
        # L [C1] -> X [C2]
        l = draw(hnp.arrays(dtype=dtype, shape=[], elements=elements_strategy))
        # M [C1] -> X [C2]
        m = draw(hnp.arrays(dtype=dtype, shape=[], elements=elements_strategy))

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

    y = run_onnx_clip(x_shape, x, l, m, dtype_name, y_shape)
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


def run_onnx_clip(x_shape, x, l, m, dtype_name, y_shape):
    """
    Function that runs the ONNX Concat operation
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
    #TODO WE NEED TO REVIEW THIS!
    if dtype_name in ["INT8", "INT16", "INT64", "UINT8", "UINT16", "BFLOAT16"]:
        # ! Using ONNX Reference Implementation -  ONNX Runtime does not give the right result
        sess = onnx.reference.ReferenceEvaluator(onnx_model)
    else:
        sess = InferenceSession(onnx_model.SerializeToString(),
                                providers=["CPUExecutionProvider"])

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
