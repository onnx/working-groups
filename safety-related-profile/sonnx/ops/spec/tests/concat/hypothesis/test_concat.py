"""
This file uses the Hypothesis library to generate a wide range of test cases
for the Concat operation in ONNX.
"""
import os

import json
import numpy as np
import ml_dtypes

from hypothesis import given, settings
import hypothesis.extra.numpy as hnp
from hypothesis import strategies as st

from onnx import helper
import onnx.checker
from onnxruntime import InferenceSession

from onnx import helper
import onnx.reference

import tensorflow as tf

if os.path.exists("generated_data.json"):
    os.remove("generated_data.json")

"""
Inputs/attributes details
"""
inputs_attributes = {
    "min_input_tensors": 1, # Input [C1]
    "max_input_tensors": 10, # Change as needed. Max is 2^31 -1
    "min_shape_size_input": 1, # Input [C3]
    "max_shape_size_input": 10, # Change as needed. Max is 2^31 -1
    "min_concatenation_axis": 0, # Axis [C1]
    "min_dim_for_concatenation_axis": 0, # Change as needed
    "max_dim_for_concatenation_axis": 10, # Change as needed
    "min_dim_for_other_axes": 0, #Change as needed
    "max_dim_for_other_axes": 10 # Change as needed
}

"""
Concat supported types
"""
# TODO we try to convert, but ONNXruntime does not run. ONNXruntime supports bfloat16?
# ONNX concat reference implementation supports bfloat16.

concat_types = {
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
    "BOOL": np.bool,
    "BFLOAT16": ml_dtypes.bfloat16
}

"""
Store generated data
"""
generated_data = {
    "number_of_input_tensors" : [],
    "shape_size_input" : [],
    "concatenation_axis" : [],
    "max_concatenation_axis" : [],
    "input_tensors_shapes" : []
}

"""
Function to generate valid concatenation arguments
"""
@st.composite
def valid_concat_args(draw):
    # Input [C1]
    number_of_input_tensors = draw(st.integers(
        min_value=inputs_attributes["min_input_tensors"],
        max_value=inputs_attributes["max_input_tensors"]))

    # Input [C3]
    shape_size_input_tensors = draw(st.integers(
        min_value=inputs_attributes["min_shape_size_input"],
        max_value=inputs_attributes["max_shape_size_input"]))
    max_concatenation_axis = shape_size_input_tensors - 1
    generated_data["max_concatenation_axis"].append(max_concatenation_axis)

    # Axis [C1]
    concatenation_axis = draw(st.integers(
        min_value=inputs_attributes["min_concatenation_axis"],
        max_value=max_concatenation_axis))

    # Input [C2]
    dim_for_other_axis = {}
    for i in range(shape_size_input_tensors):
        if i != concatenation_axis:
            dim_for_other_axis[i] = draw(st.integers(
                min_value=inputs_attributes["min_dim_for_other_axes"],
                max_value=inputs_attributes["max_dim_for_other_axes"]))

    # Generate shapes for input tensors
    input_tensors_shapes = []
    for _ in range(number_of_input_tensors):
        shape = []
        for j in range(shape_size_input_tensors):
            if j != concatenation_axis:
                dim_size = dim_for_other_axis[j]
            else:
                dim_size = draw(st.integers(
                    min_value=inputs_attributes["min_dim_for_concatenation_axis"],
                    max_value=inputs_attributes["max_dim_for_concatenation_axis"]))
            shape.append(dim_size)
        input_tensors_shapes.append(shape)

    # Generate input tensors
    dtype_name = draw(st.sampled_from(list(concat_types.keys())))
    dtype = concat_types[dtype_name]

    if np.issubdtype(dtype, np.integer):
        min_val = np.iinfo(dtype).min
        max_val = np.iinfo(dtype).max
        elements_strategy = st.integers(min_value=min_val, max_value=max_val)
    elif np.issubdtype(dtype, np.floating):
        min_val = np.finfo(dtype).min
        max_val = np.finfo(dtype).max
        elements_strategy = st.floats(min_value=min_val, max_value=max_val)
    elif np.issubdtype(dtype, np.bool_):
        elements_strategy = st.booleans()
    elif np.issubdtype(dtype, np.str_):
        elements_strategy = st.text(
            alphabet=st.characters(codec="utf-8", blacklist_characters='\x00')
        )
    elif dtype_name == "BFLOAT16":
        min_bfloat16 = float(ml_dtypes.finfo(concat_types["BFLOAT16"]).min)
        max_bfloat16 = float(ml_dtypes.finfo(concat_types["BFLOAT16"]).max)
        elements_strategy = st.floats(min_value=min_bfloat16, max_value=max_bfloat16)


    tensors = []
    for shape in input_tensors_shapes:
        if dtype_name == "BFLOAT16":
            temp_tensor = draw(hnp.arrays(dtype=np.float32, shape=shape, elements=elements_strategy))
            tf_tensor = tf.cast(tf.constant(temp_tensor), tf.bfloat16)
            tensor = tf_tensor.numpy()
            tensors.append(tensor)
        else:
            tensor = draw(hnp.arrays(dtype=dtype, shape=shape, elements=elements_strategy))
            tensors.append(tensor)


    y_concatenation_axis = 0
    for shape in input_tensors_shapes:
        y_concatenation_axis += shape[concatenation_axis]

    y_shape = []

    # Output [C1]
    for i in range(shape_size_input_tensors):
        if i != concatenation_axis:
            y_shape.append(input_tensors_shapes[0][i])
        else:
            y_shape.append(y_concatenation_axis)

    return input_tensors_shapes,tensors, concatenation_axis, y_shape, number_of_input_tensors, shape_size_input_tensors, dtype_name

"""
Function that runs the test
"""
@settings(max_examples=1000, deadline=None)
@given(valid_concat_args())
def test_concat(args):
    input_tensors_shapes, tensors, concatenation_axis, y_shape, number_of_input_tensors, shape_size_input_tensors, dtype_name = args

    generated_data["number_of_input_tensors"].append(number_of_input_tensors)
    generated_data["shape_size_input"].append(shape_size_input_tensors)
    generated_data["concatenation_axis"].append(concatenation_axis)
    generated_data["input_tensors_shapes"].append(input_tensors_shapes)

    run_onnx_concat(input_tensors_shapes, tensors, concatenation_axis, y_shape, dtype_name)
    check_constraints(len(tensors), input_tensors_shapes,
                       concatenation_axis, y_shape)


def teardown_module():
    """
    Function to write generated data to a json file
    """
    dados = {
        "titulo": "Dados gerados pelo Hypothesis",
        "min_input_tensors": inputs_attributes["min_input_tensors"],
        "max_input_tensors": inputs_attributes["max_input_tensors"],
        "number_of_input_tensors": generated_data["number_of_input_tensors"],
        "min_shape_size_input": inputs_attributes["min_shape_size_input"],
        "max_shape_size_input": inputs_attributes["max_shape_size_input"],
        "shape_size_input": generated_data["shape_size_input"],
        "min_concatenation_axis": inputs_attributes["min_concatenation_axis"],
        "max_concatenation_axis": generated_data["max_concatenation_axis"],
        "min_dim_for_concatenation_axis": inputs_attributes["min_dim_for_concatenation_axis"],
        "max_dim_for_concatenation_axis": inputs_attributes["max_dim_for_concatenation_axis"],
        "concatenation_axis": generated_data["concatenation_axis"],
        "min_dim_for_other_axes": inputs_attributes["min_dim_for_other_axes"],
        "max_dim_for_other_axes": inputs_attributes["max_dim_for_other_axes"],
        "input_tensors_shapes": generated_data["input_tensors_shapes"]
    }

    with open("generated_data.json", "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4)


def run_onnx_concat(input_tensors_shapes, tensors, concatenation_axis, y_shape, dtype_name):
    """
    Function that runs the ONNX Concat operation
    """
    input_tensor_infos = []
    input_names = []

    # Create inputs
    for i, shape in enumerate(input_tensors_shapes):
        input_name = f'input_{i}'
        input_names.append(input_name)

        tensor_info = helper.make_tensor_value_info(
            input_name,
            helper.np_dtype_to_tensor_dtype(tensors[i].dtype),
            shape
        )
        input_tensor_infos.append(tensor_info)

    # Create a node (Concat) with inputs/outputs
    node_def = helper.make_node(
        'Concat',
        input_names,
        ['y'],
        axis=concatenation_axis
    )

    # Create the graph
    graph_def = helper.make_graph(
        [node_def],
        'test-concat',
        input_tensor_infos,
        [helper.make_tensor_value_info('y',
                                       helper.np_dtype_to_tensor_dtype(tensors[0].dtype),
                                       y_shape)],
    )

    onnx_model = helper.make_model(graph_def)

    #Let's freeze the opset.
    del onnx_model.opset_import[:]
    opset = onnx_model.opset_import.add()
    opset.domain = ''
    opset.version = 15
    onnx_model.ir_version = 8

    # Verify the model
    onnx.checker.check_model(onnx_model)

    # Do inference
    if dtype_name == "BFLOAT16":
        # Usar ONNX Reference Implementation
        sess = onnx.reference.ReferenceEvaluator(onnx_model)
    else:
        sess = InferenceSession(onnx_model.SerializeToString(),
                                providers=["CPUExecutionProvider"])

    input_dic = {}
    for i, tensor in enumerate(tensors):
        input_name = f'input_{i}'
        input_dic[input_name] = tensor


    y = sess.run(None, input_dic)[0]

    for x in tensors:
        print("x shape:", x.shape)
        print("x values:", x)

    print("Concatenation axis:", concatenation_axis)
    print("y shape:", y.shape)
    print("y values:", y)
    print("y data type:", y.dtype)


def check_constraints(number_of_input_tensors,
                      input_tensors_shapes, concatenation_axis, y_shape):

    """
    Function that defines asserts for the constraints
    """

    # Inputs Constraints
    # [C1] - Input tensors range
    assert ( number_of_input_tensors >= inputs_attributes["min_input_tensors"]
            and number_of_input_tensors <= inputs_attributes["max_input_tensors"])

    # [C2] - Shape Consistency
    assert all(x[j] == input_tensors_shapes[0][j] for x in input_tensors_shapes
               for j in range(len(x)) if j != concatenation_axis)

    # [C3] - Shape size range
    assert all(len(i) >= inputs_attributes["min_shape_size_input"]
               and len(i) <= inputs_attributes["max_shape_size_input"] for i in input_tensors_shapes)

    # Attributes Constraints
    # [C1] - Concatenation axis range
    assert ( concatenation_axis >= inputs_attributes["min_concatenation_axis"]
            and concatenation_axis <= len(input_tensors_shapes[0]) - 1)

    # Outputs Constraints
    # [C1] - Output concatenation axis dimension
    assert ( y_shape[concatenation_axis] == sum(input_tensors_shapes[i][concatenation_axis]
                                                for i in range(len(input_tensors_shapes))))
    # [C1] - Other axis dimension
    assert ( y_shape[x] == input_tensors_shapes[0][x] for x in range(len(y_shape))
            if x != concatenation_axis)
