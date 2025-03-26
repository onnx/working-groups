# Warning

**This is a draft.**

# Introduction

This document captures the requirements applicable to the SONNX profile. 

The specification is organized as follows:

- General requirements
- Requirements about the operators
- Requirements about the graph
- Requirement about the serialization format

# Operators

## General requirements

### REQ `OP 000`: `Compliance with the ONNX standard`

#### Description
The SONNX standard shall not modify the structure (inputs, outputs, attributes) of the ONNX operators). However, it is allowed to restrict the input and parameter domains if deemed necessary.

#### Rationale 
Compatibility with the ONNX standard. 

#### Related need
[TBC]

### REQ `OP 001`: `Operators set`

#### Description
The SONNX profile shall include the following operators:
> [TBC]: list to be established from the [list of use cases](./usecases.md). See also [Excel file](../meetings/reqs_sub_wg/ONNX_operators_for_Use_Cases.xlsx)
  
#### Rationale 
The set of operators included in the SONNX profile shall allow the implementation of simple industral use cases by the end of 2025.

#### Related need
[TBC]

### REQ `OP 002`: `I/O specification`

#### Description
For each operator in the SONNX operator set, the SONNX profile shall completely and precisely determine the expected values of the operator's outputs for any valid value of its inputs and attributes.\ 
A *valid* input (resp. attribute) is an input (resp. attribute) whose value comply with all preconditions (see [REQ XXX](#XXXX)).\
Depending on the operator, the expected value may be unique or not.\
In the latter case, the expected value may be a range of values, or a set of values satisfying some properties (post-condition). 

The expected value will preferably be defined by a mathematical relation between inputs, outputs, and attributes. 
Usual mathematical notations (i.e., notations that are commonly used by engineers) must be used preferably.

#### Rationale 
There shall be no room for interpretation or non determinism. 

#### Related need
[TBC]


### REQ `OP 003`: `Accuracy`

#### Description
The specification shall provide 
- the maximal acceptable error (upper bound) on the outputs
- or the inputs leading to the maximal error (the measurement of errors being left to the implementer).

The error may be expressed for each scalar or, on the matrix, vector, or tensor. In any case, the error metric must be clearly defined. 

#### Rationale 
If we say nothing about the accuracy of an operator, it basically mean that any output is correct.

Note: this can be considered as a specific case of requirement [req-op-002](#req-op-002-io-specification) about the operator's I/O relation. 

#### Related need
[TBC]

## Informal specification

### REQ `OP 010`: `Informal specification - structure`

#### Description
The SONNX profile shall describe each operator according to the same structure including:
- The operator's inputs and outputs
- The operator's attributes 
- The semantics of the operator using a mathematical notation possibly illustrated by figures when applicable.
- Any intermediate variable introduced for the sake of the specification must be defined explicitly.  
  
The description shall follow the example given for the `conv` operator.

#### Rationale 
Homogeneity, readability.

#### Related need
[TBC]

### REQ `OP 011`: `Consistency of notations`

#### Description
The SONNX profile shall use consistent notations for the description of all operators. 

The following conventions apply:
- Tensors are represented in uppercase (e.g., `X`,`B`,...)
- Attributes are represented in lowercase (`auto_pad`, `group`,...)
- The number of lines and columns of a 2-dimension tensor `T` are respectively denoted by $nl(T)$ and $nc(T)$ 
- The number of channels of a tensor `T` is denoted by $nch(T)$.

#### Rationale 
Homogeneity, readability.

#### Related need
[TBC]

### REQ `OP 012`: `Consistency of naming`

#### Description
The SONNX profile shall use consistent terms for the description of all operators:
- "kernel" (not "filter"), as in "convolution *kernel*"
- "spatial dimensions" (not "spatial *axes*")

*This list is to be completed.*

#### Rationale 
Consistency, radability.

#### Related need
[TBC]


### REQ `OP 013`: `Simplicity`

#### Description
The SONNX profile shall describe the operator semantics in the simplest and most intuitive way.\
In an algorithmic description is used, it shall be as straightforward as possibe with no 
fancy optimization (that are left to the implementer).

#### Rationale 
The specification shall be easy to understand and shall facilitate validation and verification activities.

#### Related need
[TBC]

### REQ `OP 014`: `No implementation prescription`

#### Description
The SONNX profile shall not prescribe implementation solutions.\
The relation between inputs and outputs may also be expressed by algorithm describing 
how inputs are processed to generate produce the outputs according to the attributes. 
In that case, the algorithm shall not be considered as a requirement on the implementation, 
but only as one possible way to compute the expected result.

#### Rationale 
SONX is a specification and shall not prescribe implementation. Should the model designer need to 
impose a specific implementation solution, this information shall be expressed in a specific meta-data (see [derived requirements](#derived_reqs)).

#### Related need
[TBC]

### REQ `OP 015`: `Restrictions wrt ONNX`

#### Description
The SONNX profile shall clearly indicate when a condition on the inputs, outputs, and attributes is a restriction 
with respect to the ONNX standard.

In that case, the condition must be maked with tag `[restrict]`.

#### Rationale 
Clarity.

#### Related need
[TBC]

### <a name="no_default_value"></a> REQ-OP-016: No default value

 No default values
#### Description
The SONNX profile shall forbid the use of default values.

#### Rationale 
The ONNX standard defines default value for attributes that are left without values. The objective is to ensure that the model designer and model implementer has a clear knowledge of the values involved in computations. 

#### Related need
[TBC]


### <a name="datatype_specific_spec"></a> REQ-OP-017: Datatype specific specification

#### Description
The SONNX standard shall 
- specify operators for values in the domain of real numbers ($R$), systematically
- specify operators for all domain necesary to support the industrrial use cases (e.g, `float32`and `int32`). 

For instance, the `conv` operator shall be specified for values in $R$,  `float32` and `int32` datatypes.

#### Rationale 
The semantics of the operator may depend on the types (float, integers), accurracy (float32, float64), range (int16, int32)of numbers. 

#### Related need
[TBC]

### <a name="input_domain"></a> REQ-OP-018: Input domain definition

#### Description
The SONNX profile shall specify all conditions on inputs and attributes that must be satisfied for the operator to be applicable. The behaviour of the operator for any value out of the valid input domain must be described.

#### Rationale 
The semantics of operators is only defined in the inputs and attribute validity domain.

#### Related need
[TBC]

### <a name="out_of_domain_errors"></a> REQ-OP-019: Out of domain errors

#### Description
The SONNX profile shall specify the behaviour of an operator should the input values be out of the input domain.

#### Rationale 
[TBC]

#### Related need
[need-ai-008](needs.md#need-ai-008-behavioral-determinism-and-predictability)

### <a name="over_and_underflows"></a> REQ-OP-020: Overflow and underflow conditions

#### Description
The SONNX profile shall specify the conditions leading to overflows and underflows.

#### Rationale 
[TBC]

#### Related need
[need-ai-008](needs.md#need-ai-008-behavioral-determinism-and-predictability)


### <a name="unique_conditions"> REQ-OP-021: Conditions stated once

#### Description
The SONNX profile shall ensure that, when a condition involves several inputs, outputs or attributes, 
it is only expressed once in the section dedicated to one of the inputs, outputs or attributes. 
Should the condition involve multiple inputs, outputs or attributes, references to the unique condition 
shall be used in all other sections.

#### Rationale
Prevention of inconsistencies. 

#### Related need
[TBC]

### <a name="operator_stability"></a> REQ-OP-022: Stability of operators

#### Description
The SONNX profile shall not include instable operators. If an unstable operator is absolutely required, the phenomenon must be described. 

#### Rationale
[TBC]

#### Related need
[need-ai-008](needs.md#need-ai-008-behavioral-determinism-and-predictability)


### <a name="determinism_memory_usage"></a> REQ-OP-023: Determinism of resource usage

#### Description
The SONNX profile shall not include operators which memory usage depend on input values.

#### Rationale
[TBC]

#### Related need
[need-ai-009](needs.md#need-ai-009-resource-usage-determinism-and-predictability)

### <a name="determinism_execution_time"></a>  REQ-OP-024: Determinism of execution times

#### Description
The SONNX profile shall not include operators which execution time depend on input values.

#### Rationale
[TBC]

#### Related need
[need-ai-010](needs.md#need-ai-010-execution-time-determinism-and-predictability)


## Formal specification

### <a name="formal_specification"></a> REQ-OP-030: Formal specification

#### Description
The SONNX profile shall provide a formal specification of each operator.

#### Rationale
The formal specification will be used to verify the correctness of the reference implementation.

#### Related need
[TBC]


### <a name="deterministic_operators"></a>  REQ-OP-032: Deterministic operators

#### Description
The profile shall not include non-deterministic operators. 

#### Rationale 
[TBC]


#### Related need
[TBC]


# Requirements on graph interpretation

### <a name="graph_specification"></a>  REQ-GR-000: Graph specification

#### Description
The profile shall specify the graph execution semantics.

#### Rationale 

#### Related need
[TBC]

# Requirements on file format

## General requirements

### <a name="operator_versions"></a> REQ-FO-000: Operator versions

#### Description
The model shall indicate precisely the version of each operator used in the model.

#### Rationale 
Operators may have several versions (opset) and, during graph execution, the shall be no ambiguity about the version to be used.

#### Related need
[need-thav-001](needs.md#need-thav-001-version-index-in-the-onnx-model)

### <a name="parameter_representation"></a> REQ-FO-001: Representation of parameters

#### Description
The model shall not degrade the accuracy of the parameters (weights, biases, etc.). For instance, the IEEE hexadecimal binary representation may be used to represent floating point parameters ([-]0x1.abcdefp[+-]n) .  

#### Rationale 
The serialization of floating point number must not introduce degrade the accuracy of the source model parameters. 

#### Related need
[TBC]

## User documentation

### <a name="io_documentation"></a>  REQ-FO-010: Documentation of input and output tensors

#### Description
The SONNX profile shall have the capability to describe 
- the semantics of the input and output tensors, 
- the semantics of the dimensions of the tensors.

#### Rationale 
[TBC]

#### Related need
[need-arcys-001](needs.md#need-arcys-001-final-prediction)

### <a name="implementation"></a>  REQ-FO-011: Derived requirements - implementation

#### Description
The SONNX profile shall have the capability to describe how the model must be deployed on a specific target, i.e.,
- the exact order in which the graph operators must be executed
- the target hardware on which the model or part of the model must be deployed.


#### Rationale 
[TBC]

#### Related need
[need-ai-003](needs.md#need-ai-003-expression-of-implementation-requirements)

### <a name="traceability_to_training_model"></a>  REQ-FO-012: Traceability to training model

[TBDis]

#### Description
The SONNX profile must provide the capability to trace the ONNX model to the training model from which it has been generated. 

#### Rationale 
[TBC]

#### Related need
[need-ai-004](needs.md#need-ai-004-support-for-traceability)


### <a name="traceability_to_training_env"></a> REQ-FO-013: Traceability to training environment

[TBDis]

#### Description
The SONNX profile must provide the capability to trace the environment used for training.

#### Rationale 

#### Related need
[need-ai-004](needs.md#need-ai-004-support-for-traceability)


# Model validity

### <a name="valid_operators"></a>  REQ-VA-000: Valid operator set

#### Description
A model shall only use operators in the SONNX set.

#### Rationale 
[TBC]

#### Related need
[TBC]

### <a name="explicit_types_shapes"></a>  REQ-VA-001: Explicit types and shapes

#### Description
All datatypes must be indicated explicity (no type inference).\
All shape conversion must be done explicity (using the `reshape`) operator. (no [shape inference](https://onnx.ai/onnx/api/shape_inference.html))

#### Rationale 
[TBC]

#### Related need
[need-thav-002](needs.md#need-thav-002-typing-of-data-handled-by-implementation-operators)


# Reference implementation

### <a name="reference_imp"></a>  REQ-RI-000: Reference implementation

#### Description
The SONNX profile shall provide a reference implementation covering 
- the operator set
- the graph execution
- the graph import (deserialization of a SONNX model)

#### Rationale
In order to verify the correctness of his/her implementation, the user will need to compare the results computed by this implementation with some reference. Since we nned to compare computation **results**, this means that the specification must be executable. One possible way could be to use an executable formal specification (e.g., `why3`). Another way consists to provide (i) a formal specification and (ii) a "reference" implementation demonstrated to comply with the formal specification. 

#### Related need
[need-ai-011](needs.md#need-ai-011-support-for-verification-activities)

### <a name="reference_imp"></a>  REQ-RI-001: Relation with specification

#### Description
The reference implementation shall be traceable to the specification either by review or by generation. In particular, the reference implementation must reproduce the structure of the mathematical specification, without introducing implementation optimizations.

#### Rationale
Verifying the reference implementation must be as easy as possible. 

#### Related need
[TBC]

# Tooling

### <a name="verification_tool"></a>  REQ-TO-000: Verification tool

#### Description
The SONNX profile shall provide a model verification tool.\
This tool aims at verifying that all validity conditions are satisfied, including:
- the graph structure is well-formed,
- all required metadata are present
- operators are allowed
- all conditions involving operators inputs, outputs and parameters are satisfied

#### Rationale
[TBC]

#### Related need
[need-ai-007](needs.md#need-ai-007-support-for-model-verification)