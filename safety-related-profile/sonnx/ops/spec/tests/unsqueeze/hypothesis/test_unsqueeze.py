"""
This file uses the Hypothesis library to generate a wide range of test cases
for the Unsqueeze operation in ONNX.
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
    "min_size_input_x_axis": 0, # Adjust as needed ( Minimum 0 )
    "max_size_input_x_axis": 10, # Adjust as needed
    "min_number_of_axes": 0, # Adjust as needed ( Minimum 0 )
    "max_number_of_axes": 4, # Adjust as needed
    "ONNXRuntime_Provider": "CPUExecutionProvider" # available providers are CPUExecutionProvider, CUDAExecutionProvider, DmlExecutionProvider
}

"""
Unsqueeze supported types
"""
unsqueeze_types = {
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
        "BFLOAT16": ml_dtypes.bfloat16,
        "BOOL": np.bool_,
        "STRING": np.str_
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


"""
Store generated data
"""
generated_data = {
    "shape_size_input_x" : [],
    "size_input_x": [],
    "size_input_axes": [],
    "x_type": []
}

dtype_to_key = {v: k for k, v in unsqueeze_types.get(inputs_attributes["ONNXRuntime_Provider"]).items()}

"""
Function to generate valid unsqueeze arguments
"""
@st.composite
def valid_unsqueeze_args(draw):
    #---------------------------------------------------
    # Restrictions
    #---------------------------------------------------
    # X [C1] - Type Consistency
    all_valid_types = list(unsqueeze_types.get(inputs_attributes["ONNXRuntime_Provider"]).keys())
    dtype_name = draw(st.sampled_from(all_valid_types))
    dtype = unsqueeze_types.get(inputs_attributes["ONNXRuntime_Provider"])[dtype_name]

    if np.issubdtype(dtype, np.integer):
        min_value = np.iinfo(dtype).min
        max_value = np.iinfo(dtype).max
        a_numeric = st.integers(min_value=min_value, max_value=max_value)
    elif np.issubdtype(dtype, np.floating):
        min_value = np.finfo(dtype).min
        max_value = np.finfo(dtype).max
        a_numeric = st.floats(min_value=min_value, max_value=max_value)
    elif np.issubdtype(dtype, np.bool_):
        a_numeric = st.booleans()
    elif np.issubdtype(dtype, np.str_):
        a_numeric = st.text(
            alphabet=st.characters(codec="utf-8", blacklist_characters='\x00')
        )
    elif dtype == ml_dtypes.bfloat16:
        min_value = float(ml_dtypes.finfo(unsqueeze_types.get(inputs_attributes["ONNXRuntime_Provider"])["BFLOAT16"]).min)
        max_value = float(ml_dtypes.finfo(unsqueeze_types.get(inputs_attributes["ONNXRuntime_Provider"])["BFLOAT16"]).max)
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
            min_value=inputs_attributes["min_size_input_x_axis"],
            max_value=inputs_attributes["max_size_input_x_axis"]))
        x_shape.append(dim)

    # Create input tensor X
    if dtype_name == "BFLOAT16":
        # X [C1]
        temp_tensor = draw(hnp.arrays(dtype=np.float32, shape=x_shape, elements=a_numeric))
        tf_tensor = tf.cast(tf.constant(temp_tensor), tf.bfloat16)
        x = tf_tensor.numpy()
    else:        
        # X [C1]
        x = draw(hnp.arrays(dtype=dtype, shape=x_shape, elements=a_numeric))
    
    #---------------------------------------------------
    # Input A
    #---------------------------------------------------

    # number_of_axes is the number of axes to unsqueeze
    number_of_axes = draw(st.integers(
        min_value=inputs_attributes["min_number_of_axes"],
        max_value=inputs_attributes["max_number_of_axes"]))
    
    # r is the rank of output tensor Y
    r = shape_size_input_x + number_of_axes
    # all_valid_axes is the list of all non negative axes to unsqueeze
    # A [C1], # A [C2]
    all_valid_axes = list(range(r))
    # axes is the list of axes to unsqueeze
    axes_values = draw(st.permutations(all_valid_axes))[:number_of_axes]
    
    # Create input tensor A
    a = []
    for a_val in axes_values:
        # Randomly decide to use negative or positive axis representation
        use_negative = draw(st.booleans())
        if use_negative:
            a.append(a_val - r)
        else:
            a.append(a_val)
    a = np.array(a, dtype=np.int64)
    a_normalized = np.where(a < 0, a + r, a)

    #---------------------------------------------------
    # Output Y
    #---------------------------------------------------
    
    # Y [C1]
    output_shape = list(x.shape)
    for axis in sorted(a_normalized):
        pos = axis if axis >= 0 else len(output_shape) + axis + 1
        output_shape.insert(pos, 1)
    
    return x, a, output_shape, dtype_name

"""
Function that runs the test
"""
@settings(max_examples=10000, deadline=None)
@given(valid_unsqueeze_args())
def test_slice(args):
    x, a, output_shape, dtype_name = args
    x_type_key = dtype_to_key.get(x.dtype.type, str(x.dtype))
    generated_data["x_type"].append(x_type_key)
    generated_data["shape_size_input_x"].append(len(x.shape))
    generated_data["size_input_x"].append(x.shape)
    generated_data["size_input_axes"].append(len(a))

    y = run_onnx_unsqueeze(x, a, output_shape, dtype_name)
    check_constraints(x, a, y, output_shape)

def teardown_module():
    """
    Function to write generated data to a json file
    """
    data = {
        "title": "Data generated for testing ONNX Unsqueeze Operator",
        "min_shape_size_input_x": inputs_attributes["min_shape_size_input_x"],
        "max_shape_size_input_x": inputs_attributes["max_shape_size_input_x"],
        "shape_size_input_x": generated_data["shape_size_input_x"],
        "min_size_input_x": inputs_attributes["min_size_input_x_axis"],
        "max_size_input_x": inputs_attributes["max_size_input_x_axis"],
        "size_input_x": generated_data["size_input_x"],
        "min_number_of_axes": inputs_attributes["min_number_of_axes"],
        "max_number_of_axes": inputs_attributes["max_number_of_axes"],
        "size_input_axes": generated_data["size_input_axes"],
        "ONNXRuntime_Provider": inputs_attributes["ONNXRuntime_Provider"],
        "x_type": generated_data["x_type"]
    }

    with open("generated_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def run_onnx_unsqueeze(x, a, output_shape, dtype_name):
    """
    Function that runs the ONNX Unsqueeze operation
    """

    # Create inputs
    x_onnx = helper.make_tensor_value_info('x',
                                      helper.np_dtype_to_tensor_dtype(x.dtype),
                                      x.shape)
    a_onnx = helper.make_tensor_value_info('a',
                                      helper.np_dtype_to_tensor_dtype(a.dtype),
                                      a.shape)

    node_def = helper.make_node(
        'Unsqueeze',
        ['x', 'a'],
        ['y']
    )

    # Create the graph
    graph_def = helper.make_graph(
        [node_def],
        'test-unsqueeze',
        [x_onnx, a_onnx],
        # Y [C2]
        [helper.make_tensor_value_info('y',
                                       helper.np_dtype_to_tensor_dtype(x.dtype),
                                       output_shape)],
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

    # Do inference
    if dtype_name in ["BFLOAT16"]:
        # Use ONNX Reference Implementation for bfloat16
        # BFLOAT16 is not supported by ONNX Runtime while using numpy
        # An alternative is to use torch tensores and CUDAProvider
        sess = onnx.reference.ReferenceEvaluator(onnx_model)
    else:
        # Use ONNX Runtime for other types
        sess = InferenceSession(onnx_model.SerializeToString(),
                                providers=["CPUExecutionProvider"])

    y = sess.run(None, {'x': x, 'a': a})[0]

    print("x shape:", x.shape)
    print("a values:", a)
    print("y shape:", y.shape)
    return y

def check_constraints(x, a,  y, output_shape):
    """
    Function that defines asserts for the constraints
    """

    # X[C1], Y[C2] -> X[C1]
    x_is_string = np.issubdtype(x.dtype, np.str_) or np.issubdtype(x.dtype, np.object_)
    y_is_string = np.issubdtype(y.dtype, np.str_) or np.issubdtype(y.dtype, np.object_)
    if x_is_string and y_is_string:
        pass
    else:
        assert x.dtype == y.dtype
    # A [C1]
    r = len(y.shape)
    assert np.all((a >= -r) & (a < r))
    # A [C2]
    a_normalized = (a + r) % r
    assert len(np.unique(a_normalized)) == len(a_normalized)
    # Y [C1]
    assert list(y.shape) == output_shape
    