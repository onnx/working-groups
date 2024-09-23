# Introduction

## Terms

The following terms are used in the document:

-   **Trained ML model**: the conceptual structure of graphs and
    operators that maps a set of input tensors to a set of output
    tensors. The Trained ML Model Description (TMD) is represented using
    the *Trained Model Description Language* (TMDL).

-   **Trained ML Model Description** (TMD: a concrete representation of
    the conceptual trained ML Model that can be interpreted by a human
    or a program.

-   **Trained ML Model Description** **Language** (TMDL): The language
    used to represent a *Trained ML Model* (TMD).

## Contents

This document gives a first definition of the activities to be carried
out by the ONNX safety-related profile workgroup. This "workplan" is
aimed at being presented *and discussed* during the Workgroup kick-off
meeting planned for the end of September.

## Main objectives

Provide a definition of the formalism used to represent a trained ML
model\...

-   *\... that has an understandable and non-ambiguous syntax and
    semantics.*

    The description of the ML model expressed using this formalism must
    be a Low-level Requirement for the implementation phase in the sense
    that its interpretation and implementation shall not require any
    further information that the one given by the description of the ML
    model.

-   *\... that allows multiple levels of accuracy and precision for the
    description of a given model.*

    The language used to describe the model (i.e., its syntax and
    semantics) must be non-ambiguous, but a model may be ambiguous if
    this ambiguity is acceptable or even necessary to leave some freedom
    to the implementer (e.g., for optimization). The objective is to
    identify, control, and possibly remove this ambiguity by an
    appropriate refinement of the ML model description.

# Workgroup Activities

This section presents the different activities of the workgroup. Their
dependencies are expressed via their inputs/outputs.

### A1 - Elicitation of industrial needs

#### Objectives

Elicit end users' needs related to the ONNX format, i.e., What are the activities using ONNX models? What are the evidences required by certification authorities that involve the ONNX model? How do the ONNX model impact these activities?

#### Rationale

The definition of the scope of the safety-related profile (SR profile) and the elicitation of the end users' needs within that scope set the frame for the SR profile development.

#### Activity overview

First define the scope of the safety-related profile in terms of operators and constructs on the basis of use cases coming from the various industrial domains.
Then describe the needs per domain and consolidate them for the whole SR profile.
 

#### Inputs

-   Certification standards (e.g., ARP6983, ISO/DPAS 8800,
    ECSS-E-HB-40-02A DIR1, etc.)

-   Company-specific requirements

-   End users' use cases

#### Outputs

-   D1.a.\<x\>: End users' needs and requirements for domain \<x\>.
-   D1.b: Consolidated needs for all industrial domains
-   D1.c: Safety-related Profile Scope Definition

#### Detailed activities

The activities defined below are per domain <x>.

##### SC: SR profile Scope Definition

- SCAct1: Identification/definition of the Safety-related industrial use case reference models

- SCAct2: Extraction of the operators and constructs from the Safety-related industrial use cases reference models

- SSAct3: Consolidation of the set of operators and constructs to be included in the Safety-related profile (from the reference models possibly augmented with necessary additional operators and constructs).

##### EN: End Users' Needs Elicitation

-   ENAct1.\<x\>: Description (overview) of the machine learning development
    process

-   ENAct2.\<x\>: Description of the development process objectives and
    activities that produce the TMD and take it as input

-   ENAct3.\<x\>: Definition of the *Trained Model Description (TMD)* artefact
    (e.g., the Machine Learning Model Description (MLMD) in ARP6983)

-   UENAct4.\<x\>: Description of the development process verification
    objectives and activities that apply to the TMD

-   ENAct5.\<x\>: Expression of constraints on the TDM, that come from the Development and verification activities the Industrial context

-   ENAct6.\<x\>: Expression of the needs

-   ENAct7.\<x\>:Consolidation of industrial needs from all domains


### A2: Specification of the ONNX SR profile

#### Objectives

Elaborate the list of requirements applicable to the SR profile in order to comply with the end users' needs. Consolidate, filter, and prioritize the needs identified for the different industrial domains in D1.a.<x>. Discriminate requirements aimed at the preservation of the model semantics from requirements aimed at facilitating / supporting other development assurance activities.

#### Rationale

Before starting the development of the constituents of the SR profile, it is mandatory to express requirements in compliance with the users' needs, in order to guarantee the satisfaction of the latter.

#### Activity overview

Before writing the requirements for the SR profile, the various aspects to consider shall be identified clearly.
Then the requirements are elaborated, grouped, prioritized and verified against the end users' needs, within the SR profile scope.
Furthermore, the requirements for ONNX will be made traceable to one or several end users’ needs.

#### Inputs

-   D1.a.\<x\>: End users' needs for domain \<x\>.
-   D1.b: Consolidated needs for all industrial domains
-   D1.c: Safety-related Profile Scope Definition

#### Outputs

-  D2.a: ONNX safety-related Profile Requirements

#### Detailed activities

##### OR: ONNX SR profile requirements specification

-  ORAct1: Definition of the list of the aspects (e.g., accuracy, completeness, traceability, etc.) to which the requirements for a safety-related ONNX profile will apply

-  ORAct2: For each aspect, definition of the requirements applicable to the standard

-  ORAct3: Grouping and prioritization of requirements

-  ORAct4: Verification / traceability of the requirements against the end users' needs.

### A3: Development of the ONNX SR profile

#### Objectives

Development of the ONNX Safety-related profile (syntax and semantics) in compliance with the ONNX safety-related Profile Requirements (D2.a)

#### Rationale

The compliance of the SR profile with its requirements, together with the fact that the requirements are expressed from the end users' needs, leads to the satisfaction of the end users' needs.

#### Activity overview

Guidelines for the development of the SR profile are first written thanks to a proof of concept that consists in developing a limited subset of the SR profile.
Then, these guidelines are used to develop the SR profile graph semantics, the semantics of the operators of the SR profile scope, the exchange format and the reference implementation.
The SR profile constituents shall be verifiable against their requirements (verification) and against the end users' needs (validation).

#### Inputs

-  D2.a: ONNX safety-related Profile Requirements

#### Outputs

-   D3.a: ONNX Safety-related profile - proof of concept
-   D3.b: ONNX Safety-related profile - graph
-   D3.c: ONNX Safety-related profile - operators
-   D3.d: ONNX Safety-related profile - format
-   D3.e: ONNX Safety-related profile - reference implementation
-   D3.f: ONNX Safety-related profile - rules

#### Detailed activities

##### POC: Proof of concept

-   PROAct1: Elaborate a first set of (informal + formal) specification guidelines and apply them on a few operators (e.g., conv) and constructs in order to discussed and reviewed by the workgroup. They will serve as a baseline for other operators

##### GR: Graph execution semantics

-   GRAct1: Development of the ONNX SR profile graph semantics in compliance with specification D2.a

##### OP: Operator semantics

-   OPAct1: Development of the ONNX SR profile operators' semantics in compliance with specification D2.a

##### FO: Format

-  FOAct1: Development of the ONNX SR profile exchange format in compliance with specification D2.a

##### RI: Reference implementation

-  RIAct1: Development of a reference implementation (on the basis of the existing ref imp.). This covers the development of the graph execution engine and operators.

### A4: V&V of the ONNX Safety-related profile

#### Objectives

Verification (validation) of the ONNX Safety-related profile vs the requirements (resp. needs) expressed in D2.a (resp D1.b and D1.c)

#### Rationale

Since the SR profile aims at becoming the ONNX standard for safety-related applications, it is important to verify/validate it before end users can use it. 

#### Activity overview

The SR profile is verified against the requirements and validated against the end users' needs. Verification/validation cases and results shall be documented in order to give evidences about the activity.

#### Inputs

-   D3.b: ONNX Safety-related profile - graph

-   D3.c: ONNX Safety-related profile - operators

-   D3.d: ONNX Safety-related profile - format

#### Outputs

-   D4.a: ONNX Safety-related profile verification report
    Profile
-   D4.b: ONNX Safety-related profile validation report. 

#### Detailed activities

##### VE: Verification

-   VEAct1: Review of the ONNX SR profile against the requirements in D2.a 

##### VA: Validation

-   VAAct1: Validation of the ONNX SR profile via its application to one or several industrial use cases 


### A5: Tooling

#### Objectives

Expression of the needs and requirements of a toolset aimed at supporting the exploitation of the ONNX SR model, e.g., model inspection and review tool, according to the end users' ML development process objectives, activities, and to the definition of the SR profile and associated rules.

#### Rationale

Automatic rule checkers (for, e.g, consistency checks) or tools supporting model inspection and review might be the industrial answer to the fulfilment of regulatory constraints

#### Activity overview

The needs of tools and the list of them are first established.
Then the requirements applicable to each tool of the list are written. 

#### Inputs

-   D1.b: Consolidated needs for all industrial domains
-   D3.a: ONNX Safety-related profile - proof of concept
-   D3.b: ONNX Safety-related profile - graph
-   D3.c: ONNX Safety-related profile - operators
-   D3.d: ONNX Safety-related profile - format
-   D3.e: ONNX Safety-related profile - reference implementation
-   D3.f: ONNX Safety-related profile - rules

#### Outputs

- D5.a: Expression of the needs / tool list 
- D5.b.\<tool\>: Requirements of tool \<tool\>

#### Detailed activities

##### TN: Tool needs elicitation

- TNAct1: Expression of the needs for tools

##### TS: Tool requirements

- TSAct2.\<tool\>: Expression of the requirements of tool \<tool\>




