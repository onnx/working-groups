<!--- SPDX-License-Identifier: Apache-2.0 -->

# ONNX Safety-Related Profile Working Group (WG)

The purpose of this WG is to elaborate an ONNX profile dedicated to "safety-related" systems.

An ONNX model is the representation of an ML/AI model to be implemented. In other words, it is the specification for the implementation activity. 
The model may be either interpreted by a tool or translated into some lower level equivalent representation (e.g., some source code) by a tool or a human.  In both cases, to be able to interpret the model according to the intent of its designer, its syntax and semantics must be clear and non-ambiguous. 
This requirement is applicable to any system, but it is critical for systems for which a failure may have a critical business or safety impact.
This is for instance the case in the aeronautical domain for which evidences shall be provided to show that the model semantics is actually preserved throughout the implementation phase (see ARP 6983, "Process Standard for Development and Certification/Approval of Aeronautical Safety-related Products implementing AI").
We consider that the current ONNX standard does not fully satisfy these requirements and that there is a need (i) to clarify the industrial needs in that matter, (ii) to identify and address the weaknesses of the current standard in a systematic manner in order to produce an "safety-related ONNX profile" that would to fulfil these needs.
We also consider that these needs are specific and that the proposed changes and clarifications of the syntax, semantics, and documentation shall not prevent the use of ONNX in domains where constraints are relaxed. For instance, introducing restrictions on the parameters values for operators of the safety-related profile must not affect the usage of the same operators out of the profile. 

# Contents

The main elements of this repository are:
- [Slides of the Kick-Off Meeting](./meetings/general/2024-09-25%20-%20KOM/2024-09-25%20-%20SONNX%20KOM.pdf)
- [Recent presentation of the projects results](./meetings/Other_meetings/SONNX%20-%20WG114-%20oct-2025.pdf)
- [Minutes of the WG meetings](./meetings/minutes.md)
- Deliverables (draft)
  - [Industrial needs](./deliverables/needs/needs.md) (What are the needs of the industrial partners?)
  - [Use cases](./deliverables/scope/scope.md) (What are the first models to be implemented using SONNX?)
  - [Requirements](./deliverables/reqs/reqs.md) (How do the needs translate to constraints on the SONNX profile?)
  - [Issues](./deliverables/issues/issues.md) (What are the first issues identified for the usage of ONNX in a safety-related system?) (obsolete)
  - [Informal specification of operators](./sonnx/ops/spec/informal/)
  - [Formal specification of operators](./sonnx/ops/spec/formal/)
    Formal specification of operators is done using the [Why3](https://www.why3.org/).
  - [Formal specification of graphs](./sonnx/graph/README.md) (tbc)
Note that this is a **work in progress**. 


# Working Group Status
**ACTIVE**


# WG Lead(s)

* Eric JENN (IRT Saint-Exupery, France) and Jean SOUYRIS (Airbus, France) (July 22, 2024 - Current)


# WG Meeting Info

* Working group meetings take place every other Wednesday, 4 p.m. to 6 p.m. (Paris time)
* To join, please subscribe to the SONNX mailing list (see below); we will come back to you.
* The meeting notes can be found [here](./meetings/minutes.md). 

# Mailing list
* To subscribe to the mailing list, send an email to onnx-sonnx-workgroup+subscribe@lists.lfaidata.foundation
  
