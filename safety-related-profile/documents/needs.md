test test test

# Needs

This section capture the needs of the users of the ONNX model. By _users_, we mean both people generating the model and  using it during the early verification and validation phases (before implementation), and those of people using the model during the implementation, and late verificaton and validation phases. 

**A need must refer to some activity / goal that a SONNX user must do / achieve. The expression of a need should be of the form: "The <role> needs <something> to do <something>."  For instance, "The ML model developer needs a non-ambiguous description of each operator in order to build a model." or "The ML model implementer needs a non-ambogiguous description of the model operator and execution logic in order to implement the model.", etc.**

**A requirement expresses what SONNX must provide for the user to do his/her activity. provide a user with.**

## Recommendations
Here are a few questions that you may ask yourself when trying to identify your needs:
- Properties
  - What are the properties verified on the ONNX model? Robustness? fairness? other?
  - What properties do you want to preserve during the model implementation
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
  - Do you plan to use the model to generate code?
    - using some automated tool?
    - manually?
- Instrumentation 
  - Do you plan to instrument the implementation of the model? at what level?


### NEED `<XXX>`: `<Need title>`
#### Description
_Brief description of the need_
#### Rationale (optional) 
If necessary, a _brief justification of the need_ 


### NEED XXX: `Expression of Low Level Requirements`

#### Description
The model implementer needs a clear, complete and unabiguous description of the model, that is to say:
- the graph structure (structure of interconnected operators)
- the graph parameters (weights, biases, activation thresholds)
- the description of the semantics of the graph and all elements of the graph. 

### NEED XXX: `Expression of High Level Requirement`

#### Description
The model implementer needs High Level requirements about the model performance. Those requirements may concern:
- the ML performance, which may depend on the task performed by the model (e.g., Mean Squared error or Mean Absolute error for regression tasks, or precision or accuracy for classification tasks)
- numerical precision measured at the output of the model or at intermediate stages, and measured at specific points for a specific referece dataset.

### NEED XXX: `Expression of Implementation Requirements'

#### Description
In some cases, the model implementer may express specific needs concerning the implementation of the model. These requirements may concern any part of the model including:
- the order in which operators must be executed
- the target hardware n which the model or part of the model must be deployed,
- etc.


### NEED XXX: `Support for traceability`

#### Description
The desing, development, and V&V engineers need data (metadata) to support traceability analysis between the model elements (operators, graph), the requirements, the model and hyperparameters used during training, the development artifacts (code), and the verification artifacts (tests).

### NEED XXX: `Support for change management`

#### Description
The model designer and model implementer need to manage changes done on the model: all changes to the model must be tracked and linked to requirements. Model versions must be managed.

### NEED XXX: `Support for model integrity`

#### Description
Means shall be provided to guarantee the integrity of the model throughout the development process, down to the deployment:
-	Provide cryptographic signatures for model files to ensure integrity.
-	Allow checksum or hash metadata to verify model integrity during deployment.

### NEED XXX: `Support for model verification`

#### Description
The model designer and implementer need means to verify intrinsic properties of the model including: 
-	Model integrity and completeness: graph structure is well formed, all required metadata is present
-	Semantic consistency: operators consistency (input/output shapes match definitions, data types are compatible between layers), operators are mathematically well-defined
-	Safety compliance: validate compliance with bounded arithmetic constraints, check for unsupported operators (stochastic, non-deterministics, other)
-	Numerical stability: potential sources of instability (division by zero, large exponentials), highlight nodes that may require specific numerical techniques in implementation
-	Error propagation analysis: assess sensitivity of outputs to small perturbations
-	Traceability: verify that all model components (nodes, operators, weights) are linked to requirements


### NEED XXX: `Behavioral determinism and predictability`

#### Description
The model implementation shall behave in a deterministic and possibly predictable manner. 

All inputs that may have an impact on the functioncperformed by the model must be identified and documented. 

No operator having a stochastic or unpredictable behavior must be allowed.

The effects of rounding must be documented. The precision of the operators must be specified. The valid range for the operators must be defined. The behaviour in case of error (e.g., overflow) must be documented.

Numerical instability of operators must be precluded or at least documented. 

The model structure must be completely described by the model description. In particular, the size of all  tensors and the structure of the graph must be completely described in the model. More generally, all operations done on the tensors must be explicitely described in the model (e.g., no implicit type casting, [broadcasting](https://www.tensorflow.org/api_docs/python/tf/broadcast_to), shape inference).

### NEED XXX: `Resource usage determinism and predictability`

#### Description
The resource usage must be computable beforehand or, at least, must be deterministic and rpredictable too.

### NEED XXX: `Support for verification`

#### Description
The model developer needs means to support verifying compliance of his/her implementation of the model to the model. This concerns in particular demonstration of compliance with the operator and graph semantics. 

Should formal verification of the implementation against the specification be impossible to perform, the model developer needs a reference against which comparing his/her own implementation. This reference will be  considered to be compliant with the specification. 

Provision of test cases to verify compliance of an implementation against the specification would be useful. Those test cases may be those used to verify compliance of the reference implementation against the formal or informal specification. Those test cases need to cover all aspects of the specification, including those related to precision and stablity (e.g., inputs and expected outputs for softmax under typical and edge cases). 





### NEED 001: `Accurate and Precise Trained Model Description`

#### Description
Need for an ML description "language" with well-defined syntax and semantics enabling one to produce an accurate, precise a consistent description of the ML model, leaving no room to interpretation nor unspecified approximations.

#### Rationale
Safety-related systems require the demonstration that the ML model implementation process preserves the safety/functional/operational properties of the model developed during the design process.

### NEED 002: `SONNX variability`
#### Description
The Safety-related profile shall implement the notion of build-time variability. For that, a set of variability points must be defined, together with their allowed variants (instantiation values).

Whether this build-time variability should lead to a set of pre-defined sub-profiles in SONNX, or to the capability, for user, to instantiate the safety-related profile in his/her context, must be defined during the SONNX specification activity.

#### Rationale
There are ONNX features that might be of interest in some applicative domain but not in another one.

### NEED 003: `SONNX “product” definition, configuration and change management`
#### Description
The various kinds of constituents of the Safety-related profile must be identified before the start of its development. 

The principles of the configuration and change management shall be defined and implemented thanks to appropriate tools (presumably in github), before the actual development of the profile.

The configuration management includes the versioning of the Safety-related profile.

#### Rationale
Mastering the configuration, the evolutions and the correction of anomalies is crucial, moreover for safety-related systems.


### NEED 004: `Compliance with ARP6983`
#### Description
The development of Machine Learning constituents in avionics needs to comply with the ARP6983 regulation document. The Safety-related ONNX profile (SONNX) shall constitute a language in which the Machine Learning Model Description (MLMD), as defined by ARP6983, can be expressed.

The SONNX Safety-related profile shall allow the specification of the replication criterion, exact or approximate, that the implementation must ensure.

#### Rationale 
The MLMD must exist as defined by the ARP6983 document. It shall be the pivot between the trained model and the implementation for embedded inference, which is the basic aim of ONNX. The ARP6983 document requires that a replication criterion be defined in the MLMD, which constitutes a strong constraint applying to the implementation from the MLMD.

# Requirements 

YThis section captures all requirements about the SONNX profile. 


## Operators

### REQ OP-001: `<Req title>`

#### Description
_Statement of the requirement_

#### Rationale 
_Brief rational for the requirement_ 

#### Need
_Reference to the need served by this requirement_

## Graph execution 


## File format


