test test test

# Needs

This section capture the needs of the users of the ONNX model. By _users_, we mean both people generating the model and  using it during the early verification and validation phases (before implementation), and those of people using the model during the implementation, and late verificaton and validation phases. 

A need expresses what a SONNX user must achieve. A requirement express what SONNX must provide a user with.  

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
#### Rationale 
_Brief justification of 


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


### NEED 003: `Compliance with ARP6983`
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


