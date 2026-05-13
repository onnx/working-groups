"""
This file uses the Hypothesis library to generate a wide range of test cases
for the Range operation in ONNX.
"""
import os

import math
import json
import numpy as np

from onnx import helper
import onnx.checker
from onnxruntime import InferenceSession

from hypothesis import given, settings, assume
import hypothesis.extra.numpy as hnp
from hypothesis import strategies as st


if os.path.exists("generated_data.json"):
    os.remove("generated_data.json")

"""
Inputs/attributes for Range operation
"""
inputs_attributes = {
    "min_input_int": -1e6,      # Adjust as needed
    "max_input_int": 1e6,       # Adjust as needed
    "min_input_float": -1e7,    # Adjust as needed
    "max_input_float": 1e7,     # Adjust as needed
    "max_output_elements": 1e7, # Adjust as needed
    "ONNXRuntime_Provider": "CPUExecutionProvider" # available providers are CPUExecutionProvider, CUDAExecutionProvider, DmlExecutionProvider
}

"""
Store generated data
"""
generated_data = {
    "s_tensor": [],
    "l_tensor": [],
    "d_tensor": []
}

"""
Range supported types, organized by ONNXRuntime_Provider
"""
range_types = {
    "CPUExecutionProvider": {
        "INT16": np.int16, 
        "INT32": np.int32, 
        "INT64": np.int64,
        "FP32": np.float32, 
        "FP64": np.float64, 
    },
    "CUDAExecutionProvider": {
        "INT16": np.int16, 
        "INT32": np.int32, 
        "INT64": np.int64,
        "FP32": np.float32, 
        "FP64": np.float64, 
    },
    "DmlExecutionProvider": {
        "INT16": np.int16, 
        "INT32": np.int32, 
        "INT64": np.int64,
        "FP32": np.float32
    }
}

dtype_to_key = {v: k for k, v in range_types.get(inputs_attributes["ONNXRuntime_Provider"]).items()}

"""
Store generated data
"""
generated_data = {
    "input_type": [],
    "s_tensor": [],
    "l_tensor": [],
    "d_tensor": []
}

def calculate_y_shape(s, l, d):
    """
    Function to calculate the expected output shape of Range operation
    """
    return max(math.ceil((l - s) / d), 0)

"""
Function to generate valid range arguments
"""
@st.composite
@settings()
def valid_range_args(draw):
    #---------------------------------------------------
    # Restrictions
    #---------------------------------------------------

    # Input type consistency
    all_valid_types = list(range_types.get(inputs_attributes["ONNXRuntime_Provider"]).keys())
    input_type = draw(st.sampled_from(all_valid_types))
    input_dtype = range_types.get(inputs_attributes["ONNXRuntime_Provider"])[input_type]
    s_l_strategy = None
    d_strategy = None
    if np.issubdtype(input_dtype, np.integer):
        min_value = np.iinfo(input_dtype).min
        max_value = np.iinfo(input_dtype).max
        min_value = max(min_value, inputs_attributes["min_input_int"])
        max_value = min(max_value, inputs_attributes["max_input_int"])
        s_l_strategy = st.integers(min_value=min_value, max_value=max_value)

        # D [C1]
        d_strategy = st.one_of(
                        st.integers(min_value=min_value, max_value=-1),
                        st.integers(min_value=1, max_value=max_value)
                    )
    elif np.issubdtype(input_dtype, np.floating):
        min_value = np.finfo(input_dtype).min
        max_value = np.finfo(input_dtype).max
        min_value = max(min_value, inputs_attributes["min_input_float"])
        max_value = min(max_value, inputs_attributes["max_input_float"])
        s_l_strategy = st.floats(min_value= min_value, max_value=max_value)

        # D [C1]
        eps = np.finfo(input_dtype).eps
        d_strategy = st.one_of(
                        st.floats(min_value=min_value, max_value= -eps),
                        st.floats(min_value=eps, max_value=max_value)
                    )

    #---------------------------------------------------
    # Input S (Start)
    #---------------------------------------------------
    s = draw(hnp.arrays(dtype=input_dtype, shape=[], elements=s_l_strategy))

    #---------------------------------------------------
    # Input L (Limit)
    #---------------------------------------------------
    l = draw(hnp.arrays(dtype=input_dtype, shape=[], elements=s_l_strategy))

    #---------------------------------------------------
    # Input D (Delta)
    #---------------------------------------------------
    d = draw(hnp.arrays(dtype=input_dtype, shape=[], elements=d_strategy))

    y_shape = calculate_y_shape(s.item(), l.item(), d.item())

    # Ensures that the output shape does not overflow memory limits
    assume (y_shape <= inputs_attributes["max_output_elements"])

    return s, l, d, input_dtype, y_shape


"""
Function that runs the test
"""
@settings(max_examples=10000, deadline=None)
@given(valid_range_args())
def test_range(args):
    s, l, d,  input_dtype, y_shape = args
    generated_data["s_tensor"].append(s)
    generated_data["l_tensor"].append(l)
    generated_data["d_tensor"].append(d)
    input_type_key = dtype_to_key.get(input_dtype, str(input_dtype))
    generated_data["input_type"].append(input_type_key)
    y = run_onnx_range_test(s, l, d, inputs_attributes["ONNXRuntime_Provider"])
    check_constraints(d, y, y_shape)


def teardown_module():
    """
    Function to write generated data to a json file
    """
    s_tensor_int =  [s.tolist() for s, t in
                    zip(generated_data["s_tensor"], generated_data["input_type"])
                    if "INT" in t]
    s_tensor_float =[s.tolist() for s, t in
                    zip(generated_data["s_tensor"], generated_data["input_type"])
                    if "FP" in t]
    l_tensor_int =[l.tolist() for l, t in
                    zip(generated_data["l_tensor"], generated_data["input_type"])
                    if "INT" in t]
    l_tensor_float =[l.tolist() for l, t in
                    zip(generated_data["l_tensor"], generated_data["input_type"])
                    if "FP" in t]
    d_tensor_int =[d.tolist() for d, t in
                    zip(generated_data["d_tensor"], generated_data["input_type"])
                    if "INT" in t]
    d_tensor_float =[d.tolist() for d, t in
                    zip(generated_data["d_tensor"], generated_data["input_type"])
                    if "FP" in t]

    data = {
        "title": "Data generated for testing ONNX Range Operator",
        "min_input_int": inputs_attributes["min_input_int"],
        "max_input_int": inputs_attributes["max_input_int"],
        "min_input_float": inputs_attributes["min_input_float"],
        "max_input_float": inputs_attributes["max_input_float"],
        "s_tensor_int": s_tensor_int,
        "s_tensor_float": s_tensor_float,
        "l_tensor_int": l_tensor_int,
        "l_tensor_float": l_tensor_float,
        "d_tensor_int": d_tensor_int,
        "d_tensor_float": d_tensor_float,
        "input_type": generated_data["input_type"],
        "ONNXRuntime_Provider": inputs_attributes["ONNXRuntime_Provider"]
    }

    with open("generated_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def run_onnx_range_test(s, l, d, provider):
    """
    Function that runs the ONNX Range operation
    """
    s_onnx = helper.make_tensor_value_info('s', helper.np_dtype_to_tensor_dtype(s.dtype), [])
    l_onnx = helper.make_tensor_value_info('l', helper.np_dtype_to_tensor_dtype(l.dtype), [])
    d_onnx = helper.make_tensor_value_info('d', helper.np_dtype_to_tensor_dtype(d.dtype), [])

    # Dynamic output shape ([None]), because float operations can lead to imprecisions
    # Due to the roundings (on float datatypes) the y_dimensions calculation may not be exact
    # Thus, we set the output shape to None to avoid shape mismatch errors 
    y_onnx = helper.make_tensor_value_info('y', helper.np_dtype_to_tensor_dtype(s.dtype), [None])

    node_def = helper.make_node(
        'Range',
        inputs=['s', 'l', 'd'],
        outputs=['y']
    )

    # Create the graph
    graph_def = helper.make_graph(
        [node_def],
        'test_range',
        [s_onnx, l_onnx, d_onnx],
        [y_onnx],
    )

    onnx_model = helper.make_model(graph_def)

    #Let's freeze the opset.
    del onnx_model.opset_import[:]
    opset = onnx_model.opset_import.add()
    opset.domain = ''
    opset.version = 11
    onnx_model.ir_version = 10

    # Verify the model
    onnx.checker.check_model(onnx_model)

    sess = InferenceSession(onnx_model.SerializeToString(),
                               providers=[provider])

    y = sess.run(None, {'s': s, 'l': l, 'd': d})[0]
    print("y shape:", y.shape)
    print("y dtype:", y.dtype)
    print("y:", y)
    return y

def check_constraints(d, y, y_shape):
    # Cant check this assert because of numerical precision issues with floats
    # assert list (y.shape) == [y_shape]
    # Instead, we will say that the dimensions (expected/real) differ by at most 1
    assert abs(y.shape[0] - y_shape) <= 1
    # D [C1]
    assert d.item() != 0
