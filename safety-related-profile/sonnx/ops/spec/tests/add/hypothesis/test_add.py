"""
Using hypothesis to generate automatic tests for Add operator (SONNX)
"""
import math
import numpy as np

from hypothesis import given, settings
import hypothesis.extra.numpy as hnp
from hypothesis import strategies as st

from onnx import helper, TensorProto
import onnx.checker
import onnx.printer
from onnxruntime import InferenceSession


# Equivalence classes for tensor shapes: 
#   - Singular points and classes for ranks: r_scalar;r_min;]r_min,r_sufficient[;r_sufficient;]r_sufficient,r_max[;r_max. 
#     Let's set the values:
#      - r_scalar = 0
#      - r_min = 1
#      - r_sufficient = 4, which is very popular. So, do we need to consider a rank in ]1,4[? No.
#      - r_max = +inf; Not tractable
#      - Actual singular points and classes for ranks: r_scalar;r_min;]r_min,r_sufficient[;r_sufficient = 0;1;]1,4[;4
#   - Singular points and classes for dims: no_dim;;dTi_no_element;dTi_min;]dTi_min,dTi_sufficient[;dTi_sufficient;]dTi_sufficient,dTi_max[;dTi_max.
#     Let's set the values:
#      - no_dim = '-'
#      - dTi_no_element = 0
#      - dTi_min = 1
#      - dTi_sufficient = 3
#      - dTi_max = +inf; Not tractable
#      - Actual singular points and classes for dims: 
#        no_dim;;dTi_no_element;dTi_min;]dTi_min,dTi_sufficient[;dTi_sufficient;]dTi_sufficient = -;;0;1;]1,3[;3
# Combination of ranks and dims, with choice within the open intervals: {0;1;]1,4[;4} X {-;;0;1;]1,3[;3} per dimension for each rank.
#      - = {(0,-),(1,0),(1,1),(1,2),(1,3),(2,{0;1;]1,3[;3}X{0;1;]1,3[;3}),(4,{0;1;]1,3[;3}X{0;1;]1,3[;3}X{0;1;]1,3[;3}X{0;1;]1,3[;3})}
# Equivalence classes for A and B elements:
#      - EQCELTS: NaN;;-inf;]-inf,0[;0;]0,+inf[;+inf

# Two families of tests:
#      - Tests of the numerical aspects
#      - Tests of the dtructural aspects.

testnumber = 0

"""
Function to generate valid inputs for Add operator
"""
@st.composite
def valid_add_args(draw):
    global testnumber
    print(f"\nTest N1\n")
    testnumber=testnumber+1
    print("testnumber = ", testnumber)
    # a
    info_32 = np.finfo(np.float32)
    # La valeur la plus élevée (Positive)
    max_32 = info_32.max  # Env. 3.40e+38
    # La valeur la plus basse (Négative)
    min_32 = info_32.min  # Env. -3.40e+38
    # Le plus petit nombre positif au-dessus de zéro (Précision)
    tiny_32 = info_32.tiny # Env. 1.17e-38
    x_negative = draw(st.floats(min_value=min_32, max_value=-tiny_32))
    x_positive = draw(st.floats(min_value=tiny_32, max_value=max_32))
    data_a = [[[[np.nan,np.nan,np.nan,np.nan,np.nan,np.nan],
             [-np.inf,-np.inf,-np.inf,-np.inf,-np.inf,-np.inf],
             [x_negative,x_negative,x_negative,x_negative,x_negative,x_negative],
             [0,0,0,0,0,0],
             [x_positive,x_positive,x_positive,x_positive,x_positive,x_positive],
             [np.inf,np.inf,np.inf,np.inf,np.inf,np.inf]]]]
    a = np.array(data_a, dtype=np.float32)
    # b
    data_b = [[[[np.nan,-np.inf,x_negative,0,x_positive,np.inf],
             [np.nan,-np.inf,x_negative,0,x_positive,np.inf],
             [np.nan,-np.inf,x_negative,0,x_positive,np.inf],
             [np.nan,-np.inf,x_negative,0,x_positive,np.inf],
             [np.nan,-np.inf,x_negative,0,x_positive,np.inf],
             [np.nan,-np.inf,x_negative,0,x_positive,np.inf]]]]
    b = np.array(data_b, dtype=np.float32)

    data_ref_y = [[[[np.nan,np.nan,np.nan,np.nan,np.nan,np.nan],
          [np.nan,-np.inf,-np.inf,-np.inf,-np.inf,np.nan],
          [np.nan,-np.inf,x_negative+x_negative,x_negative,x_negative+x_positive,np.inf],
          [np.nan,-np.inf,x_negative,0,x_positive,np.inf],
          [np.nan,-np.inf,x_negative+x_positive,x_positive,x_positive+x_positive,np.inf],
          [np.nan,np.nan,np.inf,np.inf,np.inf,np.inf]]]]
    ref_y = np.array(data_ref_y, dtype=np.float32)   

    return a, b, ref_y

"""
Run ONNX runtime with generated inputs and check constraints
"""
@st.composite
def valid_add_args_S1(draw):
# Structural test S1
#   - selected shape = () = scalar, i.e., rank = 0 and no dimension: (0,-) as equivalence class.
#   - EQCELTS: NaN;;-inf;]-inf,0[;0;]0,+inf[;+inf:
#        - selected value for a = 31.0
#        - selected value for b = 50.0
    print(f"\nTest S1\n")
    a = np.array(31.0, dtype=np.float32)
    b = np.array(50.0, dtype=np.float32)
    ref_y = np.array(81.0, dtype=np.float32)

    return a, b, ref_y


@st.composite
def valid_add_args_S2toS5(draw):
# Structural test S2, S3, S4 and S5, all with rank = 1
#   - selected shapes:
#        - S2:(1,0): empty tensors
#        - S3:(1,1): 1-element tensors
#        - S4:(1,2)
#        - S5:(1,3)
#   - EQCELTS: NaN;;-inf;]-inf,0[;0;]0,+inf[;+inf:
#        - selected values for non-empty a = 31.0
#        - selected values for non-empty b = 50.0

    range_d0 = 4
    nbtests=range_d0
    tabret = np.empty(nbtests, dtype=object)

    index = 0
    for d0 in range(range_d0):
        a = np.full((d0), 31.0, dtype="float32")
        b = np.full((d0), 50.0, dtype="float32")
        ref_y = np.full((d0), 81.0, dtype="float32")
        tabret[index] = [a,b,ref_y]
        index += 1

    return tabret, nbtests

@st.composite
def valid_add_args_S6toS21(draw):
#(2,{0;1;]1,3[;3}X{0;1;]1,3[;3})
# Structural test S6, S7, S8...S21, all with rank = 2
#   - selected shapes: {(d0,d1 | d0 and d1 in {0,3})} => 16 cases
#   - EQCELTS: NaN;;-inf;]-inf,0[;0;]0,+inf[;+inf:
#        - selected values for non-empty a = 31.0
#        - selected values for non-empty b = 50.0
  
    range_d0 = 4
    range_d1 = 4
    nbtests = range_d0 * range_d1
    tabret = np.empty(nbtests, dtype=object)

    index = 0
    for d0 in range(range_d0):
        for d1 in range(range_d1):
            a = np.full((d0, d1), 31.0, dtype="float32")
            b = np.full((d0, d1), 50.0, dtype="float32")
            ref_y = np.full((d0, d1), 81.0, dtype="float32")
            tabret[index] = [a,b,ref_y]
            index += 1
    
    return tabret, nbtests


@st.composite
def valid_add_args_S22toS277(draw):
# (4,{0;1;]1,3[;3}X{0;1;]1,3[;3}X{0;1;]1,3[;3}X{0;1;]1,3[;3})
# Structural test S6, S7, S8...S85, all with rank = 4
#   - selected shapes: {(d0,d1, d2 | d0, d1 and d2 in {0,3})} => 64 cases
#   - EQCELTS: NaN;;-inf;]-inf,0[;0;]0,+inf[;+inf:
#        - selected values for non-empty a = 31.0
#        - selected values for non-empty b = 50.0
  
    range_d0 = 4
    range_d1 = 4
    range_d2 = 4
    range_d3 = 4
    nbtests = range_d0 * range_d1 * range_d2 * range_d3
    tabret = np.empty(nbtests, dtype=object)

    index = 0
    for d0 in range(range_d0):
        for d1 in range(range_d1):
            for d2 in range(range_d2):
                for d3 in range(range_d3):
                    a = np.full((d0, d1, d2, d3), 31.0, dtype="float32")
                    b = np.full((d0, d1, d2, d3), 50.0, dtype="float32")
                    ref_y = np.full((d0, d1, d2, d3), 81.0, dtype="float32")
                    tabret[index] = [a,b,ref_y]
                    index += 1

    return tabret, nbtests

@settings(max_examples= 10,deadline=None)
@given(valid_add_args())
def test_Add(args):
    print("--------------------------------------------------")
    a, b, ref_y = args

    y, node_def = make_session(a, b, ref_y)
    check_test_result_add(y,ref_y)
    check_constraints(a, b, y, ref_y, node_def)

@settings(max_examples= 1,deadline=None)
@given(valid_add_args_S1())
def test_Add_S1(args):
    a, b, ref_y = args

    y, node_def = make_session(a, b, ref_y)
    check_test_result_add(y,ref_y)
    check_constraints(a, b, y, ref_y, node_def)

@settings(max_examples= 1,deadline=None)
@given(valid_add_args_S2toS5())
def test_Add_S2toS5(args):
    tabret, nbtests = args

    for nbt in range(nbtests):
        indextest=2+nbt
        print(f"\nTest S2 to S5:", indextest)
        y, node_def = make_session(tabret[nbt][0], tabret[nbt][1], tabret[nbt][2])
        check_test_result_add(y,tabret[nbt][2])
        check_constraints(tabret[nbt][0], tabret[nbt][1], y, tabret[nbt][2], node_def)


@settings(max_examples= 1,deadline=None)
@given(valid_add_args_S6toS21())
def test_Add_S6toS21(args):
    tabret, nbtests = args
    
    for nbt in range(nbtests):
        indextest=6+nbt
        print(f"\nTest S6 to S21:", indextest)
        y, node_def = make_session(tabret[nbt][0], tabret[nbt][1], tabret[nbt][2])
        check_test_result_add(y,tabret[nbt][2])
        check_constraints(tabret[nbt][0], tabret[nbt][1], y, tabret[nbt][2], node_def)        

@settings(max_examples= 1,deadline=None)
@given(valid_add_args_S22toS277())
def test_Add_S22toS85(args):
    tabret, nbtests = args
    
    for nbt in range(nbtests):
        indextest=22+nbt
        print(f"\nTest S22 to S277:", indextest)
        y, node_def = make_session(tabret[nbt][0], tabret[nbt][1], tabret[nbt][2])
        check_test_result_add(y,tabret[nbt][2])
        check_constraints(tabret[nbt][0], tabret[nbt][1], y, tabret[nbt][2], node_def)

def make_session(a, b, ref_y):
    a_onnx = helper.make_tensor_value_info('a_onnx', helper.np_dtype_to_tensor_dtype(a.dtype), a.shape)
    b_onnx = helper.make_tensor_value_info('b_onnx', helper.np_dtype_to_tensor_dtype(b.dtype), b.shape)

 
    node_def = helper.make_node(
        'Add',
        ['a_onnx', 'b_onnx'],
        ['y_onnx'],
    )

    graph_def = helper.make_graph(
        [node_def],
        'test-Add',
        [a_onnx, b_onnx],
        [helper.make_tensor_value_info('y_onnx', TensorProto.FLOAT, ref_y.shape)],
    )

    onnx_model = helper.make_model(graph_def)

    # Let's freeze the opset.
    del onnx_model.opset_import[:]
    opset = onnx_model.opset_import.add()
    opset.domain = ''
    opset.version = 22
    onnx_model.ir_version = 8

    # Verify the model
    onnx.checker.check_model(onnx_model)

    # Do inference
    sess = InferenceSession(onnx_model.SerializeToString(), providers=["CPUExecutionProvider"])

    y = sess.run(None, {'a_onnx': a, 'b_onnx': b})[0]

    print("a shape:", a.shape)
    print("A = ", a)
    print("B shape:", b.shape)
    print("B = ", b)

    print("Y shape:", y.shape)
    print("Y = ", y)

    print("ref_y =", ref_y)

    return y, node_def


def check_constraints(a, b, y, refy, node_def):

    #x - Constraints
    # C1
    assert a.shape == b.shape
    #assert all(dim > 0 for dim in a.shape)

    #Shape of the output
    assert y.shape == b.shape

    #Functional check    
#    assert np.array_equal(y, refy, equal_nan=True)
    assert np.allclose(y, refy, rtol=1.2e-01, atol=1.2e-01, equal_nan=True)

def Add(A, B):
    Y = A + B
    return Y

def check_test_result_add(Y,refY):
    print("\ncheck_test_result_add\n")
    y_f = (np.array2string(Y, separator=',', max_line_width=np.inf).replace('\n', '\n'))
    print(f"Y = \n{y_f}")
    refy_f = (np.array2string(refY, separator=',', max_line_width=np.inf).replace('\n', '\n'))
    print(f"refY = \n{refy_f}")
#    if np.array_equal(Y, refY, equal_nan=True):
    if np.allclose(Y, refY, rtol=1.2e-01, atol=1.2e-01, equal_nan=True):
        print(f"-> Test of add is OK\n")
    else:
        print(f"-> Test of add is KO\n")