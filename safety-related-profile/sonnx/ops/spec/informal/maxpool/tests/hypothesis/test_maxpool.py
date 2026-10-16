"""
Using hypothesis to generate automatic tests for MaxPool operator (SONNX)
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


#AUTO_PAD_OPTIONS = ["NOTSET", "VALID", "SAME_UPPER", "SAME_LOWER"]
AUTO_PAD_OPTIONS = ["NOTSET"]

"""
Function to generate valid inputs/atributes for Conv operator
"""
@st.composite
def valid_maxpool_args(draw):
    # x and w dimensions
    dx0 = draw(st.integers(min_value=1, max_value=1))
#    dx1 = draw(st.integers(min_value=256, max_value=256))
    dx1 = draw(st.integers(min_value=2, max_value=2))
#    dx2 = draw(st.integers(min_value=32, max_value=256))
    dx2 = draw(st.integers(min_value=8, max_value=8))
#    dx3 = draw(st.integers(min_value=32, max_value=256))
    dx3 = draw(st.integers(min_value=8, max_value=8))
#    dw0 = draw(st.integers(min_value=1, max_value=dx2))
#    dw1 = draw(st.integers(min_value=1, max_value=dx3))
    dw0 = draw(st.integers(min_value=3, max_value=3))
    dw1 = draw(st.integers(min_value=3, max_value=3))


    # x
    min_value = -10000.0
    max_value = 10000.0
    a_numeric = st.floats(min_value=min_value, max_value=max_value)
    x = draw(hnp.arrays(dtype=np.float32, shape=(dx0, dx1, dx2, dx3), elements=a_numeric))

    
    # Atributes
#    pads = draw(st.lists(
#        st.integers(min_value=0, max_value=1000), min_size=4, max_size=4)

#    )#FIXME: Check this Max Value
#    pads_0 = draw(st.integers(min_value=0, max_value=(dw0-1)))
#   pads_2 = draw(st.integers(min_value=0, max_value=(dw0-1)))
#   pads_1 = draw(st.integers(min_value=0, max_value=(dw1-1)))
#   pads_3 = draw(st.integers(min_value=0, max_value=(dw1-1)))
    pads_0 = draw(st.integers(min_value=0, max_value=(1)))
    pads_2 = draw(st.integers(min_value=0, max_value=(1)))
    pads_1 = draw(st.integers(min_value=0, max_value=(1)))
    pads_3 = draw(st.integers(min_value=0, max_value=(1)))
    pads = [pads_0, pads_1, pads_2, pads_3]
#   strides = draw(st.lists(st.integers(min_value=1, max_value=1000), min_size=2, max_size=2)
    strides = draw(st.lists(st.integers(min_value=1, max_value=1), min_size=2, max_size=2)
    ) #FIXME: Check this Max Value
    auto_pad = draw(st.sampled_from(AUTO_PAD_OPTIONS))
    kernel_shape = [dw0, dw1]

    # Auxiliary variables
    myalpha = dx2 + pads[0] + pads[2]
    mybeta = dx3 + pads[1] + pads[3]
    line_dilation_max = math.floor((myalpha-1) /(dw0 -1)) if dw0 > 1 else 1
    column_dilation_max = math.floor((mybeta-1) /(dw1 -1)) if dw1 > 1 else 1
    line_dilation_value = draw(st.integers(min_value=1, max_value=line_dilation_max))
    column_dilation_value = draw(st.integers(min_value=1, max_value=column_dilation_max))

    # Atributes
    dilation = [line_dilation_value, column_dilation_value]

    return x, pads, strides, dilation, auto_pad, kernel_shape

"""
Run ONNX runtime with generated inputs/atributes and check constraints
"""
@settings(max_examples= 1000,deadline=None)
@given(valid_maxpool_args())
def test_maxpool(args):
    print("--------------------------------------------------")
    x, pads, strides, dilation, auto_pad, kernel_shape = args
    dx0, dx1, dx2, dx3 = x.shape
    dw0, dw1 = kernel_shape

    myalpha = dx2 + pads[0] + pads[2]
    mybeta = dx3 + pads[1] + pads[3]
    mytheta = (dilation[0] * (dw0 - 1)) + 1
    mygamma = (dilation[1] * (dw1 - 1)) + 1
#dY_2 = \left\lfloor{(dX_2 + pad\_shape[0] - dilations[0] * (kernel\_shape[0] - 1) - 1) / strides[0] + 1}\right\rfloor
#Where: pad_shape[i] is the sum of the pads along spatial axis i
#    mydy2 = math.floor((myalpha - (mytheta)) / strides[0])) + 1
    mydy2 = math.floor(((myalpha - (mytheta)) / strides[0]) + 1)
#dY_3 = \left\lfloor{(dX_3 + pad\_shape[1] - dilations[1] * (kernel\_shape[1] - 1) - 1) / strides[1] + 1} \right\rfloor
#    where: pad_shape[i] is the sum of the pads along spatial axis i
#    mydy3 = math.floor((mybeta - (mygamma)) / strides[1]) + 1
    mydy3 = math.floor(((mybeta - (mygamma)) / strides[1]) + 1)

#    x_onnx = helper.make_tensor_value_info('x_onnx', TensorProto.FLOAT, [dx0, dx1, dx2, dx3])
    x_onnx = helper.make_tensor_value_info('x_onnx', helper.np_dtype_to_tensor_dtype(x.dtype), [dx0, dx1, dx2, dx3])
    

    if auto_pad == "NOTSET":
        node_def = helper.make_node(
            'MaxPool',
            ['x_onnx'],
            ['y_Onnx', 'indices_Onnx'],
            dilations=dilation,
            kernel_shape=kernel_shape,
            pads=pads,
            strides=strides,
            auto_pad='NOTSET',
        )
    else:
        node_def = helper.make_node(
            'MaxPool',
            ['x_onnx'],
            ['y_Onnx', 'indices_Onnx'],
            dilations=dilation,
            kernel_shape=[dw0, dw1],
            strides=strides,
            auto_pad=auto_pad,
        )

    graph_def = helper.make_graph(
        [node_def],
        'test-maxpool',
        [x_onnx],
        [helper.make_tensor_value_info('y_Onnx', TensorProto.FLOAT, [dx0, dx1, mydy2, mydy3]),
         helper.make_tensor_value_info('indices_Onnx', TensorProto.INT64, [dx0, dx1, mydy2, mydy3])],
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

#2026-01-06 09:44:30.219581227 [E:onnxruntime:, inference_session.cc:2280 operator()] Exception during initialization: 
#    /onnxruntime_src/onnxruntime/core/providers/cpu/nn/pool_attributes.h:78 
#       onnxruntime::PoolAttributes::PoolAttributes(const onnxruntime::OpNodeProtoHelper<onnxruntime::ProtoHelperNodeContext>&, 
#               const std::string&, int) pads[dim] < kernel_shape[dim] && pads[dim + kernel_shape.size()] < kernel_shape[dim] was false. 
#    Pad should be smaller than kernel.

    # Initialize tensors
    x = x.reshape(dx0, dx1, dx2, dx3).astype(np.float32)

    print("Pads", pads)
    print("Strides", strides)
    print("Dilation", dilation)
    print("Auto_pad", auto_pad)
    y = sess.run(None, {'x_onnx': x})[0]
    indices = sess.run(None, {'x_onnx': x})[1]

    print("x shape:", x.shape)
    print("x:", x)

#    padded_x = pad_4d_spatial_js(x, pads)
#    print ("padded_x:", padded_x)

    print("w shape:", kernel_shape)
    #print("w:", w)

    print("mydy2:", mydy2)
    print("mydy3:", mydy3)
    print("Y shape:", y.shape)
    print("Indices shape:", indices.shape)
    print("Y:", y)

    check_constraints(x, auto_pad, y, mydy2, mydy3, kernel_shape, strides, node_def, pads, dilation)

def check_constraints(x, auto_pad, y, mydy2,
                      mydy3, kernel_shape, strides,
                      node_def, pads, dilation):

    #x - Constraints
    # C1
    assert x.ndim == 4 and x.shape[2] >= 0 and x.shape[3] >= 0
    # C2: see C2 of y
    
    assert all(dim > 0 for dim in x.shape)


    #w - Constraints
    # TBD
    assert len(kernel_shape) == 2
    assert all(dim > 0 for dim in kernel_shape)

    #Strides - Constraints
    # C1
    assert all(s > 0 for s in strides)
    # C2
    assert len(strides) == 2


    #Auto_pad - Constraints
    #C1
    assert auto_pad in AUTO_PAD_OPTIONS
   
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
    assert len(dilation) == len(kernel_shape)
    # C3
    # Same of C3 of x


    #kernel shape - Constraints
    # C1
    for kernel_value in kernel_shape:
        assert kernel_value > 0
    # C2
    

    #Y - Constraints
    # C1
    #Same of C3 of x

    #Functional check    
    my_y = MaxPool(x, kernel_shape, strides, dilation, pads)
    print("my_y:", my_y)
    assert np.array_equal(y, my_y)

def compute_MaxPool_output_shape(input_shape, kernel_shape, pads, dilation, strides):

    dx0, dx1, dx2, dx3 = input_shape
    dw0, dw1 = kernel_shape


    myalpha = dx2 + pads[0] + pads[2]
    mybeta = dx3 + pads[1] + pads[3]
    mytheta = (dilation[0] * (dw0 - 1)) + 1
    mygamma = (dilation[1] * (dw1 - 1)) + 1
    mydy2 = math.floor(((myalpha - (mytheta)) / strides[0]) + 1)
    mydy3 = math.floor(((mybeta - (mygamma)) / strides[1]) + 1)
    
    output_shape = [dx0, dx1, mydy2, mydy3]

    return output_shape


def pad_4d_spatial_js(tensor, paddings):
    """
    Pads the last two dimensions (H, W) of a 4D tensor.
    paddings = (top, left, bottom, right)
    """
    N, C, H, W = tensor.shape
    top, left, bottom, right = paddings
    
    # 1. Calculate the new spatial dimensions
    new_H = H + top + bottom
    new_W = W + left + right
    
    # 2. Create the new 4D "canvas" of zeros
    # The Batch (N) and Channel (C) dimensions remain the same
#    padded_tensor = np.zeros((N, C, new_H, new_W), dtype=tensor.dtype)
    padded_tensor = np.full((N, C, new_H, new_W), -np.inf)
    
    # 3. Insert the original tensor into the padded one
    # We use ":" for N and C to select all batches and channels
    # We use slicing for the H and W dimensions
    padded_tensor[:, :, top : top + H, left : left + W] = tensor
    
    return padded_tensor

def extract_max_dilated_from_dilated_window(X_p, b, c, m, n, strides, dilations, dW):
    """
    Extracts the maximum value from a dilated window.
    
    Args:
        X_p: The 2D padded input array.
        m, n: Integer constants representing the current output position.
        strides: Tuple (s_h, s_w) for step size.
        dilations: Tuple (d_h, d_w) for spacing between window elements.
        dW: Tuple (dW0, dW1) for the window height and width.
    """
    dW0, dW1 = dW
    s_h, s_w = strides
    d_h, d_w = dilations
   
    # Calculate the base (top-left) coordinates based on the stride
    base_h = m * s_h
    base_w = n * s_w
    
    # Initialize max_val with the first element of the window (h=0, w=0)
    max_val = X_p[b, c, base_h, base_w]
    
    # Iterate through the window defined by dW0 and dW1
    for h in range(dW0):
        for w in range(dW1):
            # Calculate the current dilated coordinates
            curr_h = base_h + h * d_h
            curr_w = base_w + w * d_w
            
            # Extract the value at these coordinates
            val = X_p[b, c, curr_h, curr_w]
            
            # Update the maximum found so far
            if val > max_val:
                max_val = val
                
    return max_val

def MaxPool(X, kernel_shape, strides, dilation, pads):

    Y_dims = compute_MaxPool_output_shape(X.shape, kernel_shape, pads, dilation, strides)

    Y = np.zeros(Y_dims)

    X_p = pad_4d_spatial_js(X, pads)
    dX_p0, dX_p1, dX_p2, dX_p3 = X_p.shape
    dY_p0, dY_p1, dY_p2, dY_p3 = Y.shape

    print("X_p:", X_p)

    for b in range(dX_p0):
       for c in range(dX_p1): 
         for m in range(dY_p2):
           for n in range(dY_p3):
             Y[b, c, m, n] = extract_max_dilated_from_dilated_window(X_p, b, c, m, n, strides, dilation, kernel_shape)

    return Y