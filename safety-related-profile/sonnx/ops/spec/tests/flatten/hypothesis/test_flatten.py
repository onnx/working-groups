"""
This file uses the Hypothesis library to generate a wide range of test cases
for the Flatten operation in ONNX.
"""
import os

import json
import numpy as np
import ml_dtypes

from hypothesis import given, settings
import hypothesis.extra.numpy as hnp
from hypothesis import strategies as st
from hypothesis import assume

from onnx import helper
import onnx.checker
from onnxruntime import InferenceSession
import onnx.reference


from onnx import helper

import tensorflow as tf

if os.path.exists("generated_data.json"):
    os.remove("generated_data.json")


"""
Inputs/attributes for Flatten operation
"""

inputs_attributes = {
    "min_rank_input": 1, #Adjust as needed
    "max_rank_input": 10, #Adjust as needed
    "min_dim_size_input": 1, #Adjust as needed
    "max_dim_size_input": 5, #Adjust as needed
    "ONNXRuntime_Provider": "CPUExecutionProvider" # available providers are CPUExecutionProvider, CUDAExecutionProvider, DmlExecutionProvider
}


"""
Flatten supported types, organized by ONNXRuntime_Provider
"""
flatten_types = {
    "CPUExecutionProvider": {
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
        "STRING": np.str_,
        "BOOL": np.bool_,
        "BFLOAT16": ml_dtypes.bfloat16
    },
    "CUDAExecutionProvider": {
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
        "BOOL": np.bool_,
        "BFLOAT16": ml_dtypes.bfloat16
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
        "FP64": np.float64,
        "BOOL": np.bool_
    }
}

dtype_to_key = {v: k for k, v in flatten_types.get(inputs_attributes["ONNXRuntime_Provider"]).items()}

"""
Store generated data
"""
generated_data = {
    "rank_input_tensor": [],
    "shape_input_tensor": [],
    "x_type": [],
    "axis": []
}

"""
Function to generate valid flatten arguments
"""

@st.composite
@settings()
def valid_slice_args(draw):
    #---------------------------------------------------
    # Restrictions
    #---------------------------------------------------
    
    # X [C2] - Input/Output Types Consistency
    all_valid_types = list(flatten_types.get(inputs_attributes["ONNXRuntime_Provider"]).keys())
    input_type = draw(st.sampled_from(all_valid_types))
    input_dtype = flatten_types.get(inputs_attributes["ONNXRuntime_Provider"])[input_type]

    if np.issubdtype(input_dtype, np.integer):
        min_val = np.iinfo(input_dtype).min
        max_val = np.iinfo(input_dtype).max
        input_strategy = st.integers(min_value=min_val, max_value=max_val)
    elif np.issubdtype(input_dtype, np.floating):
        min_val = np.finfo(input_dtype).min
        max_val = np.finfo(input_dtype).max
        input_strategy = st.floats(min_value=min_val, max_value=max_val)
    elif np.issubdtype(input_dtype, np.bool_):
        input_strategy = st.booleans()
    elif np.issubdtype(input_dtype, np.str_):
        input_strategy = st.text(
            alphabet=st.characters(codec="utf-8", blacklist_characters='\x00')
        )
    elif input_type == "BFLOAT16":
        min_bfloat16 = float(ml_dtypes.finfo(flatten_types.get(inputs_attributes["ONNXRuntime_Provider"])["BFLOAT16"]).min)
        max_bfloat16 = float(ml_dtypes.finfo(flatten_types.get(inputs_attributes["ONNXRuntime_Provider"])["BFLOAT16"]).max)
        input_strategy = st.floats(min_value=min_bfloat16, max_value=max_bfloat16)

    #---------------------------------------------------
    # Input X
    #---------------------------------------------------
    rank_input_tensor = draw(st.integers(
        min_value=inputs_attributes["min_rank_input"],
        max_value=inputs_attributes["max_rank_input"]
    ))

    shape_input_tensor = []
    for _ in range(rank_input_tensor):
        dim_size = draw(st.integers(
            min_value=inputs_attributes["min_dim_size_input"],
            max_value=inputs_attributes["max_dim_size_input"]
        ))
        shape_input_tensor.append(dim_size)

    if input_type == "BFLOAT16":
        temp_tensor = draw(hnp.arrays(dtype=np.float32, shape=shape_input_tensor, elements=input_strategy))
        tf_tensor = tf.cast(tf.constant(temp_tensor), tf.bfloat16)
        x = tf_tensor.numpy()
    else:
        x = draw(hnp.arrays(dtype=input_dtype, shape=shape_input_tensor, elements=input_strategy))

    #---------------------------------------------------
    # Attribute axis
    #---------------------------------------------------

    # axis [C1] ->  X [C1], axis [C2] - Axis Range
    axis = draw(st.integers(
        min_value=-(rank_input_tensor),
        max_value=rank_input_tensor
    ))

    #---------------------------------------------------
    # Output y 
    #---------------------------------------------------
    
    # Y [C1]
    y_shape = []
    dy0 = np.prod(shape_input_tensor[:axis])
    dy1 = np.prod(shape_input_tensor[axis:])
    y_shape = [int(dy0), int(dy1)]

    return x, axis, y_shape

"""
Function that runs the test
"""
@settings(max_examples=10000, deadline=None)
@given(valid_slice_args())
def test_flatten(args):
    x, axis, y_shape = args
    generated_data["rank_input_tensor"].append(len(x.shape))
    generated_data["shape_input_tensor"].append(list(x.shape))
    x_type_key = dtype_to_key.get(x.dtype.type, str(x.dtype))
    generated_data["x_type"].append(x_type_key)
    generated_data["axis"].append(axis)
    y = run_onnx_flatten_test(x, axis, y_shape, inputs_attributes["ONNXRuntime_Provider"])
    if axis < 0:
        axis += len(x.shape)
    check_constraints(y_shape, y, x, axis)


def teardown_module():
    """
    Function to write generated data to a json file
    """
    data = {
        "title": "Data generated by Hypothesis for Flatten operation tests",
        "min_rank_input": inputs_attributes["min_rank_input"],
        "max_rank_input": inputs_attributes["max_rank_input"],
        "rank_input_tensor": generated_data["rank_input_tensor"],
        "min_dim_size_input": inputs_attributes["min_dim_size_input"],
        "max_dim_size_input": inputs_attributes["max_dim_size_input"],
        "shape_input_tensor": generated_data["shape_input_tensor"],
        "x_type": generated_data["x_type"],
        "axis": generated_data["axis"],
        "ONNXRuntime_Provider": inputs_attributes["ONNXRuntime_Provider"]
    }


    with open("generated_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def run_onnx_flatten_test(x, axis, y_shape, provider):
    """
    Function that runs the ONNX Slice operation
    """
    x_onnx = helper.make_tensor_value_info('x', helper.np_dtype_to_tensor_dtype(x.dtype), x.shape)

    # Y [C3] -> X [C2] - Input/Output Types Consistency
    y_onnx = helper.make_tensor_value_info('y', helper.np_dtype_to_tensor_dtype(x.dtype), y_shape)

    node_def = helper.make_node(
        'Flatten',
        inputs=['x'],
        outputs=['y'],
        axis=axis
    )

    # Create the graph
    graph_def = helper.make_graph(
        [node_def],
        'test_flatten',
        [x_onnx],
        [y_onnx],
    )

    onnx_model = helper.make_model(graph_def)

    #Let's freeze the opset.
    del onnx_model.opset_import[:]
    opset = onnx_model.opset_import.add()
    opset.domain = ''
    opset.version = 22
    onnx_model.ir_version = 10

    # Verify the model
    onnx.checker.check_model(onnx_model)

    if str(x.dtype) == "bfloat16":
        # Use ONNX Reference Implementation for bfloat16
        # BFLOAT16 is not supported by ONNX Runtime while using numpy
        # An alternative is to use torch tensores and CUDAProvider
        sess = onnx.reference.ReferenceEvaluator(onnx_model)
    else:
        # Use ONNX Runtime for other types
        sess = InferenceSession(onnx_model.SerializeToString(),
                               providers=[provider])
        
    y = sess.run(None, {'x': x})[0]
    print("y shape:", y.shape)
    print("y dtype:", y.dtype)
    print("y:", y)
    return y

def check_constraints(y_shape, y, x, axis):
    """
    Check constraints for generated data
    """
    # X[C1]
    assert axis <= len(x.shape)
    # X[C2]
    x_is_string = np.issubdtype(x.dtype, np.str_) or np.issubdtype(x.dtype, np.object_)
    y_is_string = np.issubdtype(y.dtype, np.str_) or np.issubdtype(y.dtype, np.object_)
    if x_is_string and y_is_string:
        pass
    else:
        assert x.dtype == y.dtype
    # axis[C1] -> X[C1]
    # axis[C2]
    assert -len(x.shape) <= axis <= len(x.shape)
    # Y
    assert (len (y_shape) == 2)
    # Y[C1]
    assert y_shape == list(y.shape)
    # Y[C2]
    assert check_coords_value(x, y, axis)
    # Y[C3] -> X[C2]



def calculate_y_coords(x_coords, x_shape, axis):
    """
    Calculate the corresponding coordinates in Y given coordinates in X
    """
    n = len(x_shape)
    a = 0
    for z in range(0, axis):
        prod = 1
        for k in range(z + 1, axis):
            prod *= x_shape[k]
        a += x_coords[z] * prod

    b = 0
    for z in range(axis, n):
        prod = 1
        for k in range(z + 1, n):
            prod *= x_shape[k]
        b += x_coords[z] * prod
    
    return (a, b)

def check_coords_value(x, y, axis):
    """
    Check if there is a valid correspondence between input and output values
    """
    result = []
    it = np.nditer(x, flags=['multi_index'])
    for x_value in it:
        coords = it.multi_index
        y_coords = calculate_y_coords(coords, list(x.shape), axis)
        y_value = y[y_coords]
        result.append(x_value == y_value)
    return all(result)