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

### Consequence
(TBC)

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
[QuantizeLinear](https://onnx.ai/onnx/operators/onnx__QuantizeLinear.html) is able to output int16, uint16, but [QLinearMatMul](https://onnx.ai/onnx/operators/onnx__QLinearMatMul.html) and [QLinearConv](https://onnx.ai/onnx/operators/onnx__QLinearConv.html) do not support these types.
