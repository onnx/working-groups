"""
This file uses the Hypothesis library to generate a wide range of test cases
for the Slice operation in ONNX.
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
Inputs/attributes details
"""

inputs_attributes = {
    "min_rank_input": 1, # Minimum rank of the input tensor should be at least 1 (no scalars slice) X [C3]
    "max_rank_input": 5, # Adjust as needed
    "min_dim_size_input": 1, # Dimension should always be positive (no zero dimensions)
    "max_dim_size_input": 10 # Adjust as needed
}

"""
Slice supported types
"""
slice_types = {
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
}


slice_index_types = {
    "INT32": np.int32,
    "INT64": np.int64,
}

"""
Store generated data
"""
generated_data = {
    "rank_input_tensor": [],
    "shape_input_tensor": [],
    "x_tensor": [],
    "a_tensor": [],
    "k_tensor": [],
    "s_tensor": [],
    "e_tensor": [],
    "x_type": [],
    "index_type": []
}

"""
Function to generate valid slice arguments
"""
@st.composite
@settings()
def valid_slice_args(draw):
    #---------------------------------------------------
    # Restrictions
    #---------------------------------------------------
    
    # X [C3] - Input/Output Types Consistency
    all_valid_types = list(slice_types.keys())
    input_type = draw(st.sampled_from(all_valid_types))
    input_dtype = slice_types[input_type]

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
        min_bfloat16 = float(ml_dtypes.finfo(slice_types["BFLOAT16"]).min)
        max_bfloat16 = float(ml_dtypes.finfo(slice_types["BFLOAT16"]).max)
        input_strategy = st.floats(min_value=min_bfloat16, max_value=max_bfloat16)

    # Index Types Consistency
    # S [C4] , E [C4] -> S [C4], A[C4] -> S [C4], K [C4] -> S [C4]
    all_valid_index_types = list(slice_index_types.keys())
    index_type = draw(st.sampled_from(all_valid_index_types))
    index_dtype = slice_index_types[index_type]

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
    # Input A
    #---------------------------------------------------
    # A [C1] -> X [C1]
    da0 = rank_input_tensor
    # A [C2], A [C3] 
    possible_indices = draw(st.permutations(range(rank_input_tensor)))[:da0]
    a = []
    for idx in possible_indices:
        make_negative = draw(st.booleans())
        if make_negative:
            a.append(idx - rank_input_tensor)
        else:
            a.append(idx)
    #A [C4]
    a = np.array(a, dtype=index_dtype)
    a_normalized = np.where(a < 0, a + rank_input_tensor, a)

    #---------------------------------------------------
    # Input K
    #---------------------------------------------------
    # K [C1] -> X [C1]
    dk0 = rank_input_tensor
    # K [C4]
    k = np.empty(dk0, dtype=index_dtype)
    # K [C2]
    k_strategy = st.one_of(
        st.integers(min_value=np.iinfo(index_dtype).min, max_value=-1),
        st.integers(min_value=1, max_value=np.iinfo(index_dtype).max)
    )
    for i in range(rank_input_tensor):
        k[i] = draw(k_strategy)

    #---------------------------------------------------
    # Input S
    #---------------------------------------------------
    # S [1] -> X [C1]
    ds0 = rank_input_tensor
    # S [C4]
    s = np.empty(ds0, dtype=index_dtype)
    # S [C2]
    for i in range(rank_input_tensor):  
        min_val = -shape_input_tensor[a_normalized[i]]
        max_val = shape_input_tensor[a_normalized[i]] - 1
        s_strategy = st.integers(min_value=min_val, max_value=max_val)
        s[i] = draw(s_strategy)
    s_normalized = np.empty(ds0, dtype=index_dtype)
    for i in range(len(s)):
        if s[i] < 0:
            s_normalized[i] = s[i] + shape_input_tensor[a_normalized[i]]
        else:
            s_normalized[i] = s[i]

    #---------------------------------------------------
    # Input E
    #---------------------------------------------------
    # E [1] -> X [C1]
    de0 = rank_input_tensor
    # E [C4]
    e = np.empty(de0, dtype=index_dtype)
    # E [C2]
    for i in range(rank_input_tensor):
        # E [C3] -> S [C3], K [C3] -> S [C3], S [C3]
        if k[i] > 0:
            min_val = s[i]
            max_val = shape_input_tensor[a_normalized[i]]
        else:
            min_val = -shape_input_tensor[a_normalized[i]] - 1
            max_val = s[i]
        s_strategy = st.integers(min_value=min_val, max_value=max_val)
        e[i] = draw(s_strategy)
    e_normalized = np.empty(de0, dtype=index_dtype)
    for i in range(len(e)):
        if e[i] < 0:
            e_normalized[i] = e[i] + shape_input_tensor[a_normalized[i]]
        else:
            e_normalized[i] = e[i]
    
    #---------------------------------------------------
    # Output Y
    #---------------------------------------------------
    # Y [C1] -> X [C1]
    output_shape = [0] * rank_input_tensor
    # Y [C2]
    for i in range(rank_input_tensor):
        space_i = e_normalized[i] - s_normalized[i]
        k_val = k[i]
        f = 0 if space_i % k_val == 0 else 1
        dY_i = (space_i // k_val) + f
        assume(dY_i > 0)
        output_shape[a_normalized[i]] = int(dY_i)
    return x, a, k, s, e, output_shape, s_normalized, a_normalized, e_normalized

"""
Function that runs the test
"""
@settings(max_examples=10000, deadline=None)
@given(valid_slice_args())
def test_slice(args):
    x, a, k, s, e, y_shape, s_normalized, a_normalized, e_normalized = args
    generated_data["rank_input_tensor"].append(len(x.shape))
    generated_data["shape_input_tensor"].append(list(x.shape))
    generated_data["x_tensor"].append(x.tolist())
    generated_data["a_tensor"].append(a.tolist())
    generated_data["k_tensor"].append(k)
    generated_data["s_tensor"].append(s.tolist())
    generated_data["e_tensor"].append(e.tolist())
    generated_data["x_type"].append(str(x.dtype))
    generated_data["index_type"].append(str(a.dtype))

    y = run_onnx_slice(x, a, k, s, e, y_shape)
    check_constraints(x, y, s_normalized, k, a_normalized, e_normalized, s, a, e, y_shape)

def teardown_module():
    """
    Function to write generated data to a json file
    """
    data = {
        "title": "Data generated by Hypothesis for Slice operation tests",
        "min_rank_input": inputs_attributes["min_rank_input"],
        "max_rank_input": inputs_attributes["max_rank_input"],
        "rank_input_tensor": generated_data["rank_input_tensor"],
        "min_dim_size_input": inputs_attributes["min_dim_size_input"],
        "max_dim_size_input": inputs_attributes["max_dim_size_input"],
        "shape_input_tensor": generated_data["shape_input_tensor"],
        "x_tensor": generated_data["x_tensor"],
        "a_tensor": generated_data["a_tensor"],
        "k_tensor": generated_data["k_tensor"],
        "s_tensor": generated_data["s_tensor"],
        "e_tensor": generated_data["e_tensor"],
        "x_type": generated_data["x_type"],
        "index_type": generated_data["index_type"]
    }

    with open("generated_data.json", "w", encoding="utf-8") as f:
        data["k_tensor"] = [(arr.tolist(), str(arr.dtype)) for arr in data["k_tensor"]]
        json.dump(data, f, indent=4)

def run_onnx_slice(x, a, k, s, e, y_shape):
    """
    Function that runs the ONNX Slice operation
    """
    x_onnx = helper.make_tensor_value_info('x', helper.np_dtype_to_tensor_dtype(x.dtype), x.shape)
    a_onnx = helper.make_tensor_value_info('a', helper.np_dtype_to_tensor_dtype(a.dtype), a.shape)
    k_onnx = helper.make_tensor_value_info('k', helper.np_dtype_to_tensor_dtype(k.dtype), k.shape)
    s_onnx = helper.make_tensor_value_info('s', helper.np_dtype_to_tensor_dtype(s.dtype), s.shape)
    e_onnx = helper.make_tensor_value_info('e', helper.np_dtype_to_tensor_dtype(e.dtype), e.shape)
    y_onnx = helper.make_tensor_value_info('y', helper.np_dtype_to_tensor_dtype(x.dtype), y_shape)

    node_def = helper.make_node(
        'Slice',
        inputs=['x', 's', 'e', 'a', 'k'],
        outputs=['y'],
    )

    # Create the graph
    graph_def = helper.make_graph(
        [node_def],
        'test-clip',
        [x_onnx, s_onnx, e_onnx, a_onnx, k_onnx],
        [y_onnx],
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

    if str(x.dtype) == "bfloat16":
        # Use ONNX Reference Implementation for bfloat16
        # BFLOAT16 is not supported by ONNX Runtime while using numpy
        # An alternative is to use torch tensores and CUDAProvider
        sess = onnx.reference.ReferenceEvaluator(onnx_model)
    else:
        # Use ONNX Runtime for other types
        sess = InferenceSession(onnx_model.SerializeToString(),
                               providers=["CPUExecutionProvider"])

    y = sess.run(None, {'x': x, 's': s, 'e': e, 'a': a, 'k': k})[0]
    print("y shape:", y.shape)
    print("y values:", y)
    print("y data type:", y.dtype)
    return y

def check_output_input(x, y, start, step, axis):
    indices = np.ndindex(y.shape)

    for out_idx in indices:
        real_index = []
        for dim in range(len(out_idx)):
            axis_index = axis.tolist().index(dim)
            real_index.append(axis[axis_index])
    
    for out_idx in indices:
        in_idx = tuple(start[real_index[dim]] + out_idx[dim] * step[real_index[dim]] for dim in range(len(out_idx)))
        if x[in_idx] != y[out_idx]:
            print(f"Mismatch at output index {out_idx}: expected {x[in_idx]}, got {y[out_idx]}")
            return False
    
    return True

def check_constraints(x, y, s_normalized, k, a_normalized, e_normalized, s, a, e, y_shape):
    """
    Check constraints for generated data
    """
    # X Constraints
    # X [C1], S [C1] -> X [C1], E [C1] -> X [C1], A [C1] -> X [C1], K [C1] -> X [C1]
    assert len(x.shape) == len(s_normalized) == len(k) == len(a_normalized) == len(e_normalized)
    # X [C2]
    assert len(x.shape) == len(y.shape)
    # X [C3]
    assert len(x.shape) >= 1
    # X [C4]
    if np.issubdtype(x.dtype, np.str_) or np.issubdtype(x.dtype, np.object_):
        assert np.issubdtype(y.dtype, np.str_) or np.issubdtype(y.dtype, np.object_)
    else:
        assert x.dtype == y.dtype

    # S Constraints
    # S [C2]
    for i in range(len(s)):
        assert -x.shape[a_normalized[i]] <= s[i] <= x.shape[a_normalized[i]] - 1
    # S [C3], E [C3] -> S [C3], K [C3] -> S [C3]
    for i in range(len(s_normalized)):
        if k[i] > 0:
            assert s_normalized[i] <= e_normalized[i] <= x.shape[a_normalized[i]]
        else:
            assert s_normalized[i] >= e_normalized[i]
    
    # S [C4], E [C4] -> S [C4], K [C4] -> S [C4], A [C4] -> S [C4]
    assert s.dtype == k.dtype == a.dtype == e.dtype

    # S Constraints
    # S [C2]
    for i in range(len(s)):
        if k[i] > 0:
            assert -x.shape[a_normalized[i]] <= s[i] <= x.shape[a_normalized[i]] 
        else:
            assert -x.shape[a_normalized[i]] - 1 <= s[i] <= x.shape[a_normalized[i]] - 1
    
    # A Constraints
    # A [C2]
    for i in range(len(a)):
        assert -len(x.shape) <= a[i] <= len(x.shape) - 1
    # A [C3]
    axis_unique = set()
    for i in range(len(a_normalized)):
        assert a_normalized[i] not in axis_unique
        axis_unique.add(a_normalized[i])
    
    # K Constraints
    # K [C2]
    for i in range(len(k)):
        assert k[i] != 0
    
    # Output Y Constraints
    # Y [C2]
    assert list(y.shape) == y_shape

    #Y [C3]
    assert  check_output_input(x, y, s_normalized, k, a_normalized)
