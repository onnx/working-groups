# Template

## Issue `<issue id>`: `<issue title>`

- CAT: _category in {__OPERATOR__ , __GRAPH__ , __FORMAT__}_
- CRIT: _criticality in { __LOW__  , __HIGH__ }_
- REQ:	_Identification of the SONNX requirement that can't be satisfied due to this issue_
- LOC: 	_Location in the standard, possibly using an hyperlink__

### Issue
_Description of the issue (in a synthetic way)_

### Consequence
_Brief description of the effect the issue on the development activities._

### Proposal
_Proposal to solve the issue or mitigate its consequences_

### Remarks (opt)
_Additional remarks_

# Issues - Non operators

## Issue #1.1: Execution order of graph nodes
- CAT: GRAPH
- CRI: LOW
- REQ: (TBC)
- LOC: [Open Neural Network Exchange Intermediate Representation (ONNX IR) Specification](https://github.com/onnx/onnx/blob/main/docs/IR.md)

### Issue
The ONNX specification states that "Each computation dataflow graph is structured as a topologically sorted list of nodes that form a graph, which MUST be free of cycles. [...] ". The topological order is a partial order.

### Consequence
Different implementations may execute nodes in different orders, leading to different results when computations are done using floating poit numbers. 

### Proposal
The SONNX standard should provide a means to impose a total ordering on the nodes. 

### Remarks
This constraint will prevent optimisations. 
Note that nothing prevents a model to be ill-formed. Compliance with the syntax and semantics of the ONNX standard must be checked (it is certainly checked, but nothing is said about what is checked or not and whether these checkers are complete / correct or not). 

Other constraints are given in the [onnx-ml.proto3](https://github.com/onnx/onnx/blob/main/onnx/onnx-ml.proto3). E.g.: 

    // One FunctionProto can reference other FunctionProto in the model, however, recursive reference
    // is not allowed.

## Issue #1.2: Overloading

- CAT: (to be completed)
- CRIT: (to be completed)
- REQ:	(to be completed)
- LOC: 	ONNX file format definition ([onnx-ml.proto3](https://github.com/onnx/onnx/blob/main/onnx/onnx-ml.proto3)) 

### Issue
A [function in ONNX](https://onnx.ai/onnx/intro/concepts.html) is a way to reuse the same combination of operators at different locations in a model. A function may refer to operators that are in a different opset than the model itself. In that case, the standard leaves the runtimes the freedom to chose whether the local  

    // The (domain, name, overload) tuple must be unique across the function protos in this list.
    // In case of any conflicts the behavior (whether the model local functions are given higher priority,
    // or standard operator sets are given higher priotity or this is treated as error) is defined by
    // the runtimes.

### Consequence
(TBC)

### Proposal
(TBC)

### Remarks (opt)
(TBC)

## Issue #1.3: opset resolution

- CAT: (to be completed)
- CRIT: (to be completed)
- REQ:	(to be completed)
- LOC: 	ONNX file format definition ([onnx-ml.proto3](https://github.com/onnx/onnx/blob/main/onnx/onnx-ml.proto3)) 

### Issue
A [function in ONNX](https://onnx.ai/onnx/intro/concepts.html) is a way to reuse the same combination of operators at different locations in a model. A function may refer to operators that are in a different opset than the model itself. In that case, the standard leaves the runtimes the freedom to chose whether the local  

    // The (domain, name, overload) tuple must be unique across the function protos in this list.
    // In case of any conflicts the behavior (whether the model local functions are given higher priority,
    // or standard operator sets are given higher priotity or this is treated as error) is defined by
    // the runtimes.

### Consequence
(TBC)

### Proposal
(TBC)

### Remarks
As per the ONNX IR documentation: "each function contained in a Model (also referred to as a model-local function) serves as a default or fallback implementation of the corresponding operator. A runtime, however, may choose to use an alternative implementation of the operator (usually as an optimized kernel). As such, the unique name of a function is significant as it is implicitly associated with a semantic specification."

From opset10 onwards, a function is uniquely identified by the triple (domain, name, overload).


## Issue #1.4: Function polymorphism

- CAT: (TBC)
- CRI: (TBC)
- REQ: (TBC)
- LOC: [Shape inference in ONNX](https://onnx.ai/onnx/api/shape_inference.html), this also covers type inference.

### Issue
Function tensor input and output data type and shape are not specified by the ONNX format. Actual types are obtained using type inference. 

### Consequence
The actual types and shapes are not explicit in the model: they can only be knwon once the input tensors are known.

### Proposal
Enforce that all tensor data types and shapes are explicit in the model.

### Remarks (opt)

## Issue #1.5: Shape broadcasting

- CAT: (TBC)
- CRI: (TBC)
- REQ: (TBC)
- LOC: [Broadcasting in ONNX](https://github.com/onnx/onnx/blob/main/docs/Broadcasting.md)

### Issue
The broadcasting logic is insufficiently specified on the ONNX documentation.

MatMul is using numpy broadcast spec : [MatMul](https://numpy.org/doc/stable/reference/generated/numpy.matmul.html)

[Gemm](https://onnx.ai/onnx/operators/onnx__Gemm.html) is unidirectional broadcast-able

element wise Add, Mul, Sub... are multidirectional broadcast-able

### Consequence
Several reported issues with onnx to C code generators, which complexity increases with this broadcast capability.

### Proposal
(TBC)

### Remarks
About broadcasting, see the [dedicated section of the NumPy manual ](https://numpy.org/doc/stable/user/basics.broadcasting.html#general-broadcasting-rules)

## Issue #1.6: Overloading

- CAT: (TBC)
- CRI: (TBC)
- REQ: (TBC)
- LOC: See section on Functions in [Open Neural Network Exchange Intermediate Representation (ONNX IR) Specification](https://github.com/onnx/onnx/blob/main/docs/IR.md)

### Issue
IR version 10 introduces overloading, i.e. the capability to have several definitions for the same function, and select them using a new ‘overloading’ field.

### Consequence
(TBC)

### Proposal
(TBC)

## Issue #1.7: Variadic inputs

- CAT: (TBC)
- CRI: (TBC)
- REQ: (TBC)
- LOC: 

### Issue
Variadic operators can accept any number of inputs.


### Consequence
(TBC)

### Proposal
Introduce a maximal number of parameters.

### Remarks

## Issue #1.8: Dynamic (Node input) vs static (Node attribute)

- CAT: (TBC)
- CRI: (TBC)
- REQ: (TBC)
- LOC: 

### Issue
The semantics is not clear that Node  input is dynamic and Node attribute is static.
As attributes can take Tensor values, these values might come from other Nodes (constant or not)

### Consequence
(TBC)

### Proposal
Introduce a maximal number of parameters.

### Remarks


## Issue #1.9: Data storage

- CAT: (TBC)
- CRI: LOW
- REQ: (TBC)
- LOC: [onnx-ml.proto3](https://github.com/onnx/onnx/blob/main/onnx/onnx-ml.proto3#L611) 

### Issue

### Consequence
(TBC)

### Proposal

### Remarks

ONNX supports __typed__ and __raw__ serialization of data. When __raw_data__ are used, the standard specifies that data must be stored in as "fixed-width, little endian order" with other specific constraints for float64, complex64, etc. data.

Do we need to specify our own encoding format?

## Issue #1.10: Quantization consistency

- CAT: (TBC)
- CRI: LOW
- REQ: (TBC)
- LOC: (TBC)

### Issue

### Consequence
(TBC)

### Proposal

### Remarks

ONNX supports __Quantization__ operators. Quantization data types are not consistent accross operators.
[QuantizeLinear](https://onnx.ai/onnx/operators/onnx__QuantizeLinear.html) is able to output int16, uint16, but [QLinearMatMul](https://onnx.ai/onnx/operators/onnx__QLinearMatMul.html), [QLinearConv](https://onnx.ai/onnx/operators/onnx__QLinearConv.html), [MatMulInteger](https://onnx.ai/onnx/operators/onnx__MatMulInteger.html) and [ConvInteger](https://onnx.ai/onnx/operators/onnx__ConvInteger.html#l-onnx-doc-convinteger) do not support these types.

# Operators

## Issue #2.1: Incomplete specification of SPLIT operator

- CAT: Operator
- CRIT: High
- REQ:	(TBC)
- LOC: https://onnx.ai/onnx/operators/onnx__Split.html

### Issue
1. The "axis" attribute gives an integer to define the axis along which split the input tensor into a list of tensors. The onnx documentation does not specify the correspondance between the integer and the axis of the tensor. Is the following interpretation the correct representation ? : 
- axis = '0' <=> batch ?
- axis = '1' <=> channels ?
- axis = '2' <=> rows ?
- axis = '3' <=> columns ?

2. Moreover, the "split" input gives a tensor which indicate the length of the 'axis' specified for each output tensor. For example, if the shape of the input tensor is [1,32,320,320] (assuming 32=channels, 320=lines and 320=columns) and the "split" input is [16,16] with the "axis" attribute = 1, then the operator splits the input tensor into two output tensors [1,16,320,320] and [1,16,320,320]. In general, the next layer of the network applies its operation on one of the two output tensors and the other one is kept for use in a deeper layer of the network. But the documentation does not specify which 16 channels are used in the next layer and which 16 channels are set aside. Is it the first 16 or the last 16 channels of the input tensor ?

### Consequence
1. When implementing a neural network containing a "split" operator, the split operation on an input tensor can be performed on the wrong axis et so it would give an incorrect result. 
2. After the split of tensor's channels, the next layer of the neural network could receive the wrong feature maps and not those expected from the correct channels. 

### Proposal
Define in the documentation a dictionary associating integers with axis of tensors. 
The onnx description should specify exactly how the axis of the input tensor is splited and indicate precisely where each of the outputs in the following layers of the network are used.


## Issue #2.2: Incomplete specification of CONCAT operator 

- CAT: Operator
- CRIT: High
- REQ:	(TBC)
- LOC: 	https://onnx.ai/onnx/operators/onnx__Concat.html

### Issue
1. The "axis" attribute gives an integer which defines the axis along which the n input tensors should be concatenated. The onnx documentation does not specify the correspondance between the integer and the axis of the tensor. In general, the "axis" attribute of the concat operator is set to 1, but which axis corresponds to 1 ? Does this mean that we must concatenate the channels of the input tensors, if "axis=1" corresponds to the channels ?
2. Moreover, the onnx description does not specify the order in which the input tensors are concatenated.

### Consequence
If the concatenation was done along the wrong axis of the input tensors or in the wrong order depending on the different input tensors, then the next layer of the network would give an incorrect result by applying its operation on the wrong feature maps. 

### Proposal
Define in the documentation a dictionary associating integers with axis of tensors. 
The onnx description should specify the order in which the input tensors are concatenated.

## Issue #2.3: Incomplete specification of RESIZE operator 

- CAT: Operator
- CRIT: High
- REQ:	(TBC)
- LOC: 	https://onnx.ai/onnx/operators/onnx__Resize.html

### Issue
1. The "scales" input gives a tensor which indicate the resize of each dimension. Each element of 'scales' corresponds to an axe of the input tensor. The onnx documentation indicates that the "scales" tensor takes value greater than 0. If it’s less than 1, it’s sampling down, otherwise, it’s upsampling. But the documentation does not specify the correspondance between the position of the element on the 'scales' tensor and the axe of the input tensor. Does the first element of the 'scales' tensor correspond to batch of the input tensor ? Does the second element of the 'scales' tensor correspond to the channels of the input tensor ? Does the third element of the 'scales' tensor correspond to the rows of the input tensor ? ... Moreover, if it's the value '2', we understand that the dimension of the corresponding axis is upsampling but by how much ? Does it mean that it is multiplied by 2 ?
2. The "nearest_mode" attribute indicates how to get “nearest” pixel in input tensor from x_original. There are 4 modes : "round_prefer_floor", "round_prefer_ceil", "floor", "ceil" but for no mode the documentation explains which operation applies to the tensor. What difference applies depending on the mode? 

### Consequence
The ouput tensor could be the incorrect shape with incorrect elements in the feature maps if the rescaling of the dimension was misunderstood. The operations of the next layers would be distorted. 

### Proposal
1. Specify the correspondance between the elements of the "scales" input and the axis of the input tensor to be resized.
2. Specify exactly the transformation applied to the input tensor depending on the assigned upsampling mode. Give an example of what the output tensor looks like from an input tensor for each of the modes


## Issue #2.4: Incomplete specification of RESHAPE operator 

- CAT: Operator
- CRIT: High
- REQ:	(TBC)
- LOC:  https://onnx.ai/onnx/operators/onnx__Reshape.html

### Issue
The "shape" input is a shape tensor which specifies the output shape. If one dimension of the new shape is -1, the value of the output dimension is inferred from the size of the input tensor and the remaining dimensions. Let's suppose an input tensor with size [1,c,l,w] and 'shape'=[1,c,-1], in this case where the shape of the output tensor is inferior to the shape of the input tensor, does it mean that we have to reorganize the matrix lxw of feature map into an unique row of size l*w in order to obtain an output tensor with the shape [1,c,l*w] ? And how are the rows of w columns organized on a single line ? Are they concatenated one after the other ? Is an order to be respected ? The onnx documentation does not specify exactly how the dimension '-1' transform the tensor to be reshaped. And vice versa, if shape of the output tensor > shape of the input tensor (input tensor's size = [1,c,L] and 'shape'=[1,c,l,w]), then how is the data from a row organized into matrices (L=l*w) ? The onnx documentation does not specify exactly how the data from the input tensor is reorganized. Moreover, the documentation does not specify the correspondance between the position of the element on the 'shape' tensor and the axe of the input tensor.

### Consequence
1. The output tensor may be incorrect if the input tensor was reshaped based on the wrong axes.
2. The output tensor may be incorrect if the reordering data in one dimension was done in the wrong order --> the operations of the next layers would be distorted. 

### Proposal
1. Specify the correspondance between the position of the element on the 'shape' tensor and the axe of the input tensor.
2. Specify exactly how the dimension '-1' transform the tensor to be reshaped.
3. Specify exactly how the data from the tensor is reorganized.


## Issue #2.5: Incomplete specification of SOFTMAX operator 

- CAT: Operator
- CRIT: High
- REQ:	(TBC)
- LOC: 	https://onnx.ai/onnx/operators/onnx__Softmax.html

### Issue
Softmax(input, axis) = Exp(input) / ReduceSum(Exp(input), axis=axis, keepdims=1)
The “axis” attribute indicates the dimension along which Softmax will be performed. But the onnx documentation does not specify the correspondance between the integer given to the "axis" attribute and the axe of the input tensor. If 'axis=1', does it mean that Softmax is performed along the channels of the input tensor ? 

### Consequence
The values of elements in the feature maps of the output tensor could be incorrect if the softmax was performed along the wrong axe of the input tensor. 

### Proposal
Specify in the documentation the correspondance between the integer given to the "axis" attribute and the axe of the input tensor.


## Issue #2.6 : Incomplete specification of SHAPE operator 

- CAT: Operator
- CRIT: High
- REQ:	(TBC)
- LOC: 	https://onnx.ai/onnx/operators/onnx__Shape.html

### Issue
The "shape" operator outputs an 1D tensor containing the shape of the input tensor. But the onnx documentation does not specify the correspondance between the dimension of the input tensor and the position of the element on the 'shape' output tensor. If the input was a tensor containing 16 channels of feature maps with size 80x80, what would the output tensor look like ? 'shape' = [16,80,80] ? Or the sizes of each dimension of the input tensor should be written to the output tensor in another order ? 

### Consequence
The output tensor could be incorrect if the implementation of the 'shape' operator did not list the dimensions of the input tensor in the correct order. 

### Proposal
1. Specify in the documentation the correspondance between the dimension of the input tensor and the position of the value on the 'shape' output tensor.
2. Note in the onnx file of description of the neural network the shape of the layer input as well as the layer output. 


## Issue #2.7 : Incomplete specification of SLICE operator 

- CAT: Operator 
- CRIT: High
- REQ:	(TBC)
- LOC: 	https://onnx.ai/onnx/operators/onnx__Slice.html

### Issue
The "axes" attribute gives an integer which defines the axis along which the input tensor should be sliced. The onnx documentation does not specify the correspondance between the integer and the axis of the tensor. 

### Consequence
When implementing a neural network containing a "slice" operator, the slice operation on an input tensor can be performed on the wrong axis et so it would give an incorrect result. 

### Proposal
Define in the documentation a dictionary associating integers with axis of tensors. 


## Issue #2.8: incomplete specification of CONV operator
- CAT: Operator
- CRI: HIGH
- REQ: (TBC)
- LOC: [CONV operator](https://onnx.ai/onnx/operators/onnx__Conv.html), but this issue appear in other operators

### Issue
The description of the CONV operator is very abstract: "The convolution operator consumes an input tensor and a filter, and computes the output.". 

The value of the padding is not defined (it is actually 0).

Presentation of attributes makes it difficult to check if all dependencies are expressed. 

### Consequence
Implementer needs to check the referece implementation (or other doc.) to understand what needs to be implemented. Different implementation may lead to different results.

### Proposal
See [example](https://github.com/ericjenn/working-groups/tree/ericjenn-srpwg-wg1/safety-related-profile/documents/conv_specification_example)
