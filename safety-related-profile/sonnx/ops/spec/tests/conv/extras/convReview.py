import math
import numpy
import onnx.checker
from onnx import helper, TensorProto
from onnxruntime import InferenceSession

# * Adding Padding to the Input Matrix
def padTrasform(X,pads):
    ## pads = [left,top,right,bottom]
    m_Lines = len(X)
    n_Cols = len(X[0])
    top = [[0 for j in range(0, n_Cols + pads[0] + pads[2])] for i in range(0, pads[1])]
    bottom = [[0 for j in range(0, n_Cols + pads[0] + pads[2])] for i in range(0, pads[3])]
    padded_rows = []
    for x in X:
        new_row = [0]*pads[0] + list(x) + [0]*pads[2]
        padded_rows.append(new_row)
    final = top + padded_rows + bottom
    return final

# * Adding Dilation to the Kernel Matrix
def kernelDilation(W, dilation):
    dW2 = len(W)
    dW3 = len(W[0])
    x_dil = dilation[0]
    y_dil = dilation[1]

    horiz_W = []
    for row in W:
        new_row = []
        for j in range(dW3):
            new_row.append(row[j])
            if j < dW3 - 1:
                for _ in range(y_dil - 1):
                    new_row.append(0)
        horiz_W.append(new_row)

    new_W = []
    for i in range(len(horiz_W)):
        new_W.append(horiz_W[i])
        if i < len(horiz_W) - 1:
            for _ in range(x_dil - 1):
                new_W.append([0] * len(horiz_W[0]))
    return new_W

 
""" Suggetion for Dy2 and DY3 Calculation """
# The dilated kernel is equal to the original kernel multiplied by the dilation factor
# and subtracted by ( dilation factor minus 1 ) because no zeros are added at the last margin.
# However, the value that was already in the matrix remains
# Assuming that dilation[0] refers to rows and dilation[1] to columns

"""
dw2 - original kernel rows
dilation[0] - dilation factor for rows

dW2_p = dW2 * dilation[0] - (dilation[0] - 1)

dw3 - original kernel columns
dilation[1] - dilation factor for columns

dW3_p = dW3 * dilation[1] - (dilation[1] - 1)

"""

def calculateDy2(dX2,pads,dW2,strides,dilation):
    alpha = dX2 + pads[1] + pads[3]
    theta = dilation[0] * (dW2 - 1) + 1
    finalResult = (alpha - theta) // strides[1] + 1
    return finalResult

def calculateDy3(dX3,pads,dW3,strides,dilation):
    beta = dX3 + pads[0] + pads[2]
    gamma = dilation[1] * (dW3 - 1) + 1
    finalResult = (beta - gamma) // strides[0] + 1
    return finalResult

## *! Wrong Dy2 Calculation
def wrongDy2(dX2,pads,dW2,strides,dilation):
    alpha = dX2 + pads[0] + pads[2]
    theta = dilation[0] * dW2 - 1
    finalResult = math.floor((alpha - theta) / strides[0]) + 1
    return finalResult

## *! Wrong Dy3 Calculation
def wrongDy3(dX3,pads,dW3,strides,dilation):
    beta = dX3 + pads[1] + pads[3]
    gamma = dilation[1] * dW3 - 1
    finalResult = math.floor((beta - gamma) / strides[1]) + 1
    return finalResult

def standConvDef(X,W):
    ## Move kernel 2 steps right and 1 step down
    strides = (2,3)
    pads = [1,2,2,2]
    dilation = (2,2)

    dW2 = len(W)
    dW3 = len(W[0])

    dX2 = len(X)
    dX3 = len(X[0])

    X_p = padTrasform(X,pads)
    W_p = kernelDilation(W,dilation)

    print("X_p:")
    printTensor(X_p)
    print("W_p:")
    printTensor(W_p)

    dY2 = calculateDy2(dX2,pads,dW2,strides,dilation)
    dY3 = calculateDy3(dX3,pads,dW3,strides,dilation)

    print("dY2:",dY2)
    print("dY3:",dY3)

    dW2_p = len(W_p)
    dW3_p = len(W_p[0])

    Y = [[0 for j in range(0, dY3)] for i in range(0, dY2)]
    
    for m in range(dY2):
        for n in range(dY3):
            for j in range(dW2_p):
                 for z in range(dW3_p):
                    ## TODO: Important Change
                    Y[m][n] += X_p[m*strides[1]+j][n*strides[0]+z] * W_p[j][z]

    return Y

# *! Wrong Version of their code (Sum Order)
def standConvDefWrong(X,W):
    ## Move kernel 2 steps right and 1 step down
    strides = (2,3)
    pads = [1,2,2,2]
    dilation = (2,2)

    X_p = padTrasform(X,pads)
    W_p = kernelDilation(W,dilation)

    print("X_p:")
    printTensor(X_p)
    print("W_p:")
    printTensor(W_p)

    dY2 = 4
    dY3 = 4

    dW2_p = len(W_p)
    dW3_p = len(W_p[0])

    Y = [[0 for j in range(0, dY3)] for i in range(0, dY2)]
    
    for m in range(dY2):
        for n in range(dY3):
            for j in range(dW2_p):
                 for z in range(dW3_p):
                    ## TODO: Wrong Change
                    Y[m][n] += X_p[m*strides[0]+j][n*strides[1]+z] * W_p[j][z]

    return Y

# *! Wrong Version of their code (Calculation of dY2 and dY3)
def standConvDefWrongY(X,W):
    ## Move kernel 2 steps right and 1 step down
    strides = (2,3)
    pads = [1,2,2,2]
    dilation = (2,2)

    X_p = padTrasform(X,pads)
    W_p = kernelDilation(W,dilation)

    dY2 = wrongDy2(len(X),pads,len(W),strides,dilation)
    dY3 = wrongDy3(len(X[0]),pads,len(W[0]),strides,dilation)

    print("dY2:",dY2)
    print("dY3:",dY3)

    dW2_p = len(W_p)
    dW3_p = len(W_p[0])

    Y = [[0 for j in range(0, dY3)] for i in range(0, dY2)]
    
    for m in range(dY2):
        for n in range(dY3):
            for j in range(dW2_p):
                 for z in range(dW3_p):
                    ## TODO: Important Change
                    Y[m][n] += X_p[m*strides[1]+j][n*strides[0]+z] * W_p[j][z]

    return Y


X = [
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1]
]

W = [
    [1,1,1],
    [1,1,1]
]


def printTensor(T):
    for x in T:
        print(x)

"""
Correct Version
"""
Y = standConvDef(X,W)
print("\nFinal Matrix Y (Correct):")
printTensor(Y)

"""
Wrong Version of their code (Sum Order)
"""
#Y_wrong = standConvDefWrong(X,W)
#print("\nFinal Matrix Y (Wrong):")
#printTensor(Y_wrong)

"""
Wrong Version of their code (Calculation of dY2 and dY3)
"""
#Y_wrong = standConvDefWrongY(X,W)
#print("\nFinal Matrix Y (Wrong):")
#printTensor(Y_wrong)

print("\n")
print("ONNX CHECK")

""""
ONNX CHECK
"""
x_Onnx = helper.make_tensor_value_info('x_Onnx', TensorProto.FLOAT, [1, 1, 8, 8])
w_Onnx = helper.make_tensor_value_info('w_Onnx', TensorProto.FLOAT, [1, 1, 3, 2])
b_Onnx = helper.make_tensor_value_info('b_Onnx', TensorProto.FLOAT, [1, 1])

node_def = helper.make_node(
    'Conv',
    ['x_Onnx', 'w_Onnx', 'b_Onnx'],
    ['y_Onnx'],
    dilations=[2,2],
    kernel_shape=[3,2],
    pads=[1, 2, 2, 2],
    strides=[2, 3],
    auto_pad='NOTSET',
    group=1,
)

graph_def = helper.make_graph(
    [node_def],
    'test-conv',
    [x_Onnx, w_Onnx, b_Onnx],
    [helper.make_tensor_value_info('y_Onnx', TensorProto.FLOAT, [1, 1, 4, 4])],
)

onnx_model = helper.make_model(graph_def)

# Let's freeze the opset.
del onnx_model.opset_import[:]
opset = onnx_model.opset_import.add()
opset.domain = ''
opset.version = 15
onnx_model.ir_version = 8

# Verify the model
onnx.checker.check_model(onnx_model)

# Print a human-readable representation of the graph
print(onnx.helper.printable_graph(onnx_model.graph))

# Do inference
sess = InferenceSession(onnx_model.SerializeToString(),
                        providers=["CPUExecutionProvider"])

# Initialize tensors
x = numpy.ones((1, 1, 8, 8), dtype=numpy.float32)
w = numpy.ones((1, 1, 3, 2), dtype=numpy.float32)
b = numpy.ones((1, 1), dtype=numpy.float32)

y = sess.run(None, {'x_Onnx': x, 'w_Onnx':w, 'b_Onnx': b})[0]

print("X shape:", x.shape)
print("X:", x)

print("W shape:", w.shape)
print("W:", w)

print("B shape:",
      b.shape)
print("B:", b)

print("Y shape:", y.shape)
print("Y:", y)
