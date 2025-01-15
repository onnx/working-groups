# Introduction

This document capture the needs of the users of the ONNX model. By _users_, we mean both people generating the model and  using it during the early verification and validation phases (before implementation), and those of people using the model during the implementation, and late verificaton and validation phases. 

**A need must refer to some activity / goal that a SONNX user must do / achieve. The expression of a need should be of the form: "The `<role>` needs `<something>` to do `<something>`."  For instance, "The ML model developer needs a non-ambiguous description of each operator in order to build a model." or "The ML model implementer needs a non-ambogiguous description of the model operator and execution logic in order to implement the model.", etc.**

**A requirement expresses what SONNX must provide with for the user to do his/her activity.

# Recommendations

## Approach

Here are a few questions that you may ask yourself when trying to identify your needs:
- Properties
  - What are the properties verified on the ONNX model? Robustness? fairness? other?
  - What properties do you want to preserve during the model implementation?
- Derived requirements 
  - Do you have specific needs in terms of implementation that coud determine some SONNX feature?
  - Do you have specific needs about the traceability between the implementation of the model and the model? 
External needs  
  - Do you have to provide some specific evidences to some regularoty body? 
  - Do you have to demonstrate compliace with some specific standard?
- Verification
  - What are the verification activities to be done on the model? Formal verification? Manual review? other 
  - How do you plan to verify the implementation of the model? 
    - Do you plan to test it? (for what proprty)
    - Do you plan to use formal verification techniques and tools (and for what property)?
- Model transformation
  - Do you plan to use the model to generate code? using some automated tool? manually?
- Instrumentation 
  - Do you plan to instrument the implementation of the model? at what level?

## Template

### NEED `<ID>`: `<TITLE>`
#### Description
_Brief description of the need_.
#### Rationale (optional) 
If necessary, a _brief justification of the need_ 
#### Analysis
Analysis of the need. The objective is to determine whether it leads to a requirement for the SONNX profile or not. 

# GENERAL needs

(To be completed.)

# THAV needs

### NEED THAV-000: Capability to Embed Compatible ONNX Models in Avionic Databases with a DO200 Process
#### Description
There is a need for a format consistency checker for ONNX format itself not only operator to ensure that ONNX models can be integrated into avionic databases in compliance with the DO200 process.
#### Analysis
[TBC]

> [TODO] Clarify the relationship between the DO200 (applicable to avionics databases) and the MLMD.

### NEED THAV-001: Version Index in the ONNX Model
#### Description
The ONNX model must include a version index to indicate the compatibility of the ONNX format version with a particular version of an ONNX execution engine.
#### Analysis
[TBC]

### NEED THAV-002: Typing of Data Handled by Implementation Operators
#### Description
There is a need to know the typing of data handled by implementation operators, whether they are float or int (32-bit/16-bit/8-bit), bool (8-bit/32-bit), or text string size max, and to specify which representation is used (ASCII, UTF8, UTF16, Unicode) as well as the support for accented characters.
#### Analysis
[TBC]

### NEED THAV-003: Support for Dynamic Sizing of Input/Output Arrays in ONNX Format
#### Description
There is a need to determine whether the ONNX format should support dynamic sizing of input/output arrays (often used for batch size). It is necessary to check if we should limit this to purely static sizes or allow dynamic sizing to be possible.
#### Rationale
This need ensures flexibility in handling input/output dimensions within ONNX models, which is particularly important for optimizing batch processing and other dynamic use cases. These needs ensure that ONNX models can be reliably and compatibly integrated and used in avionic environments and other critical systems.
#### Analysis
The batch size could actually be considered as an implementation choice rather than a design choice since it does not modify the computed values.  
> [TODO] Need to be discussed.

# AIRBUS needs

### NEED `AI-000`: `Compliance with ARP6983, EASA Concept Paper`
#### Description
The development of Machine Learning constituents in avionics needs to comply with the ARP6983 regulation document and other documents produced by Certification Authorities (e.g., EASA Concept Paper). The Safety-related ONNX profile (SONNX) shall constitute a language in which the Machine Learning Model Description (MLMD), as defined by ARP6983, can be expressed.

The SONNX Safety-related profile shall allow the specification of the replication criterion, exact or approximate, that the implementation must ensure.

#### Rationale 
The MLMD must exist as defined by the ARP6983 document. It shall be the pivot between the trained model and the implementation for embedded inference, which is the basic aim of ONNX. The ARP6983 document requires that a replication criterion be defined in the MLMD, which constitutes a strong constraint applying to the implementation from the MLMD.

#### Analysis
[TBC]

### NEED `AI-001`: `Accurate and Precise Trained Model Description`

#### Description
We need an ML description "language" with a well-defined syntax and semantics enabling one to produce an accurate, precise a consistent description of the ML model, leaving no room to interpretation nor unspecified approximations.
This concerns in particular
- the operators
- the graph structure (i.e., the structure of interconnected operators)
- the graph parameters (i.e., the weights, biases, activation thresholds)
- the description of the semantics of the graph and all elements of the graph. 

#### Rationale
Safety-related systems require the demonstration that the ML model implementation process preserves the safety/functional/operational properties of the model developed during the design process.

#### Analysis
[TBC]

### NEED `AI-002`: `Expression of High Level Requirement`

#### Description
The model implementer needs High Level requirements about the model performance.\
Those requirements may concern:
- the ML performance, which measurement metric may depend on the task performed by the model (e.g., Mean Squared error or Mean Absolute error for regression tasks, or precision or accuracy for classification tasks)
- the numerical accuracy measured at the output of the model or at intermediate stages (e.g, all activations, activations at a certain layer, etc.), and specific inputs (reference dataset).

#### Analysis
[TBC]

> Shall it be part of the MLMD?

### NEED `AI-003`: `Expression of Implementation Requirements`

#### Description
In some cases, the model implementer may express specific needs concerning the implementation of the model. These requirements may concern any part of the model including:
- the order in which operators must be executed
- the target hardware on which the model or part of the model must be deployed
- etc.

#### Analysis
[TBC]

### NEED `AI-004`: `Support for traceability`

#### Description
The design, development, and V&V engineers need data (metadata) to support traceability analysis between the model elements (operators, graph), the requirements, the model and hyperparameters used during training, the development artifacts (code), and the verification artifacts (tests).

#### Analysis
[TBC]

> At what level shall traceaibility be maintained? Dos it make sense to trace an operator, a layer, to sole higher level requirement? Will it be such a high level requirement to trace to? 
 
### NEED `AI-005`: `Support for change management`

#### Description
The model designers and implementers need to manage changes done on the model: all changes to the model must be tracked and linked to requirements. Model versions must be managed.

#### Analysis
Change management shall be done on the file containing the SONNX model. 

> What is the granularity of change management? 

### NEED `AI-006`: `Support for model integrity`

#### Description
Means shall be provided to guarantee the integrity of the model throughout the development process, down to the deployment:
-	Provide cryptographic signatures for model files to ensure integrity.
-	Allow checksum or hash metadata to verify model integrity during deployment.

#### Analysis
Data to support model integrity must be carried in an additional file that would provide, e.g., a SHA. Consequently, no additional data shall is needed in the SONNX file. 

### NEED `AI-007`: `Support for model verification`

#### Description
The model designers and implementers need to verify that some intrinsic properties of the model hold. This include: 
-	Model integrity and completeness: graph structure is well formed, all required metadata is present
-	Semantic consistency: operators consistency (input/output shapes match definitions, data types are compatible between layers), operators are mathematically well-defined
-	Safety compliance: validate compliance with bounded arithmetic constraints, check for unsupported operators (stochastic, non-deterministics, other)
-	Numerical stability: potential sources of instability (division by zero, large exponentials), highlight nodes that may require specific numerical techniques in implementation
-	Error propagation analysis: assess sensitivity of outputs to small perturbations
-	Traceability: verify that all model components (nodes, operators, weights) are linked to requirements

#### Analysis
[TBC]

> Refine what is actually needed in terms of traceability. 

### NEED `AI-008`: `Behavioral determinism and predictability`

#### Description
The model implementation shall behave in a deterministic and possibly predictable manner:
- All inputs that may have an impact on the function performed by the model must be identified and documented. 
- No operator having a stochastic or unpredictable behavior must be allowed.
- The effects of rounding must be documented. The precision of the operators must be specified. The valid range for the operators must be defined. The behaviour in case of error (e.g., overflow) must be documented.
- Numerical instability of operators must be precluded or at least documented. 
- The model structure must be completely described by the model description. In particular, the size of all  tensors and the structure of the graph must be completely described in the model. More generally, all operations done on the tensors must be explicitely described in the model (e.g., no implicit type casting, [broadcasting](https://www.tensorflow.org/api_docs/python/tf/broadcast_to), shape inference).


All inputs that may have an impact on the function performed by the model must be identified and documented. 

> Define unstability in this context.

### NEED `AI-009`: `Resource usage determinism and predictability`

#### Description
The model implementer needs to provide an upper bound of memory usage. Therefore, constructs which memory usage would vary dynamically (e.g., depending on an input) should be prevented. 

#### Analysis
The objective is **not** to provide a means to estimate memory usage at model level since this actually depends on the implementation, but to preclude operators for which predictability would be intrinsically impossible.
[TBC]

### NEED `AI-010`: `Execution time determinism and predictability`

#### Description
The model implementer needs to provide an upper bound of execution time. Therefore, contructs which execution time would vary "significantly" (in particular: in an unpredictable way) should be prevented. 

#### Analysis
The objective is **not** to provide a means to estimate WCETs at model level since this actually depends on the implementation, but to preclude operators for which predictability would be intrinsically impossible.
[TBC]

### NEED `AI-011`: `Support for verification activities`

#### Description
The model developer needs means to support verifying compliance of his/her implementation of the model to the model. This concerns in particular demonstration of compliance with the operator and graph semantics. 

Should formal verification of the implementation against the specification be impossible to perform, the model developer needs a reference against which comparing his/her own implementation. This reference will be  considered to be compliant with the specification. 

Provision of test cases to verify compliance of an implementation against the specification would be useful. Those test cases may be those used to verify compliance of the reference implementation against the formal or informal specification. Those test cases need to cover all aspects of the specification, including those related to precision and stablity (e.g., inputs and expected outputs for softmax under typical and edge cases). 

# BOSCH needs

### NEED `BOSCH-001`: `Precise, unique operator specifications`
The default ONNX standard allows for a lot of variability in the definition of operators.

For example, the 'Unsqueeze' operator needs to have information about the axes it needs to unsqueeze.
This is sometimes stored as an attribute of the operator and sometimes as an input tensor.
The SONNX standard should only allow one specific way to give such information for each operator,
and it should not allow default values.
Each required attribute or tensor must be explicitly set in the model.
A bias tensor, for example, can of course be the zero vector, but it should be provided in any case.

### NEED `BOSCH-002`: `Precise set of supported operators with precise set of supported configurations`
For our use case code generation we require a precise set of operators that are supported within SONNX,
and a precise set of configurations of these operators. 

### NEED `BOSCH-003`: `Reference implementation`
A reference implementation of each supported operator in a high-level language (e.g. Python) 
to compare against would be very helpful, especially if SONNX shall contain support for quantized networks.

Currently, we see discrepancies between tensorflow, LiteRT, and tensorflow lite micro in the implementation of quantized networks.
Important standard libraries like CMSIS-NN and ACL could be used as a reference if they fulfill the requirements on code quality.


### NEED `AI-012`: `SONNX variability`
#### Description
The Safety-related profile shall implement the notion of build-time variability. For that, a set of variability points must be defined, together with their allowed variants (instantiation values).

Whether this build-time variability should lead to a set of pre-defined sub-profiles in SONNX, or to the capability, for user, to instantiate the safety-related profile in his/her context, must be defined during the SONNX specification activity.

#### Rationale
There are ONNX features that might be of interest in some applicative domain but not in another one.

#### Analysis
[TBC]

### NEED `AI-013`: `SONNX “product” definition, configuration and change management`
#### Description
The various kinds of constituents of the Safety-related profile must be identified before the start of its development. 

The principles of the configuration and change management shall be defined and implemented thanks to appropriate tools (presumably in github), before the actual development of the profile.

The configuration management includes the versioning of the Safety-related profile.

#### Rationale
Mastering the configuration, the evolutions and the correction of anomalies is crucial, moreover for safety-related systems.

#### Analysis
[TBC]

# ARCYS needs

### NEED `ARCYS-001`: `Final Prediction`
#### Description
The Safety-related profile shall provide an interpretation on the model output. For example, the last layer of the yolov8 model is a convolution and an image comes out. How to interpret the classes that were identified on the objects found in the input image from the output matrix?

#### Analysis
[TBC]
