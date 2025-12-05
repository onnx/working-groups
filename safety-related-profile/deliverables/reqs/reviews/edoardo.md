# Introduction

This document captures the requirements applicable to the SONNX profile. 

The specification is organized as follows:

- General requirements
- Requirements about the operators
- Requirements about the graph
- Requirement about the serialization format

> **_NOTE:_**  General requirements are presented later in the document. Move them here at the beginning. Perhaps create also a list by collating general operator, graph and serialization-specific requirements?
> OK: moved.

## General requirements

> **_NOTE:_** Move the general requirements section to the top. It will act as a good introduction to the requirements. \
> OK: Done

### Documentation

The documentation of the SONNX profile is composed of two parts: 
- a documentary part, used to document the operator semantics
- a formal part, used to specify the exact behaviour of the operator.  

The documentary part shall not be considered to be a formal specification. For an exact and precise specification of an operator, the user shall refer to the formal specification.  

> **_NOTE:_** This section is a bit "meta". Shall we move it to the top of the document? It would work great under "general requirements".\
> OK: moved

### <a name="documentation_structure"></a>  REQ-DO-010: Documentation structure

#### Description
The SONNX profile shall describe each operator according to the following structure:
- a summary of the restrictions applicable to the operator
- the signature of the operator
- the inputs, attributes and output of the operator 
- a documentation about the semantics of the operator, which may include illustrations, code samples, etc.
- a formal specification of the operator semantics written in Why3

#### Rationale 
Homogeneity, readability.

#### Related need
[TBC]

### <a name="notation_consistency"></a> REQ-DO-020: Notation consistency

#### Description
The SONNX profile shall use consistent notations for the description of all operators. 

#### Rationale 
Homogeneity, readability.

#### Notes
SONNX may provide a set of standard notations to be used in the documentation. 

For instance, the following conventions may be applied:
- Tensors are represented in uppercase (e.g., `X`,`B`,...)
- Attributes are represented in lowercase (`auto_pad`, `group`,...)
- The number of lines and columns of a 2-dimension tensor `T` are respectively denoted by $nl(T)$ and $nc(T)$ 
- The number of channels of a tensor `T` is denoted by $nch(T)$.

#### Related need
[TBC]

### <a name="naming_consistency"></a> REQ-DO-030: Naming consistency

#### Description
The SONNX profile shall use consistent terms for the description of all operators.

#### Rationale 
Consistency, readability.

#### Notes
SONNX may provide a set of standard terms to be used in the documentation. 

For instance:
- "kernel" (not "filter"), as in "convolution *kernel*"
- "spatial dimensions" (not "spatial *axes*")
- etc.

#### Related need
[TBC]

### <a name="simplicity"></a> REQ-DO-040: Simplicity

#### Description
In the documentation part, the SONNX profile shall describe the operator semantics in the simplest and most intuitive way.\
It shall be as close as possible to the standard mathematical description of the operator, without optimization (those are left to the implementer).

> **_NOTE:_** This is very important, yet very difficult to define. I can already see some future discussion about what "simplicity" means... Ideas to improve: add a reference style such as "understandable by anyone with a STEM undergraduate/anyone who can implement a neural network in PyTorch", "in a similar style of the MatLab/TensorFlow documentation", etc.\
> ??: I fully agree with you. This is not really a "requirement", but we don need to say something about it. I don't really like the reference to "STEM undergraduate or someone who can implement...". Another way can be to define a set of basic constructs / math operations and require all specs to be build using these elements. This would not prevent specifications to be  written in a convoluted way (for instance, an optimized way)... Rather than a req, this could simply be a recommendation. It will be up to the reviewer of the operator spec to determine whether or not it must be rewritten or not...  
> Final: Change this "req" a "reco" 

#### Rationale 
The documentation shall be easy to understand and shall facilitate validation and verification activities.

#### Related need
[TBC]

### <a name="imp_prescription"></a> REQ-DO-050: No implementation prescription

#### Description
The SONNX profile shall not mandate specific implementation solutions. However, if a particular implementation is to be preferred in practice, the specification shall define the properties that such an implementation satisfies. 

#### Rationale 
SONNX is a specification and shall not prescribe implementation. Should the model designer need to impose a specific implementation solution, this information will be expressed using specific meta-data (see [derived requirements](#derived_reqs)).

#### Notes
The relation between inputs and outputs may also be expressed by algorithm describing 
how inputs are processed to generate produce the outputs according to the attributes. 
In that case, the algorithm shall not be considered as a requirement on the implementation, 
but only as one possible way to compute the expected result.

#### Related need
[TBC]


### <a name="unique_conditions"></a> REQ-DO-060: Conditions stated once

#### Description
The SONNX profile shall ensure that, when a condition involves several inputs, outputs or attributes, it is only expressed once in the section dedicated to one of the inputs, outputs or attributes. Should the condition involve multiple inputs, outputs or attributes, references (hyperlinks) to the unique condition shall be used in all other sections.

For instance, if the values of two scalar inputs `A` and `B` are such that `A` > `B` , there shall  be one constraint C applicable to `A` stating that `A` > `B`, and one constraint applicable to `B` referencing constraint C. 


> **_NOTE:_** I can guess what this mean (and I agree with it), but an example would help clarify.\
> OK: Done
> => change the example in a "negative" way.

#### Rationale
Prevention of inconsistencies. 

#### Related need
[TBC]

## Formal specification

### <a name="formal_specification"></a> REQ-FS-000: Formal specification

#### Description
The SONNX profile shall provide a formal specification of each operator.


#### Rationale
The formal specification uses a formal language with a well-defined and sound semantics that shows none of the potential ambiguities of the informal specification operators used in the documentary part. In particular, the formal specification can be used to prove the correctness of an implementation or be used as a test oracle.

> **_NOTE:_** Potential inconsistency with the requirement that we do not enforce a specific implementation. Maybe clarify that we only enforce a number of _properties_ of the implementation (invariants?), which are listed in the formal specification.\
> OK: I have reworded the rationale. I see no reference to the implementation...
> => OK

#### Related need
[TBC]

### <a name="formal_spec_traceability"></a> REQ-FS-010: Formal specification traceability

#### Description
The formal specification must be traceable to the documentation, i.e., the elements of the formal specification shall refer to the sections and or paragraphs of the documentary part. 


> **_NOTE:_** Define exact meaning of "traceability"\
> > OK: defined. 
> => OK

#### Rationale
The formal specification of an operator perfectly defines it, but the semantics so expressed may not reflect the operator designer intent. Having an explicit link between the formal specification and its informal counterpart is one way (i) to prevent errors (both specifications are redundant to some extent) and (ii) to enforce the formal specification to remain "simple". 

#### Related need
[TBC]


### <a name="operator_versions"></a> REQ-FO-020: Operator versions

#### Description
The model shall indicate precisely the version of each operator used in the model.

#### Rationale 
Operators may have several versions (opset) and, during graph execution, the shall be no ambiguity about the version to be used.

#### Related need
[need-thav-001](needs.md#need-thav-001-version-index-in-the-onnx-model)


### <a name="parameter_representation"></a> REQ-FO-030: Representation of parameters

#### Description
The model shall shall specify all parameters down to the least significant bit and in a non-ambiguous way. For instance, the IEEE hexadecimal binary representation may be used to represent floating point parameters ([-]0x1.abcdefp[+-]n) .  

> **_NOTE:_** Rephrase in positive: e.g. "the model shall specify all parameters down to the least significant bit and in a non-ambiguous way". I like the hexadecimal representation for IEEE754 floats.\
> OK: done
> => OK

#### Rationale 
The serialization of floating point number must not degrade the accuracy of the source model parameters. 

#### Related need
[TBC]

### <a name="io_documentation"></a>  REQ-FO-040: Documentation of input and output tensors

#### Description
The SONNX file format shall have the capability to describe 
- the semantics of the input and output tensors, 
- the semantics of the dimensions of the tensors.

#### Rationale 
[TBC]

#### Related need
[need-arcys-001](needs.md#need-arcys-001-final-prediction)

### <a name="implementation"></a>  REQ-FO-050: Derived requirements - implementation

#### Description
The SONNX profile shall have the capability to describe how the model must be deployed on a specific target, i.e.,
- the exact order in which the graph operators must be executed
- the target hardware on which the model or part of the model must be deployed.

> **_NOTE:_** This is ambitious. I get how it may be useful to guarantee deterministic behaviour. But "target hardware" may be split into different levels of abstraction, e.g. "any GPU" vs "that specific model of GPU running that specific version of CUDA".\
> ??: I am really wondering if this req has to be kept... Note that the req makes no assumption about the target, it only states that there shall be a way to specify the exact order in which operations (as defined in the model) are to be computed. The main question is: is it useful? is it necessary?
> => Simply provide the capability to add meta-data in the model. Check whether they exist or not.

#### Rationale 
[TBC]

#### Related need
[need-ai-003](needs.md#need-ai-003-expression-of-implementation-requirements)


# Operators


## Operator set


### <a name="deterministic_operators"></a>  REQ-OP-010: Deterministic operators

#### Description
The profile shall only include functional operators, or restriction shall be expressed to ensure that the operator will behave as a function during inference. 

A functional operator is an operator that maps one input value to one and only one output value. For instance, the ONNX ``dropout`` operator with ``training_mode`` set to ``true`` performs a random dropout that is not functional. A functional behaviour may be achieved by restricting the use of the operator, for instance, by enforcing input ``training_mode`` to be set to false. Operator ``RandomUniform`` is another example: if the seed input is set to some fixed value, the operator becomes functional. Checking that the input value may be done by a dedicated tool. 

> **_NOTE:_** Add examples to clarify? E.g. drop-out layers. Clarify whether the requirement extends to the _implementation_ of the operator: parallel computing in floating-point is non deterministic.
> ??: I have rewritten the req in a positive way. I have added examples. I have used the term "functional" rather than "deterministic". 
=> OK

#### Rationale 
A graph must be deterministic. 

#### Related need
[need-ai-008](needs.md#need-ai-008-behavioral-determinism-and-predictability)

### <a name="operator_set"></a> REQ OP 000: Operator set

#### Description
The SONNX profile shall include at least the following operators:


| Operator                     |
|------------------------------|
| Abs                          |
| Add                          |
| Cast                         |
| Clip                         |
| Concat                       |
| Constant                     |
| ConstantOfShape              |
| Conv                         |
| ConvTranspose                |
| Dense                        |
| Div                          |
| Equal                        |
| Erf                          |
| Exp                          |
| Expand                       |
| Flatten                      |
| FullyConnected               |
| Gather                       |
| Gemm                         |
| GlobalAveragePool            |
| GRU                          |
| HardSwish                    |
| Identity                     |
| LeakyRelu                    |
| Less                         |
| Log                          |
| LSTM                         |
| MatMul                       |
| Max                          |
| MaxPool                      |
| Min                          |
| Mod                          |
| Mul                          |
| Neg                          |
| Not                          |
| Pad                          |
| Padding                      |
| Pow                          |
| Range                        |
| ReduceMean                   |
| ReduceSum                    |
| Relu                         |
| Reshape                      |
| Resize                       |
| ScatterND                    |
| Shape                        |
| Sigmoid                      |
| Slice                        |
| Softmax                      |
| SoftPlus                     |
| Split                        |
| Sqrt                         |
| Squeeze                      |
| Sub                          |
| Tanh                         |
| Transpose                    |
| ConvTransposeDeconvolution   |
| Unsqueeze                    |
| Where                        |


#### Rationale 
The SONNX profile does not cover the complete set of ONNX operators. It is limited to operators (i) used during inference, (ii) that do not undermine determinism and predictability, (iii) used in a first set of industrial [use cases](../../scope/scope.md). This set may be later extended depending on the needs. 

> **_NOTE:_** "inference", "determinism", "predictability", "use cases" should be defined before being used as a justification.
> ??:  Note that this text is not part of the specification. I have introduced the requirement about determinism before. The concept of "inference" is well-known and I don't think that it deserves a definition (to be discussed). 
> => Inference to be defined (lexicon to be added)

> **_NOTE:_**  We should list the use cases (with references) if possible. That will give the reader a better idea of the scope.

#### Related need
[TBC]



### <a name="inference_operators"></a>  REQ-OP-020: Inference operators

#### Description
The profile shall only include operators used during inference.

#### Rationale 
SONNX is only concerned with inference. 

> **_NOTE:_** Is "inference" clear enough? Can we define it as "all numerical parameters in the graph are constant" or something like that?
> OK/ modified as proposed.
> => Modify the rationale ("dead code").

#### Related need
[TBC]

#### Related need
[need-ai-009](needs.md#need-ai-009-resource-usage-determinism-and-predictability)


### <a name="compliance_with_onnx"></a> REQ-OP-030: Compliance with the ONNX standard

#### Description
The SONNX version of an operator `op` shall have the same inputs, outputs, and attributes than the ONNX `op` operator. 

However, it is allowed to restrict the inputs and parameters value domains if deemed necessary.

> **_NOTE:_** CHange "ranges" to "values"?\
> ?? : "ranges" => "domains"
> => OK

#### Rationale 
Compatibility with the ONNX standard. 

#### Related need
[TBC]

### <a name="restrictions"></a> REQ-OP-060: Restrictions wrt ONNX

#### Description
The SONNX profile shall clearly indicate when a condition on the inputs, outputs, and attributes is a restriction with respect to the ONNX standard.

In that case, the condition must be marked with tag `[restrict]`.

> **_NOTE:_** Move this requirement closer to requirement "compliance with the ONNX standard" as they are related?\
> OK: moved
> => OK

#### Rationale 
Clarity.

#### Related need
[TBC]


## Operator specification

### <a name="domain_spec"></a> REQ-OP-030: Input domain specification

#### Description
For each operator in the SONNX operator set, the SONNX profile shall specify the validity domain of inputs and attributes.

#### Rationale 
There shall be no room for interpretation or non determinism. 

#### Related need
[TBC]

### <a name="function_spec"></a> REQ-OP-030: Operator specification

#### Description
For each operator in the SONNX operator set, the SONNX profile shall specify the expected output values for any input values and attributes in their validity domain.

The SONNX standard shall specify operators for values in the domain of real numbers ($R$) and in all domains necessary to support the industrial use cases (e.g, `float32`and `int32`). 

For instance, the `conv` operator shall be specified for values in $R$,  `float32` and `int32` datatypes.

> **_NOTE:_** Again, I'm not against the use of qualifiers such as "systematically", but we should give a definition of their meaning at the beginning of the document.\
> OK: I have simply removed "systematically that was not required here. I have also suppressed the dedicated req and merged it with the one concerning ht operator specification
> => OK.

#### Rationale 
The semantics of the operator may depend on the types (float, integers), accuracy (float32, float64) and range (int16, int32) of numbers. 

#### Related need
[TBC]

> **_NOTE:_** Very nice! Do we want to introduce some specific language at the beginning of the document, like in legal documents? E.g. by "completely and specific" we mean... Also, there are multiple requirements named REQ-OP-030. \
> ??: (i) I think that we can remove "completely" and "precisely" that brings no useful information > - requirements will be renumbered in a second phase.
> => OK

#### Rationale 
There shall be no room for interpretation or non determinism. 

#### Related need
[TBC]

### <a name="out_of_domain_errors"></a> REQ-OP-040: Out of domain errors

#### Description
The SONNX profile shall specify the behaviour of an operator should some input value be out of its validity domain.

#### Rationale 
Out of domain conditions may not be prevented by design, checked statically or detected at runtime.  
For attributes, a static verification of the model is expected to be carried out in order to prevent such error conditions.

#### Related need
[need-ai-008](needs.md#need-ai-008-behavioral-determinism-and-predictability)

### <a name="over_and_underflows"></a> REQ-OP-050: Overflow and underflow conditions

#### Description
The SONNX profile shall specify the conditions leading to overflows, underflows, wrap-around.

#### Rationale 
[TBC]

#### Related need
[need-ai-008](needs.md#need-ai-008-behavioral-determinism-and-predictability)


### <a name="no_default_value"></a> REQ-OP-070: No default value

 #### Description
The SONNX profile shall forbid the use of default values.

#### Rationale 
The ONNX standard defines default value for attributes that are left without values. The objective is to ensure that the model designer and model implementer has a clear knowledge of the values involved in computations. 

#### Related need
[TBC]



# Requirements on graph

### <a name="graph_specification"></a>  REQ-GR-000: Graph specification

#### Description
The profile shall specify the graph execution semantics.

#### Rationale 
A model is a graph of operators. The semantics of the graph defines how operators are applied to generate the graph outputs out of its inputs.

> **_NOTE:_** Missing: what is a node, what is an edge, is it a DAG, etc.
> => See if we put it before ops. 

#### Related need
[TBC]

### <a name="explicit_types_shapes"></a>  REQ-GR-000: Explicit types and shapes

#### Description
All numerical types must be indicated explicitly (no type inference).\
All shape conversion must be done explicitly (using the `reshape`) operator. (no [shape inference](https://onnx.ai/onnx/api/shape_inference.html))

> **_NOTE:_** If we enforce consistent input/output shapes (types), then the latter requirement is redundant. We could keep it as an example?
> OK: chenged "datatypes" to numerical types (because in formal "theory" a "type" also covers the structure...)

#### Rationale 
[TBC]

#### Related need
[need-thav-002](needs.md#need-thav-002-typing-of-data-handled-by-implementation-operators)


# Requirements on file format

### <a name="format_compatibility"></a> REQ-FO-000: Compatibility with ONNX

#### Description
Any model compliant with the SONNX file format shall be a correct ONNX model.

#### Rationale 
Compliance with ONNX.

#### Related need
[TBC]

### <a name="format_completeness"></a> REQ-FO-010: Format completeness

#### Description
The SONNX file format specification shall ensure that a model expressed in this format can be implemented without requiring any additional information.

#### Rationale 
A SONNX model must be completely determined, leaving no room to interpretation.

> **_NOTE:_** Slight ambiguity here. We do not mandate a specific implementation, thus a single SONNX model accepts multiple implementations, i.e. there _is_ room for interpretation. Can we reformulate this in a better way? "sufficient number of properties"?
> => To be rephrased... 

#### Related need
[TBC]


# Reference implementation

### <a name="reference_imp"></a>  REQ-RI-000: Reference implementation

#### Description
The SONNX profile shall provide a reference implementation covering 
- the operator set
- the graph execution
- the graph import (deserialization of a SONNX model)

#### Rationale
In order to verify the correctness of his/her implementation, the user will need to compare the results computed by this implementation with some reference. Since we need to compare computation **results**, this means that the specification must be executable. One possible way could be to use an executable formal specification (e.g., `why3`). Another way consists to provide (i) a formal specification and (ii) a "reference" implementation demonstrated to comply with the formal specification. 

#### Related need
[need-ai-011](needs.md#need-ai-011-support-for-verification-activities)

### <a name="reference_imp"></a>  REQ-RI-010: Relation with specification

#### Description
The reference implementation satisfies all the properties of the SONNX specification, i.e. it is compliant to SONNX, and it is written in the most plain and clear style possible (no optimisations).

> **_NOTE:_** Again, I understand the spirit of the requirement -> make the implementation as "vanilla" as possible. However, I wonder whether we can say something as "the reference implementation satisfies all the properties of the SONNX specification, i.e. it is compliant to SONNX, and it is written in the most plain and clear style possible (no optimisations)". Just to stress that there are two separate requirements: (1) correctness/adherence to SONNX and (2) simple and easy-to-read style.
> => change to recommandation and use Edoardo's sentence.

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
- all conditions involving attributes are satisfied

> **_NOTE:_** Do we need to add "is executable" as one of the conditions (well-formedness)? Also, the latter condition needs to be split into (1) conditions related to input/output/parameter _types_ are satisfied and (2) conditions related to input/output/parameter _values_ are satisfied. The conditions on values may not be trivial to verify at all, especially if they depend on very specific execution traces (e.g. proving an operator input is always positive is an NP-Hard problem).
> => Check if conditions that can be verified only cobncer attributes (and not values). Check also the case of dimensions... 

#### Rationale
[TBC]

#### Related need
[need-ai-007](needs.md#need-ai-007-support-for-model-verification)


# TO BE DISCUSSED

> **_NOTE:_** These are not bad ideas, but they are very ambiguous.
> => Ceck if we keep some of them as recos.

### <a name="operator_stability"></a> REQ-OP-022: Stability of operators

#### Description
The SONNX profile shall not include numerically unstable operators. If such an unstable operator is required, the instability phenomenon shall be fully characterized

#### Rationale
[TBC]

#### Related need
[need-ai-008](needs.md#need-ai-008-behavioral-determinism-and-predictability)


### <a name="determinism_memory_usage"></a> REQ-OP-023: Determinism of resource usage

#### Description
The SONNX profile shall only include operators which memory usage does not depend on input values.

#### Rationale
[TBC]

### <a name="determinism_execution_time"></a>  REQ-OP-030: Determinism of execution times

#### Description
The SONNX profile shall not include operators which execution time depend on input values.

#### Rationale
[TBC]

#### Related need
[need-ai-010](needs.md#need-ai-010-execution-time-determinism-and-predictability)

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

