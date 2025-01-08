# ONNX analysis 

## Issue #TEMPLATE: Title of the issue

- CAT: category in {__OPERATOR__ , __GRAPH__ , __FORMAT__}
- CRIT: criticality in { __LOW__  , __HIGH__ }
- REQ:	_Identification of the SONNX requirement that can't be satisfied due to this issue_
- LOC: 	__Identification of the exact location in the standard, possibly using an hyperlink__

### Issue
__Description of the issue (in a synthetic way)__

### Consequence
__Brief description of the effect the issue on the development activities.__

### Proposal
__Proposal to solve the issue or mitigate the consequences__

### Remarks (opt)
__Additional remarks__


## Issue #1: incomplete specification of CONV operator
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

## Issue #2: Execution order of graph nodes
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

## Issue #3: Overloading

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


## Issue #4: opset resolution

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


## Issue #4: Function polymorphism

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

## Issue #5: Shape broadcasting

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

## Issue #6: Overloading

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


## Issue #7: Variadic inputs

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

## Issue #8: Dynamic (Node input) vs static (Node attribute)

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


## Issue #9: Data storage

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

## Issue #10: Quantization consistency

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


## Issue #11: Incomplete specification of SPLIT operator

- CAT: Operator
- CRIT: High
- REQ:	(TBC)
- LOC: https://onnx.ai/onnx/operators/onnx__Split.html

### Issue
1. The "axis" attribute gives an integer to define the axis along which split the input tensor into a list of tensors. The onnx documentation does not specify the correspondance between the integer and the axis of the tensor. Is the following interpretation the correct representation ? : 
- axis = '0' <=> batch ?
- axis = '1' <=> channels ?
- axis = '2' <=> lines ?
- axis = '3' <=> columns ?

2. Moreover, the "split" input gives a tensor which indicate the length of the 'axis' specified for each output tensor. For example, if the shape of the input tensor is [1,32,320,320] (assuming 32=channels, 320=lines and 320=columns) and the "split" input is [16,16] with the "axis" attribute = 1, then the operator splits the input tensor into two output tensors [1,16,320,320] and [1,16,320,320]. In general, the next layer of the network applies its operation on one of the two output tensors and the other one is kept for use in a deeper layer of the network. But the documentation does not specify which 16 channels are used in the next layer and which 16 channels are set aside. Is it the first 16 or the last 16 channels of the input tensor ?

### Consequence
1. When implementing a neural network containing a "split" operator, the split operation on an input tensor can be performed on the wrong axis et so it would give an incorrect result. 
2. After the split of tensor's channels, the next layer of the neural network could receive the wrong feature maps and not those expected from the correct channels. 

### Proposal
Define in the documentation a dictionary associating integers with axis of tensors. 
The onnx description should specify exactly how the axis of the input tensor is splited and indicate precisely where each of the outputs in the following layers of the network are used.


## Issue #12: Incomplete specification of CONCAT operator 

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


## Issue #13: Incomplete specification of RESIZE operator 

- CAT: Operator
- CRIT: High
- REQ:	(TBC)
- LOC: 	https://onnx.ai/onnx/operators/onnx__Resize.html

### Issue
1. The "scales" input gives a tensor which indicate the resize of each dimension. Each element of 'scales' corresponds to an axe of the input tensor. The onnx documentation indicates that the "scales" tensor takes value greater than 0. If it’s less than 1, it’s sampling down, otherwise, it’s upsampling. But the documentation does not specify the correspondance between the position of the element on the 'scales' tensor and the axe of the input tensor. Does the first element of the 'scales' tensor correspond to batch of the input tensor ? Does the second element of the 'scales' tensor correspond to the channels of the input tensor ? Does the third element of the 'scales' tensor correspond to the lines of the input tensor ? ... Moreover, if it's the value '2', we understand that the dimension of the corresponding axis is upsampling but by how much ? Does it mean that it is multiplied by 2 ?
2. The "nearest_mode" attribute indicates how to get “nearest” pixel in input tensor from x_original. There are 4 modes : "round_prefer_floor", "round_prefer_ceil", "floor", "ceil" but for no mode the documentation explains which operation applies to the tensor. What difference applies depending on the mode? 

### Consequence
(TBC)

### Proposal
1. Specify the correspondance between the elements of the "scales" input and the axis of the input tensor to be resized.
2. Specify exactly the transformation applied to the input tensor depending on the assigned upsampling mode. Give an example of what the output tensor looks like from an input tensor for each of the modes
