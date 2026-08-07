"""
This file uses the Hypothesis library to generate a wide range of test cases
for the Reshape operation in ONNX.
"""
import os

import math
import json
import numpy as np

from hypothesis import given, settings
import hypothesis.extra.numpy as hnp
from hypothesis import strategies as st
from hypothesis import assume

from onnx import helper
import onnx.checker
from onnxruntime import InferenceSession


from onnx import helper

import tensorflow as tf

from sympy import divisors

from reshape import reshape

if os.path.exists("generated_data.json"):
    os.remove("generated_data.json")


"""
Inputs/attributes for Reshape operation
"""

inputs_attributes = {
    "min_rank_input": 1, #Adjust as needed
    "max_rank_input": 5, #Adjust as needed
    "min_dim_size_input": 1, #Adjust as needed
    "max_dim_size_input": 5, #Adjust as needed
    "ONNXRuntime_Provider": "CPUExecutionProvider" # available providers are CPUExecutionProvider, CUDAExecutionProvider, DmlExecutionProvider
}

"""
Reshape supported types, organized by ONNXRuntime_Provider
"""
reshape_types = {
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
        "BOOL": np.bool_
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

dtype_to_key = {v: k for k, v in reshape_types.get(inputs_attributes["ONNXRuntime_Provider"]).items()}

"""
Store generated data
"""
generated_data = {
    "rank_input_tensor_x": [],
    "shape_input_tensor_x": [],
    "rank_input_tensor_s": [],
    "shape_input_tensor_s": [],
    "input_type": []
}

        
def calculate_y_shape(allowzero, data_tensor_shape, shape_input_tensor):
    """
    Function to calculate expected output shape after Reshape operation
    """
    y_shape = []
    for i, dim in enumerate(data_tensor_shape):
        if allowzero == 0  and dim == 0 and i < len(shape_input_tensor):
            y_shape.append(int(shape_input_tensor[i]))
        elif dim == -1:
            prod_known_dims = 1
            for j, d in enumerate(data_tensor_shape):
                if j != i:
                    if d == 0 and j < len(shape_input_tensor) and allowzero == 0:
                        prod_known_dims *= shape_input_tensor[j]
                    else:
                        prod_known_dims *= d
            inferred_dim = int(np.prod(shape_input_tensor) // prod_known_dims)
            y_shape.append(inferred_dim)
        else:
            y_shape.append(int(dim))
    return y_shape



def valid_shape_values_allowzero_one(shape_input_tensor, num_shape_elements, draw):
    """
    Function to generate valid shape tensor values when allowzero is 1
    """
    data_tensor_shape = []
    total_shape = np.prod(shape_input_tensor)
    possible_dims = []
    for _ in range(num_shape_elements - 1):
        possible_dims = divisors(total_shape)
        if 0 in shape_input_tensor:
            possible_dims.append(0)
        dim = draw(st.sampled_from(possible_dims))
        data_tensor_shape.append(dim)
        if dim != 0:
            total_shape = total_shape // dim
    data_tensor_shape.append(total_shape)
    return data_tensor_shape


def valid_shape_values_allowzero_zero(shape_input_tensor, rank_input_tensor, num_shape_elements, draw):
    """
    Function to generate valid shape tensor values when allowzero is 0
    """
    data_tensor_shape = []
    total_shape = np.prod(shape_input_tensor)
    possible_dims = []
    for i in range(num_shape_elements - 1):
        # Allowzero [C2], S[C2]
        if i < rank_input_tensor and shape_input_tensor[i] in divisors(total_shape):
            possible_dims = divisors(total_shape) + [0]
        else:
            possible_dims = divisors(total_shape)
        dim = draw(st.sampled_from(possible_dims))  
        data_tensor_shape.append(dim)
        if dim != 0:
            total_shape = total_shape // dim
        if dim == 0 and i < len(shape_input_tensor):
            total_shape = total_shape // shape_input_tensor[i]
    data_tensor_shape.append(total_shape)
    return data_tensor_shape

"""
Function to generate valid reshape arguments
"""
@st.composite
@settings()
def valid_reshape_args(draw):
    #---------------------------------------------------
    # Restrictions
    #---------------------------------------------------
    
    #TODO Change contraints numbers
    # X [C2] - Input/Output Types Consistency
    all_valid_types = list(reshape_types.get(inputs_attributes["ONNXRuntime_Provider"]).keys())
    input_type = draw(st.sampled_from(all_valid_types))
    input_dtype = reshape_types.get(inputs_attributes["ONNXRuntime_Provider"])[input_type]

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
        
        x = draw(hnp.arrays(dtype=input_dtype, shape=shape_input_tensor, elements=input_strategy))

    #---------------------------------------------------
    # Attribute allowzero
    #---------------------------------------------------

    # Allowzero [C1]
    allowzero = draw(st.integers(
        min_value=0,
        max_value=1
    ))

    #---------------------------------------------------
    # Input S
    #---------------------------------------------------
    rank_tensor_shape = draw(st.integers(
        min_value=inputs_attributes["min_rank_input"],
        max_value=inputs_attributes["max_rank_input"]
    ))

    shape_tensor_shape = []
    for _ in range(rank_tensor_shape):
        dim_size = draw(st.integers(
            min_value=inputs_attributes["min_dim_size_input"],
            max_value=inputs_attributes["max_dim_size_input"]
        ))
        shape_tensor_shape.append(dim_size)

    # ONNX Runtime limit the total number of dimensions, on shape tensor, to 64
    assume(np.prod(shape_tensor_shape) <= 64)

    num_shape_elements = np.prod(shape_tensor_shape)
    
    if allowzero == 1:
        data_tensor_shape = valid_shape_values_allowzero_one(shape_input_tensor, num_shape_elements, draw)
    else:
        data_tensor_shape = valid_shape_values_allowzero_zero(shape_input_tensor, rank_input_tensor, num_shape_elements, draw)
    
    # Allowzero [C3], S [C1], S [C3]
    allow_infer = draw(st.booleans())
    if allow_infer and ((allowzero == 0  and 0 not in shape_input_tensor) or (allowzero == 1 and 0 not in data_tensor_shape)):
        infer_index = draw(st.integers(
            min_value=0,
            max_value=num_shape_elements - 1
        ))
        data_tensor_shape[infer_index] = -1
    
    shape_tensor = np.array(data_tensor_shape, dtype=np.int64)
    
    y_shape = calculate_y_shape(allowzero, data_tensor_shape, shape_input_tensor)

    return x, shape_tensor, y_shape, allowzero


@settings(max_examples=50000, deadline=None)
@given(valid_reshape_args())
def test_reshape(args):
    x, shape_tensor, y_shape, allowzero = args
    generated_data["rank_input_tensor_x"].append(len(x.shape))
    generated_data["shape_input_tensor_x"].append(list(x.shape))
    generated_data["rank_input_tensor_s"].append(len(shape_tensor.shape))
    generated_data["shape_input_tensor_s"].append(list(shape_tensor.shape))
    input_type_key = dtype_to_key.get(x.dtype.type, str(x.dtype))
    generated_data["input_type"].append(input_type_key)
    y = run_onnx_reshape_test(x, shape_tensor, y_shape, inputs_attributes["ONNXRuntime_Provider"])
    check_constraints(x, shape_tensor, allowzero, y, y_shape)


def teardown_module():
    """
    Function to write generated data to a json file
    """
    data = {
        "title": "Data generated by Hypothesis for Reshape operation tests",
        "min_rank_input": inputs_attributes["min_rank_input"],
        "max_rank_input": inputs_attributes["max_rank_input"],
        "rank_input_tensor_x": generated_data["rank_input_tensor_x"],
        "rank_input_tensor_s": generated_data["rank_input_tensor_s"],
        "min_dim_size_input": inputs_attributes["min_dim_size_input"],
        "max_dim_size_input": inputs_attributes["max_dim_size_input"],
        "shape_input_tensor_x": generated_data["shape_input_tensor_x"],
        "shape_input_tensor_s": generated_data["shape_input_tensor_s"],
        "input_type": generated_data["input_type"],
        "ONNXRuntime_Provider": inputs_attributes["ONNXRuntime_Provider"]
    }


    with open("generated_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def run_onnx_reshape_test(x, s, y_shape, provider):
    """
    Function that runs the ONNX Reshape operation
    """
    x_onnx = helper.make_tensor_value_info('x', helper.np_dtype_to_tensor_dtype(x.dtype), x.shape)
    s_onnx = helper.make_tensor_value_info('s', helper.np_dtype_to_tensor_dtype(s.dtype), s.shape)

    y_onnx = helper.make_tensor_value_info('y', helper.np_dtype_to_tensor_dtype(x.dtype), y_shape)

    node_def = helper.make_node(
        'Reshape',
        inputs=['x', 's'],
        outputs=['y']
    )

    # Create the graph
    graph_def = helper.make_graph(
        [node_def],
        'test_reshape',
        [x_onnx, s_onnx],
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

    sess = InferenceSession(onnx_model.SerializeToString(),
                            providers=[provider])

    y = sess.run(None, {'x': x, 's': s})[0]
    print("y shape:", y.shape)
    print("y dtype:", y.dtype)
    print("y:", y)
    return y


def clamp_s_tensor(x,s,allowzero):
    """
    Function to clamp shape tensor values to valid ones
    """
    clamped_s = []
    for i, dim in enumerate(s):
        if allowzero == 0 and dim == 0 and i < len(x.shape):
            clamped_s.append(x.shape[i])
        else:
            clamped_s.append(dim)
    x_prod = np.prod(x.shape)
    s_prod = np.prod([dim for dim in clamped_s if dim != -1])
    if -1 in clamped_s:
        inferred_dim = x_prod // s_prod
        clamped_s = [inferred_dim if dim == -1 else dim for dim in clamped_s]
    return clamped_s


def check_constraints(x, s, allowzero, y, y_shape):
    """
    Function to check constraints after Reshape operation
    """
    # Y[C1] - Shape consistency
    assert np.prod(x.shape) == np.prod(y.shape) == np.prod(clamp_s_tensor(x,s,allowzero))

    #Allowzero [C1]
    assert allowzero in [0,1]

    #Allowzero [C2]
    if allowzero == 0:
        for i, s_value in enumerate(s):
            if s_value == 0:
                assert i < len(x.shape)

    # Allowzero [C3]
    if allowzero == 0 and -1 in s:
        assert 0 not in x.shape

    if allowzero == 1:
        for s_value in s:
            assert s_value > 0 or (s_value == 0 and 0 in list(x.shape) and not -1 in s) or (s_value == -1 and 0 not in s)
    
    # S [C1]
    assert list(s).count(-1) <= 1

    expected_result = reshape(x,y)
    assert np.array_equal(y, expected_result)
