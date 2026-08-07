"""
This file uses the Hypothesis library to generate a wide range of test cases
for the Shape operation in ONNX.
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
Inputs/attributes for Shape operation
"""
inputs_attributes = {
    "min_rank_input": 0, #Adjust as needed
    "max_rank_input": 10, #Adjust as needed
    "min_dim_size_input": 0, #Adjust as needed
    "max_dim_size_input": 10, #Adjust as needed
    "start_min": -50, #Adjust as needed
    "start_max": 50, #Adjust as needed
    "end_min": -50, #Adjust as needed
    "end_max": 50, #Adjust as needed
    "ONNXRuntime_Provider": "CPUExecutionProvider" # available providers are CPUExecutionProvider, CUDAExecutionProvider, DmlExecutionProvider
}


"""
Shape supported types, organized by ONNXRuntime_Provider
"""
# We remove from CPUExecutionProvider the BFLOAT16 type. ONNXRutime does not support BFLOAT16 while using numpy.
# We tried to use the reference implementation from ONNX, but it was giving wrong results so we remove it.
shape_types = {
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
        "BOOL": np.bool_
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

dtype_to_key = {v: k for k, v in shape_types.get(inputs_attributes["ONNXRuntime_Provider"]).items()}

"""
Store generated data
"""
generated_data = {
    "rank_input_tensor": [],
    "shape_input_tensor": [],
    "x_type": [],
    "start": [],
    "end": []
}

def calculate_y (x_shape, start, end):
    """
    Function to calculate the expected output shape y
    """
    rank = len(x_shape)
    # Clamp start
    if start < 0:
        start += rank
    if start < 0:
        start = 0
    # Clamp end
    if end < 0:
        end += rank
    if end > rank:
        end = rank
    if start > end:
        return []
    else:
        return list(x_shape[start:end])

"""
Function to generate valid shape arguments
"""
@st.composite
@settings()
def valid_shape_args(draw):
    #---------------------------------------------------
    # Restrictions
    #---------------------------------------------------
    
    # Input type consistency
    all_valid_types = list(shape_types.get(inputs_attributes["ONNXRuntime_Provider"]).keys())
    input_type = draw(st.sampled_from(all_valid_types))
    input_dtype = shape_types.get(inputs_attributes["ONNXRuntime_Provider"])[input_type]

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
        min_bfloat16 = float(ml_dtypes.finfo(shape_types.get(inputs_attributes["ONNXRuntime_Provider"])["BFLOAT16"]).min)
        max_bfloat16 = float(ml_dtypes.finfo(shape_types.get(inputs_attributes["ONNXRuntime_Provider"])["BFLOAT16"]).max)
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
    # Attribute start
    #---------------------------------------------------

    start = draw(st.integers(
        min_value=inputs_attributes["start_min"],
        max_value=inputs_attributes["start_max"]
    ))

    #---------------------------------------------------
    # Attribute end
    #---------------------------------------------------

    end = draw(st.integers(
        min_value=inputs_attributes["end_min"],
        max_value=inputs_attributes["end_max"]
    ))

    #---------------------------------------------------
    # Output y 
    #---------------------------------------------------
    y_shape = [len(calculate_y(x.shape, start, end))]

    return x, start, end, y_shape


"""
Function that runs the test
"""
@settings(max_examples=10000, deadline=None)
@given(valid_shape_args())
def test_shape(args):
    x, start, end, y_shape = args
    generated_data["rank_input_tensor"].append(len(x.shape))
    generated_data["shape_input_tensor"].append(list(x.shape))
    x_type_key = dtype_to_key.get(x.dtype.type, str(x.dtype))
    generated_data["x_type"].append(x_type_key)
    generated_data["start"].append(start)
    generated_data["end"].append(end)
    y = run_onnx_shape_test(x, start, end, y_shape, inputs_attributes["ONNXRuntime_Provider"])
    check_constraints(x, start, end, y)


def teardown_module():
    """
    Function to write generated data to a json file
    """
    data = {
        "title": "Data generated by Hypothesis for Shape operation tests",
        "min_rank_input": inputs_attributes["min_rank_input"],
        "max_rank_input": inputs_attributes["max_rank_input"],
        "rank_input_tensor": generated_data["rank_input_tensor"],
        "min_dim_size_input": inputs_attributes["min_dim_size_input"],
        "max_dim_size_input": inputs_attributes["max_dim_size_input"],
        "shape_input_tensor": generated_data["shape_input_tensor"],
        "x_type": generated_data["x_type"],
        "start_min": inputs_attributes["start_min"],
        "start_max": inputs_attributes["start_max"],
        "start": generated_data["start"],
        "end_min": inputs_attributes["end_min"],
        "end_max": inputs_attributes["end_max"],
        "end": generated_data["end"],
        "ONNXRuntime_Provider": inputs_attributes["ONNXRuntime_Provider"]
    }


    with open("generated_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def run_onnx_shape_test(x, start, end, y_shape, provider):
    """
    Function that runs the ONNX Shape operation
    """
    x_onnx = helper.make_tensor_value_info('x', helper.np_dtype_to_tensor_dtype(x.dtype), x.shape)

    y_onnx = helper.make_tensor_value_info('y', onnx.TensorProto.INT64, y_shape)

    node_def = helper.make_node(
        'Shape',
        inputs=['x'],
        outputs=['y'],
        start=start,
        end=end
    )

    # Create the graph
    graph_def = helper.make_graph(
        [node_def],
        'test_shape',
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
    print("x.shape:", x.shape, "start:", start, "end:", end)
    print("x.type: ", x.dtype)
    print("y shape:", y.shape)
    print("y dtype:", y.dtype)
    print("y:", y)
    return y

def check_constraints(x, start, end, y):
    """
    Function that checks the constraints of the Shape operation
    """
    expected_y = calculate_y(x.shape, start, end)
    assert list(y) == expected_y, f"Output shape {list(y)} does not match expected shape {expected_y}, x shape: {x.shape}, start: {start}, end: {end}"