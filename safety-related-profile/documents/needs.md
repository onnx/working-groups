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

### NEED 001: `Compliance with ARP6983`
#### Description
The development of Machine Learning constituents in avionics needs to comply with the ARP6983 regulation document. The Safety-related ONNX profile (SONNX) shall constitute a language in which the Machine Learning Model Description (MLMD), as defnined by ARP6983, can be expressed.
#### Rationale 
The MLMD must exist as defined by the ARP6983 document. It shall be the pivot between the trained model and the implementation for embedded inference, which is the basic aim of ONNX.

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


