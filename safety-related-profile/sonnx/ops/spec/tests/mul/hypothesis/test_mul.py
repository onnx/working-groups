"""
This file uses the Hypothesis library to generate a wide range of test cases
for the Mul operation in ONNX.
"""
import os
import json
import numpy as np
try:
    import ml_dtypes # kept for consistency with test_clip.py, NOT REALLY USED.
except ImportError:
    ml_dtypes = None

from onnx import helper
import onnx.checker
from onnxruntime import InferenceSession
import onnx.reference 

try:
    import tensorflow as tf # kept for consistency with test_clip.py, NOT REALLY USED.
except ModuleNotFoundError:
    tf = None  

from hypothesis import given, settings, assume
import hypothesis.extra.numpy as hnp
from hypothesis import strategies as st


"""
Clean previous generated data
"""
if os.path.exists("generated_data.json"):
    os.remove("generated_data.json")


"""
Inputs/attributes details
"""
inputs_attributes = {
    "min_shape_size_input": 0,   # number of dimensions (rank)
    "max_shape_size_input": 4,   # number of dimensions (rank)
    "min_size_input_axis": 1,    # no zero dimension
    "max_size_input_axis": 10,
    "ONNXRuntime_Provider": "CPUExecutionProvider"  # CPUExecutionProvider, CUDAExecutionProvider, DmlExecutionProvider
}


"""
Mul supported types (adapt if it restricts Mul differently)
"""
mul_types = {
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
Store/log generated data
"""
generated_data = {
    "shape_size_input_a": [],
    "shape_size_input_b": [],
    "shape_input_a": [],
    "shape_input_b": [],
    "a_tensor": [],
    "b_tensor": []
}


"""
Helper: build a broadcast-compatible pair of shapes
We generate a "result shape" then derive a_shape and b_shape from it.
"""
def _make_broadcastable_shapes(draw):
    # result rank
    y_rank = draw(st.integers(
        min_value=inputs_attributes["min_shape_size_input"],
        max_value=inputs_attributes["max_shape_size_input"]
    ))

    # result shape (each dim >= 1)
    y_shape = []
    for _ in range(y_rank):
        d = draw(st.integers(
            min_value=inputs_attributes["min_size_input_axis"],
            max_value=inputs_attributes["max_size_input_axis"]
        ))
        y_shape.append(d)

    # choose ranks for a and b (<= y_rank)
    a_rank = draw(st.integers(min_value=0, max_value=y_rank))
    b_rank = draw(st.integers(min_value=0, max_value=y_rank))

    # align right --> pick the last a_rank/b_rank dims from y_shape
    y_tail_for_a = y_shape[-a_rank:] if a_rank > 0 else []
    y_tail_for_b = y_shape[-b_rank:] if b_rank > 0 else []

    # for each dim in the tail, choose either 1 or the corresponding y dim
    a_shape = []
    for d in y_tail_for_a:
        a_shape.append(draw(st.sampled_from([1, d])))

    b_shape = []
    for d in y_tail_for_b:
        b_shape.append(draw(st.sampled_from([1, d])))

    # Ensure broadcast is valid (sanity check with numpy)
    a_dummy = np.empty(a_shape, dtype=np.float32)
    b_dummy = np.empty(b_shape, dtype=np.float32)
    broadcasted_shape = np.broadcast(a_dummy, b_dummy).shape  # must not throw

    return list(a_shape), list(b_shape), list(broadcasted_shape)


"""
Function to generate valid Mul arguments
"""

@st.composite
def valid_mul_args(draw):
    # Restrictions : type consistency
    all_valid_types = list(mul_types.get(inputs_attributes["ONNXRuntime_Provider"]).keys())
    dtype_name = draw(st.sampled_from(all_valid_types))
    dtype = mul_types[inputs_attributes["ONNXRuntime_Provider"]][dtype_name]

    # Choose numeric elements strategy
    if np.issubdtype(dtype, np.integer):
        # Keep values moderate to avoid "too wild" overflows in some backends.
        # (Still valid for Mul semantics; adjust if you want full range.)
        info = np.iinfo(dtype)
        lo = max(info.min, -10_000) if np.issubdtype(dtype, np.signedinteger) else 0
        hi = min(info.max, 10_000)
        a_numeric = st.integers(min_value=lo, max_value=hi)
    elif np.issubdtype(dtype, np.floating):
        # allow NaN and +/-Inf: MUST NOT set min_value/max_value in Hypothesis
        # width controls the kinds of floats generated
        width = 16 if dtype == np.float16 else 32 if dtype == np.float32 else 64
        a_numeric = st.floats(allow_nan=True, allow_infinity=True, width=width)
    else:
        # If your Mul supports other types, add them here
        assume(False)

    
    # Input shapes : broadcast-compatible
    a_shape, b_shape, y_shape = _make_broadcastable_shapes(draw)

    # Input tensors
    a = draw(hnp.arrays(dtype=dtype, shape=a_shape, elements=a_numeric))
    b = draw(hnp.arrays(dtype=dtype, shape=b_shape, elements=a_numeric))

    return (a_shape, b_shape, a, b, dtype_name, y_shape)


"""
Test function
"""
failed_cases = []
warning_cases = []  # Alertes mathématiques (Overflow, NaN)

@settings(max_examples=2000, deadline=None)
@given(valid_mul_args())
def test_mul(args):
    a_shape, b_shape, a, b, dtype_name, y_shape = args
    
    # On demande à NumPy de lever une erreur pour les overflows et les calculs invalides
    with np.errstate(over='raise', invalid='raise'):
        try:
            # 1. Calcul ONNX
            y = run_onnx_mul(a_shape, b_shape, a, b, dtype_name, y_shape, inputs_attributes["ONNXRuntime_Provider"])
            
            # 2. Vérification (Ici les warnings NumPy seront levés)
            check_constraints(a, b, y)
            
        except (FloatingPointError, RuntimeWarning) as w:
            # CAS DES WARNINGS (Overflow / Invalid)
            # On enregistre 
            if len(warning_cases) < 500:
                warning_cases.append({
                    "type": "Warning Mathématique",
                    "detail": str(w),
                    "dtype": dtype_name,
                    "tensor_a": a.tolist(),
                    "tensor_b": b.tolist()
                })
        
        except AssertionError as e:
            # CAS DES ERREURS (ONNX donne un mauvais résultat)
            failed_cases.append({
                "type": "Erreur d'Assertion",
                "detail": str(e),
                "dtype": dtype_name,
                "shape_a": a_shape,
                "shape_b": b_shape,
                "tensor_a": a.tolist(),
                "tensor_b": b.tolist()
            })
            raise e 


def teardown_module():
    # --- Fichier 1 : Les erreurs réelles ---
    if failed_cases:
        with open("failures_report.json", "w", encoding="utf-8") as f:
            json.dump({"total_errors": len(failed_cases), "errors": failed_cases}, f, indent=4)
        print(f"\n[!!!] {len(failed_cases)} ERREURS enregistrées dans failures_report.json")

    # --- Fichier 2 : Les warnings mathématiques ---
    if warning_cases:
        with open("warnings_report.json", "w", encoding="utf-8") as f:
            json.dump({"total_warnings": len(warning_cases), "warnings": warning_cases}, f, indent=4)
        print(f"\n[i] {len(warning_cases)} WARNINGS enregistrés dans warnings_report.json")

"""
Function that runs the ONNX Mul operation
"""
def run_onnx_mul(a_shape, b_shape, a, b, dtype_name, y_shape, provider):
    # Create inputs
    a_onnx = helper.make_tensor_value_info(
        'a',
        helper.np_dtype_to_tensor_dtype(a.dtype),
        list(a_shape)
    )
    b_onnx = helper.make_tensor_value_info(
        'b',
        helper.np_dtype_to_tensor_dtype(b.dtype),
        list(b_shape)
    )

    node_def = helper.make_node(
        'Mul',
        ['a', 'b'],
        ['y']
    )

    # Create the graph
    graph_def = helper.make_graph(
        [node_def],
        'test-mul',
        [a_onnx, b_onnx],
        [helper.make_tensor_value_info(
            'y',
            helper.np_dtype_to_tensor_dtype(a.dtype),
            list(y_shape)
        )],
    )

    onnx_model = helper.make_model(graph_def)

    # Let's freeze the opset.
    del onnx_model.opset_import[:]
    opset = onnx_model.opset_import.add()
    opset.domain = ''
    opset.version = 14
    onnx_model.ir_version = 10

    # Verify the model
    onnx.checker.check_model(onnx_model)

    # Do inference
    sess = InferenceSession(
        onnx_model.SerializeToString(),
        providers=[provider]
    )

    y = sess.run(None, {'a': a, 'b': b})[0]
    return y


def check_constraints(a, b, y):
    """
    Function that defines asserts for the constraints (Mul)
    """

    # Shape consistency: y must match numpy broadcasting
    expected_shape = np.broadcast(a, b).shape
    assert y.shape == expected_shape

    # Type consistency
    assert a.dtype == b.dtype == y.dtype

    # Value consistency: compare to numpy reference
    ref = np.multiply(a, b)

    if np.issubdtype(y.dtype, np.floating):
        # tolerate rounding differences especially for float16
        if y.dtype == np.float16:
            rtol, atol = 1e-2, 1e-2
        else:
            rtol, atol = 1e-5, 1e-6

        # equal_nan=True is required when we allow NaN generation
        np.testing.assert_allclose(y, ref, rtol=rtol, atol=atol, equal_nan=True)
    else:
        # integers: exact match (numpy uses wrap-around for fixed-width ints)
        assert np.array_equal(y, ref)