import math
import numpy as np
import os
import json

from hypothesis import given, settings
import hypothesis.extra.numpy as hnp
from hypothesis import strategies as st
from hypothesis import assume

from onnx import helper, TensorProto
import onnx.checker
from onnxruntime import InferenceSession


#TODO: Auto_pad "VALID" need more documentation to do the properly constraints
AUTO_PAD_OPTIONS = ["NOTSET", "SAME_UPPER", "SAME_LOWER"] #auto_pad  [C1], MISSING VALID

"""
Tensor value details
"""
tensor_range = {
    'min_value': -1e6,
    'max_value': 1e6,
    'allow_nan': False,
    'allow_infinity': False
}


"""
Inputs/attributes details
"""
inputs_atributes = {
    'min_dx0': 1, # Dimension should always be positive (batch size > 0)
    'max_dx0': 10, # Adjust as needed
    'min_dx1': 1, # Dimension should always be positive (channels > 0)
    'max_dx1': 10, # Adjust as needed
    'x_spatial_axis_min': 1, # Dimension should always be positive (spatial axes > 0)
    'x_spatial_axis_max': 10, # Adjust as needed
    'min_dw0': 1, # Dimension should always be positive (output channels > 0)
    'max_dw0': 10, # Adjust as needed
    'min_dw1': [], # W [C1] -> X [C2]
    'max_dw1': [], # W [C1] -> X [C2]
    'w_spatial_axis_min': 1, # Dimension should always be positive (spatial axes > 0)
    'w_spatial_axis_max': [], # W [C2] -> X [C3]
    'w_spatial_axis_max_unlimited': 10, # Used when auto_pad is not NOTSET
    'pads_min': 0, # Pads [C1]
    'pads_max': 10, # Adjust as needed
    'strides_min': 1, # Strides [C1]
    'strides_max': 10, # Adjust as needed
    'db0_min': [], # B [C1]
    'db0_max': [], # B [C1]
    'dilation_min': 1, # Dilations [C1]
    'dilation_max': [], # Dilations [C3] -> X [C3]
    'dilation_unlimited_max': 10, # Used when auto_pad is not NOTSET
    'groups': []
}


if os.path.exists("generated_data.json"):
    os.remove("generated_data.json")


"""
Store generated data
"""
generated_data = {
    "dx0": [],
    "dx1": [],
    "x_spatial_axis": [],
    "x": [],
    "dw0": [],
    "dw1": [],
    "w_spatial_axis": [],
    "w": [],
    "db0": [],
    "bias": [],
    "strides": [],
    "auto_pad": [],
    "pads": [],
    "dilations": [],
    "kernel_shape": [],
    "dy2": [],
    "dy3": [],
    "groups": []
}


"""
Function to generate valid convolution arguments
"""
@st.composite
def valid_conv_args(draw, inputs_atributes=inputs_atributes, tensor_range=tensor_range):
    float_strategy = st.floats(min_value=tensor_range['min_value'], max_value=tensor_range['max_value'], 
                               allow_nan=tensor_range['allow_nan'], allow_infinity=tensor_range['allow_infinity'])

    dx0 = draw(st.integers(min_value=inputs_atributes['min_dx0'], 
                           max_value=inputs_atributes['max_dx0']))
    
    dx1 = draw(st.integers(min_value=inputs_atributes['min_dx1'],
                            max_value=inputs_atributes['max_dx1']))
    

    # X [C1]
    num_spatial_axes_x = 2
    spatial_x_dimension_values = st.integers(min_value=inputs_atributes['x_spatial_axis_min'], 
                                           max_value=inputs_atributes['x_spatial_axis_max'])
    x_spatial_axis = draw(st.lists
                            (spatial_x_dimension_values,
                            min_size=num_spatial_axes_x,
                            max_size=num_spatial_axes_x))
    # X [C4]
    x = draw(hnp.arrays(dtype=np.float32, shape=(dx0, dx1, *x_spatial_axis),
                       elements=float_strategy))
    
    # Strides [C1]
    stride_value = st.integers(min_value=inputs_atributes['strides_min'], max_value=inputs_atributes['strides_max'])
    # Strides [C2] -> X [C3] - No value constraint just size
    stride_axis_number = 2
    strides = draw(st.lists(stride_value, min_size=stride_axis_number, max_size=stride_axis_number))

    # Groups [C1]
    # Groups [C2]
    # Groups [C3]
    VALID_GROUPS = [1, dx1]
    groups = draw(st.sampled_from(VALID_GROUPS))
    inputs_atributes['groups'].append(groups)
    
    # Groups [C2]
    VALID_VALUES_DW0 = [i for i in range(inputs_atributes['min_dw0'], inputs_atributes['max_dw0'] + 1) if i % groups == 0]
    dw0 = draw(st.sampled_from(VALID_VALUES_DW0))

    #dw0 = draw(st.integers(min_value=inputs_atributes['min_dw0'], max_value=inputs_atributes['max_dw0']))
    # W [C1] -> X [C2] #This value does not need to be generated, by X [C2] constraint
    dw1 = dx1
    # Groups Documentation Additional Constraint
    dw1 = dw1 // groups
    inputs_atributes['min_dw1'].append(dx1//groups)
    inputs_atributes['max_dw1'].append(dx1//groups)

    num_spatial_axes_w = 2

    
    # Auto Pad [C1]
    auto_pad = draw(st.sampled_from(AUTO_PAD_OPTIONS))
    # Auto Pad [C2]
    if auto_pad == "NOTSET":
        # Pads [C1]
        pads_value = st.integers(min_value=inputs_atributes['pads_min'], max_value=inputs_atributes['pads_max'])
        # Pads [C2]
        pads = draw(st.lists(
                        pads_value,
                        min_size=2*num_spatial_axes_x,
                        max_size=2*num_spatial_axes_x
                        ))
        #Pads [C3] -> X [C3]
        #No Constraint, variable not restricted

        # W [C2] -> X [C3] - FIXME - REVIEW THIS, Needed because of explicit padding
        alpha =  pads[0] + pads[2] + x_spatial_axis[0]
        beta =  pads[1] + pads[3] + x_spatial_axis[1]
        spatial_dimension_values_w_max = [alpha, beta]
        inputs_atributes['w_spatial_axis_max'].append(spatial_dimension_values_w_max)
        w_spatial_axis = [draw(st.integers(min_value=inputs_atributes['w_spatial_axis_min'], 
                                           max_value=spatial_dimension_values_w_max[i])) for i in range(num_spatial_axes_w)]
        
        # Dilations [C1] 
        # Dilations [C3] -> X [C3]
        dilation_max = []
        for i in range(num_spatial_axes_w):
            if w_spatial_axis[i] > 1:
                dilation_max.append(math.floor((spatial_dimension_values_w_max[i] - 1) / (w_spatial_axis[i] - 1)))
            else:
                dilation_max.append(inputs_atributes['dilation_unlimited_max'])

        inputs_atributes['dilation_max'].append(dilation_max)
        # Dilations [C2]
        dilations = [draw(st.integers
                            (min_value=inputs_atributes['dilation_min'],
                            max_value=dilation_max[i])) for i in range(num_spatial_axes_w)]

        theta = (dilations[0] * (w_spatial_axis[0] - 1)) + 1
        gamma = (dilations[1] * (w_spatial_axis[1] - 1)) + 1

        # y spatial dimension calculations
        # When auto_pad is NOTSET, pads are explicit
        # X [C3]
        dy2 = math.floor(((alpha - (theta)) / strides[0])) + 1
        dy3 = math.floor(((beta - (gamma)) / strides[1])) + 1

    else:
        pads = []
        dilations = []
        spatial_w_dimension_values = st.integers(min_value=inputs_atributes['w_spatial_axis_min'],
                                            max_value=inputs_atributes['w_spatial_axis_max_unlimited'])
        
        inputs_atributes['w_spatial_axis_max'].append([inputs_atributes['w_spatial_axis_max_unlimited']] * num_spatial_axes_w)
        w_spatial_axis = draw(st.lists
                                (spatial_w_dimension_values,
                                min_size=num_spatial_axes_w,
                                max_size=num_spatial_axes_w))

        # y spatial dimension calculations
        # When auto_pad is different from NOTSET
        # X [C3]
        dy2 = math.ceil(x_spatial_axis[0] / strides[0])
        dy3 = math.ceil(x_spatial_axis[1] / strides[1])

    # W [C4]    
    w = draw(hnp.arrays(dtype=np.float32, shape=(dw0, dw1, *w_spatial_axis),
                       elements=float_strategy))

    # B [C1] # This value does not need to be generated, once it is always equal to dw0
    db0 = dw0
    inputs_atributes['db0_min'].append(dw0)
    inputs_atributes['db0_max'].append(dw0)
    bias = draw(hnp.arrays(dtype=np.float32, shape=(db0,),
                        elements=float_strategy))

    # Kernel Shape [C1]
    # Kernel Shape [C2] -> W [C3]
    # This data is not need to be generated, once it is always equal to w_spatial_axis
    kernel_shape = w_spatial_axis


    return dx0, dx1, x_spatial_axis, x, dw0, dw1, w_spatial_axis, w, db0, bias, strides, auto_pad, pads, dilations, kernel_shape, dy2, dy3, groups


"""
Function that runs the test
"""
@settings(max_examples=1000, deadline=None)
@given(valid_conv_args())
def test_conv(args):
    dx0, dx1, x_spatial_axis, x, dw0, dw1, w_spatial_axis, w, db0, bias, strides, auto_pad, pads, dilations, kernel_shape, dy2, dy3, groups = args
    generated_data["dx0"].append(dx0)
    generated_data["dx1"].append(dx1)
    generated_data["x_spatial_axis"].append(x_spatial_axis)
    generated_data["x"].append(x.tolist())
    generated_data["dw0"].append(dw0)
    generated_data["dw1"].append(dw1)
    generated_data["w_spatial_axis"].append(w_spatial_axis)
    generated_data["w"].append(w.tolist())
    generated_data["db0"].append(db0)
    generated_data["bias"].append(bias.tolist())
    generated_data["strides"].append(strides)
    generated_data["auto_pad"].append(auto_pad)
    generated_data["pads"].append(pads)
    generated_data["dilations"].append(dilations)
    generated_data["kernel_shape"].append(kernel_shape)
    generated_data["dy2"].append(dy2)
    generated_data["dy3"].append(dy3)
    generated_data["groups"].append(groups)

    y, node_def = run_onnx_conv(dx0, dx1, x_spatial_axis, x, 
                  dw0, dw1, w_spatial_axis, w, 
                  db0, bias,strides, auto_pad, 
                  pads, dilations, kernel_shape, dy2, dy3, groups)
    
    check_constraints(x, w, auto_pad, y, dy2,
                      dy3, kernel_shape, bias, strides,
                      node_def, pads, dilations, groups)


"""
Function to write generated data to a json file
"""
def teardown_module():
    dados = {
        "titulo": "Dados gerados pelo Hypothesis",
        "min_dx0": inputs_atributes['min_dx0'],
        "max_dx0": inputs_atributes['max_dx0'],
        "dx0": generated_data["dx0"],
        "min_dx1": inputs_atributes['min_dx1'],
        "max_dx1": inputs_atributes['max_dx1'],
        "dx1": generated_data["dx1"],
        "x_spatial_axis_min": inputs_atributes['x_spatial_axis_min'],
        "x_spatial_axis_max": inputs_atributes['x_spatial_axis_max'],
        "x_spatial_axis": generated_data["x_spatial_axis"],
        "x": generated_data["x"],
        "min_dw0": inputs_atributes['min_dw0'],
        "max_dw0": inputs_atributes['max_dw0'],
        "dw0": generated_data["dw0"],
        "min_dw1": inputs_atributes['min_dw1'],
        "max_dw1": inputs_atributes['max_dw1'],
        "dw1": generated_data["dw1"],
        "w_spatial_axis_min": inputs_atributes['w_spatial_axis_min'],
        "w_spatial_axis_max": inputs_atributes['w_spatial_axis_max'],
        "w_spatial_axis": generated_data["w_spatial_axis"],
        "w": generated_data["w"],
        "db0_min": inputs_atributes['db0_min'],
        "db0_max": inputs_atributes['db0_max'],
        "db0": generated_data["db0"],
        "bias": generated_data["bias"],
        "strides_min": inputs_atributes['strides_min'],
        "strides_max": inputs_atributes['strides_max'],
        "strides": generated_data["strides"],
        "auto_pad": generated_data["auto_pad"],
        "pads_min": inputs_atributes['pads_min'],
        "pads_max": inputs_atributes['pads_max'],
        "pads": generated_data["pads"],
        "dilation_min": inputs_atributes['dilation_min'],
        "dilation_max": inputs_atributes['dilation_max'],
        "dilations": generated_data["dilations"],
        "kernel_shape": generated_data["kernel_shape"],
        "dy2": generated_data["dy2"],
        "dy3": generated_data["dy3"]
    }

    with open("generated_data.json", "w") as f:
        json.dump(dados, f, indent=4)


"""
Function that runs the ONNX Conv operation
"""
def run_onnx_conv(dx0, dx1, x_spatial_axis, x, 
                  dw0, dw1, w_spatial_axis, w, 
                  db0, bias, strides, auto_pad, 
                  pads, dilations, kernel_shape, dy2, dy3, groups):

    x_onnx = helper.make_tensor_value_info('x_onnx', TensorProto.FLOAT, [dx0, dx1, x_spatial_axis[0], x_spatial_axis[1]])
    w_onnx = helper.make_tensor_value_info('w_onnx', TensorProto.FLOAT, [dw0, dw1, w_spatial_axis[0], w_spatial_axis[1]])
    b_onnx = helper.make_tensor_value_info('b_onnx', TensorProto.FLOAT, [dw0])

    if auto_pad == "NOTSET":
        node_def = helper.make_node(
            'Conv',
            ['x_onnx', 'w_onnx', 'b_onnx'],
            ['y_Onnx'],
            dilations=dilations,
            kernel_shape=kernel_shape,
            pads=pads,
            strides=strides,
            auto_pad='NOTSET',
            group=groups,
        )
    else:
        node_def = helper.make_node(
            'Conv',
            ['x_onnx', 'w_onnx', 'b_onnx'],
            ['y_Onnx'],
            kernel_shape=kernel_shape,
            strides=strides,
            auto_pad=auto_pad,
            group=groups,
        )

    graph_def = helper.make_graph(
        [node_def],
        'test-conv',
        [x_onnx, w_onnx, b_onnx],
        [helper.make_tensor_value_info('y_Onnx', TensorProto.FLOAT, [dx0, dw0, dy2, dy3])],
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
    sess = InferenceSession(onnx_model.SerializeToString(),
                            providers=["CPUExecutionProvider"])

    # Initialize tensors
    x = x.reshape(dx0, dx1, x_spatial_axis[0], x_spatial_axis[1]).astype(np.float32)
    w = w.reshape(dw0, dw1, w_spatial_axis[0], w_spatial_axis[1]).astype(np.float32)
    b = bias.reshape((dw0,)).astype(np.float32)

    y = sess.run(None, {'x_onnx': x, 'w_onnx':w, 'b_onnx': b})[0]
    
    print("Output shape:", y.shape)
    print("Output values:", y)
    return y, node_def


"""
Function that defines asserts for the constraints
"""
def check_constraints(x, w, auto_pad, y, dy2,
                      dy3, kernel_shape, bias, strides,
                      node_def, pads, dilation, groups):

    # X Constraints
    # X [C1]
    assert x.ndim == 4 and x.shape[0] > 0 and x.shape[1] > 0 and x.shape[2] > 0 and x.shape[3] > 0
    # X [C2] -> FIXME probably need review on informal spec
    assert x.shape[1] == w.shape[1] * groups
    # X [C3]
    assert y.shape[2] == dy2 and y.shape[3] == dy3

    # W Constraints
    # W [C1] -> X [C2]
    # W [C2] -> X [C3]
    # W [C3]
    kernel_shape[0] == w.shape[2] and kernel_shape[1] == w.shape[3]
    # W [C4]
    assert w.ndim == 4
    assert all(dim > 0 for dim in w.shape)


    # B Constraints
    # B [C1]
    assert bias.shape[0] == w.shape[0]

    # Strides Constraints
    # S [C1]
    assert all(s > 0 for s in strides)
    # S [C2]
    assert len(strides) == 2
    # S [C2] -> X [C3]


    # Auto_pad Constraints
    # auto_pad [C1]
    assert auto_pad in AUTO_PAD_OPTIONS
    # auto_pad [C2]
    if auto_pad != "NOTSET":
        assert all(attr.name!="pads" for attr in node_def.attribute)

    if auto_pad == "NOTSET":
        # Pads Constraints
        # Pads [C1]
        assert all(p >= 0 for p in pads)
        # Pads [C2] 
        assert len(pads) == (x.ndim - 2) * 2
        # Pads [C3] -> X [C3]

        # Dilation - Constraints
        # Dilation [C1]
        assert all(d > 0 for d in dilation)
        # Dilation [C2]
        assert len(dilation) == (w.ndim - 2)
        # Dilation [C3] -> X [C3]

    # Groups - Constraints
    # Groups [C1]
    assert groups > 0
    # Groups [C2]
    assert x.shape[1] % groups == 0
    assert y.shape[1] % groups == 0
    # Groups [C3]
    assert groups == 1 or groups == x.shape[1]

    # Kernel shape - Constraints
    # Kernel shape [C1]
    assert all(k > 0 for k in kernel_shape)
    # Kernel shape [C2] -> W [C3]

    # Y - Constraints
    # Y [C1] -> X [C3]
