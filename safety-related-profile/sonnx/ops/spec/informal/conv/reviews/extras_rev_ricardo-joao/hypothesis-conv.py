"""
Using hypothesis to generate automatic tests for conv operator (SONNX)
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


AUTO_PAD_OPTIONS = ["NOTSET", "VALID", "SAME_UPPER", "SAME_LOWER"]

"""
Function to generate valid inputs/atributes for Conv operator
"""
@st.composite
def valid_conv_args(draw):
    # x and w dimensions
    dx0 = draw(st.integers(min_value=1, max_value=10))
    dx1 = draw(st.integers(min_value=1, max_value=10))
    dx2 = draw(st.integers(min_value=1, max_value=100))
    dx3 = draw(st.integers(min_value=1, max_value=100))
    dw0 = draw(st.integers(min_value=1, max_value=10))
    dw1 = dx1
    dw2 = draw(st.integers(min_value=1, max_value=dx2))
    dw3 = draw(st.integers(min_value=1, max_value=dx3))
    # x and w tensors
    x = draw(hnp.arrays(dtype=np.float32, shape=(dx0, dx1, dx2, dx3)))
    w = draw(hnp.arrays(dtype=np.float32, shape=(dw0, dw1, dw2, dw3)))
    #FIXME: Should BIAS be W1 or W0?
    bias = draw(hnp.arrays(dtype=np.float32, shape=(dw1,)))

    # Atributes
    pads = draw(st.lists(
        st.integers(min_value=0, max_value=1000), min_size=4, max_size=4)
    )#FIXME: Check this Max Value
    strides = draw(st.lists(
        st.integers(min_value=1, max_value=1000), min_size=2, max_size=2)
    ) #FIXME: Check this Max Value
    auto_pad = draw(st.sampled_from(AUTO_PAD_OPTIONS))
    kernel_shape = [dw2, dw3]

    # Auxiliary variables
    myalpha = dx2 + pads[0] + pads[2]
    mybeta = dx3 + pads[1] + pads[3]
    line_dilation_max = math.floor((myalpha-1) /(dw2 -1)) if dw2 > 1 else 1
    column_dilation_max = math.floor((mybeta-1) /(dw3 -1)) if dw3 > 1 else 1
    line_dilation_value = draw(st.integers(min_value=1, max_value=line_dilation_max))
    column_dilation_value = draw(st.integers(min_value=1, max_value=column_dilation_max))

    # Atributes
    dilation = [line_dilation_value, column_dilation_value]

    return x, w, bias,  pads, strides, dilation, auto_pad, kernel_shape

"""
Run ONNX runtime with generated inputs/atributes and check constraints
"""
@settings(max_examples= 1000,deadline=None)
@given(valid_conv_args())
def test_conv(args):
    print("--------------------------------------------------")
    x, w, bias, pads, strides, dilation, auto_pad, kernel_shape = args
    dx0, dx1, dx2, dx3 = x.shape
    dw0, dw1, dw2, dw3 = w.shape

    myalpha = dx2 + pads[0] + pads[2]
    mybeta = dx3 + pads[1] + pads[3]
    mytheta = (dilation[0] * (dw2 - 1)) + 1
    mygamma = (dilation[1] * (dw3 - 1)) + 1
    mydy2 = math.floor((myalpha - (mytheta)) / strides[0]) + 1
    mydy3 = math.floor((mybeta - (mygamma)) / strides[1]) + 1

    dy2 = math.floor( (myalpha - (dilation[0] * dw2 - 1)) / strides[0] ) + 1
    dy3 = math.floor( (mybeta - (dilation[1] * dw3 - 1)) / strides[1] ) + 1

    #FIXME: Review bias dimension
    x_onnx = helper.make_tensor_value_info('x_onnx', TensorProto.FLOAT, [dx0, dx1, dx2, dx3])
    w_onnx = helper.make_tensor_value_info('w_onnx', TensorProto.FLOAT, [dw0, dw1, dw2, dw3])
    b_onnx = helper.make_tensor_value_info('b_onnx', TensorProto.FLOAT, [dw1])

    if auto_pad == "NOTSET":
        node_def = helper.make_node(
            'Conv',
            ['x_onnx', 'w_onnx', 'b_onnx'],
            ['y_Onnx'],
            dilations=dilation,
            kernel_shape=kernel_shape,
            pads=pads,
            strides=strides,
            auto_pad='NOTSET',
            group=1,
        )
    else:
        node_def = helper.make_node(
            'Conv',
            ['x_onnx', 'w_onnx', 'b_onnx'],
            ['y_Onnx'],
            kernel_shape=[dw2, dw3],
            strides=strides,
            auto_pad=auto_pad,
            group=1,
        )

    graph_def = helper.make_graph(
        [node_def],
        'test-conv',
        [x_onnx, w_onnx, b_onnx],
        [helper.make_tensor_value_info('y_Onnx', TensorProto.FLOAT, [dx0, dw0, mydy2, mydy3])],
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
    x = x.reshape(dx0, dx1, dx2, dx3).astype(np.float32)
    w = w.reshape(dw0, dw1, dw2, dw3).astype(np.float32)
    b = bias.reshape((dw1,)).astype(np.float32)

    print("Pads", pads)
    print("Strides", strides)
    print("Dilation", dilation)
    print("Auto_pad", auto_pad)
    y = sess.run(None, {'x_onnx': x, 'w_onnx':w, 'b_onnx': b})[0]

    print("x shape:", x.shape)
    #print("x:", x)

    print("w shape:", w.shape)
    #print("w:", w)

    print("B shape:",b.shape)
    #print("B:", b)

    print("dy2:", dy2)
    print("dy3:", dy3)
    print("mydy2:", mydy2)
    print("mydy3:", mydy3)
    print("Y shape:", y.shape)
    #print("Y:", y)

    check_constraints(x, w, auto_pad, y, mydy2,
                      mydy3, kernel_shape, b, strides,
                      node_def, pads, dilation)


def check_constraints(x, w, auto_pad, y, mydy2,
                      mydy3, kernel_shape, b, strides,
                      node_def, pads, dilation):

    #x - Constraints
    # C1
    assert x.ndim == 4 and x.shape[2] >= 0 and x.shape[3] >= 0
    # C2
    assert x.shape[1] == w.shape[1]
    # C3 #FIXME: REVIEW THIS BECAUSE OF AUTO_PAD
    if auto_pad == "NOTSET":
        assert y.shape[2] == mydy2 and y.shape[3] == mydy3
    # C4 ??
    assert x.ndim == 4
    assert all(dim > 0 for dim in x.shape)


    #w - Constraints
    # C1
    # Same of C2 of x
    # C2
    #Same of C3 of x
    # C3
    kernel_shape[0] == w.shape[2] and kernel_shape[1] == w.shape[3]
    # C4
    assert w.ndim == 4
    assert all(dim > 0 for dim in w.shape)


    #B - Constraints
    #C1
    assert b.shape[0] == w.shape[1]

    #Strides - Constraints
    # C1
    assert all(s > 0 for s in strides)
    # C2
    assert len(strides) == 2
    # And same of C3 of x


    #Auto_pad - Constraints
    #C1
    assert auto_pad in AUTO_PAD_OPTIONS
    #C2
    if auto_pad != "NOTSET":
        assert all(attr.name!="pads" for attr in node_def.attribute)


    #Pads - Constraints
    # C1
    assert all(p >= 0 for p in pads)
    # C2
    assert len(pads) == (x.ndim - 2) * 2
    # C3
    # Same of C3 of x


    #Dilation - Constraints
    # C1
    assert all(d > 0 for d in dilation)
    # C2
    assert len(dilation) == (w.ndim - 2)
    # C3
    # Same of C3 of x


    #kernel shape - Constraints
    # C1
    for kernel_value in kernel_shape:
        assert kernel_value > 0
    # C2
    #Same of C3 of w

    #Y - Constraints
    # C1
    #Same of C3 of x
    