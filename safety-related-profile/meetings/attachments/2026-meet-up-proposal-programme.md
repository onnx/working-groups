
# ONNX for Critical Systems

## Call for Participation

We are pleased to announce a two-day workshop dedicated to the use, evolution, and industrial deployment of the *Open Neural Network Exchange (ONNX) in critical systems.*

Critical systems are understood here in a broad sense. They include not only *safety-critical systems*, for which failures may endanger people, equipment, or the environment, but also *mission-critical* and *business-critical systems*, for which failures, incompatibilities, loss of performance, or long-term maintenance problems may have significant operational or economic consequences.

The workshop aims to bring together:
* industrial users of ONNX;
* ONNX contributors and experts;
* researchers;
* runtime, compiler, and tool developers;
* hardware and technology providers;
* specialists in verification, validation, qualification, and certification.

The objective is to create a bridge between the ONNX community and organizations deploying machine-learning models in critical applications. We would like to favour concrete technical discussions, experiments, specifications, and potential contributions to ONNX and its ecosystem.

# Objectives

The workshop will seek to:
* establish a shared understanding of the current state of ONNX and its ecosystem;
* identify the main obstacles to using ONNX in critical applications;
* distinguish problems already addressed by ONNX from remaining technical or methodological gaps;
* present ongoing initiatives intended to address these limitations;
* identify requirements specific to safety-, mission-, and business-critical applications;
* identify opportunities to improve ONNX specifications, documentation, implementations, and validation mechanisms;
* provide industrial use cases and requirements to the ONNX community;
* experiment collaboratively with possible solutions during hands-on sessions;
* identify concrete contributions, working topics, demonstrators, benchmarks, or follow-up activities.

The event is deliberately designed not only as a conference or information-sharing event, but as a working workshop from which concrete technical actions can emerge.

# Guiding Questions

The workshop will be structured around several questions.

### Where are we today?
* What does ONNX provide today?
* How is ONNX actually being used in industrial applications?
* What guarantees does the ONNX specification provide?
* What are the responsibilities of the specification, runtimes, converters, and tool providers?
* What mechanisms already exist for testing and conformance?

### What prevents ONNX from being used confidently in critical systems?

Possible issues include:
* ambiguity or incompleteness in operator specifications;
* differences between runtime implementations;
* preservation of semantics during model implementation;
* numerical behaviour and numerical reproducibility;
* operator coverage;
* model validation;
* runtime conformance;
* traceability between development and deployment environments;
* verification and validation;
* qualification or certification of tools and execution platforms;
* version management and backward compatibility;
* long-term maintainability;
* deterministic behaviour;
* performance guarantees;
* repeatability
* hardware-specific behaviour,
* etc.


### What is already being done?

The event will provide visibility on:

* ONNX roadmap and current developments;
* relevant ONNX working groups and special-interest groups;
* testing and conformance activities;
* improvements to specifications and operator definitions;
* runtime and compiler developments;
* verification and validation approaches;
* **SONNX and other initiatives addressing critical or safety-related uses of ONNX**.

### What should we work on next?

The objective is to identify issues for which the workshop community can formulate concrete requirements, specifications, tests, reference implementations, experiments, or proposals for future ONNX developments.

# Workshop Structure

The event will take place over **two complementary days**.

## Day 1 — State of the Art, Industrial Challenges and Ongoing Work

The first day establishes a common technical understanding of ONNX and of the problems encountered when using it for critical applications.

The purpose is to ensure that participants arrive at the hands-on sessions of Day 2 with a shared understanding of:

1. what ONNX currently provides;
2. where the most important difficulties lie;
3. which solutions and initiatives already exist;
4. which questions remain open.

### Morning — Invited Talks

The morning will consist primarily of invited presentations. 

*The detailed speaker list remains to be established.*

Possible presentations include:

**ONNX today**:
* current ONNX architecture and governance;
* status of the specification;
* operator sets and evolution mechanisms;
* ONNX roadmap;
* current working groups and priorities.

**Industrial adoption of ONNX**:
* how ONNX is being used in industrial systems;
* recurring interoperability and deployment problems;
* long-term model maintenance;
* expectations from organizations developing critical systems.

**ONNX and critical systems**:
* what changes when ONNX becomes part of a critical system;
* assurance, verification, traceability, qualification, or certification considerations;
* semantic and numerical consistency;
* runtime conformance and reproducibility.

**Ongoing initiatives**:
* current ONNX developments addressing identified limitations;
* SONNX;
* verification and validation activities;
* specification and conformance initiatives;
* relevant academic or industrial research.

The objective of the morning is not to provide an exhaustive tutorial on ONNX, but to establish a **common technical baseline and a clear picture of the problems that deserve attention**.

### Afternoon — Open Contributions

The afternoon will be open to contributions from the community.

We particularly encourage presentations that complement the morning sessions with:

* industrial experience reports;
* concrete ONNX deployment problems;
* limitations encountered in existing specifications or implementations;
* research results;
* tools and demonstrations;
* proposed ONNX improvements;
* verification and validation methods;
* compiler or runtime developments;
* experiences with hardware deployment;
* proposed solutions to critical-system requirements.

Contributions should preferably be **problem-oriented**.

Rather than simply presenting a product or project, contributors are encouraged to explain:

1. the problem being addressed;
2. why it matters for critical applications;
3. what ONNX currently provides;
4. what is missing or difficult;
5. the proposed or existing solution;
6. what could potentially be contributed back to the ONNX ecosystem.

The afternoon will conclude with a synthesis of the main issues identified during Day 1. These issues will provide input to the hands-on sessions on Day 2.

# Day 2 — Hands-on ONNX Working Sessions

The second day will be organized as a set of technical working sessions.

The objective is not primarily to present results, but to work collaboratively on concrete ONNX problems.  Participants will work from selected examples, use cases, models, operators, implementations, or test cases.

Possible hands-on session are proposed hereafter.
### Hands-on Session 1 — Writing an Unambiguous ONNX Operator Specification

**How should an ONNX operator be specified so that independent implementations behave consistently?**

Participants will select one or more operators and examine their specification from the perspective of critical-system use. 

Activities may include:
* analysing the existing operator definition;
* identifying ambiguities or underspecified behaviours;
* defining input and output semantics;
* defining accepted input domains;
* specifying corner cases;
* specifying error behaviour;
* examining numerical precision and rounding issues;
* identifying implementation-dependent behaviour;
* defining shape inference behaviour;
* defining constraints on attributes;
* producing illustrative examples;
* identifying useful properties or invariants;
* defining associated conformance tests.

The session could produce, for example:
* an improved operator specification;
* a list of specification ambiguities;
* proposed normative requirements;
* clarification examples;
* associated conformance tests;
* recommendations that could subsequently be submitted to the ONNX community.

## Hands-on Session 2 — From Specification to Conformance

**How can we determine whether an ONNX implementation actually conforms to the intended semantics?**

Starting from an operator or small model, participants could compare several implementations or runtimes.

Activities may include:
* deriving tests from the ONNX specification;
* creating nominal and boundary test cases;
* generating adversarial or unusual inputs;
* comparing runtime outputs;
* investigating numerical differences;
* distinguishing acceptable implementation freedom from specification violations;
* identifying missing conformance criteria;
* discussing reference implementations or executable specifications;
* examining how conformance evidence could be produced and retained.


Possible outputs include:
* reusable test cases;
* candidate conformance criteria;
* an operator test suite;
* identified runtime discrepancies;
* proposals for strengthening the ONNX testing infrastructure.

## Hands-on Session 3 — Critical-System Use Case

**From training framework to target hardware**

Participants could investigate:
* model conversion;
* preservation of semantics;
* version dependencies;
* operator compatibility;
* optimization transformations;
* runtime selection;
* numerical differences;
* hardware-specific behaviour;
* traceability of transformations;
* reproducibility;
* evidence needed to validate the deployed model.

The purpose would be to identify **where guarantees are lost across the toolchain** and which mechanisms could improve confidence in the deployed implementation.


The day will conclude with a plenary synthesis.


# Contributions for Day 1

Prospective speakers are invited to submit a short proposal describing:

* title;
* authors and affiliations;
* industrial or technical context;
* problem addressed;
* relationship with ONNX;
* relevance for critical systems;
* main findings or proposed solution;
* open questions that could benefit from discussion during the workshop.

We particularly encourage submissions presenting **problems that could lead to collaborative work during Day 2**.

Contributions may take the form of:

* technical presentations;
* industrial experience reports;
* demonstrations;
* problem statements;
* research presentations;
* proposals for ONNX improvements.

---

# Contributions to Day 2

Participants may also propose a hands-on topic.

A proposal should contain:

* the technical question to investigate;
* why the issue matters;
* the ONNX artifact concerned;
* an example operator, model, runtime, or use case;
* required tools or data;
* the activity participants would perform;
* the expected output.

Suitable topics should preferably be narrow enough for participants to make tangible progress during the workshop.

---

# Expected Outcomes

The workshop aims to produce more than a collection of presentations.

Expected outcomes include:

* a consolidated view of the main barriers to using ONNX in critical systems;
* a clearer distinction between specification, implementation, tooling, and methodological issues;
* identified gaps in ONNX specifications or implementations;
* proposed improvements to operator specifications;
* reusable conformance or validation tests;
* documented industrial requirements;
* proposals for ONNX issues or pull requests;
* candidate topics for ONNX working groups;
* shared benchmarks or demonstrators;
* collaborative research or development activities;
* stronger links between industrial users and the ONNX community.

Where possible, issues and proposals identified during the workshop should subsequently be transformed into **concrete contributions to ONNX, SONNX, associated tools, or collaborative projects**.

---

# Proposed Two-Day Programme

### Day 1 — Understand

**Morning — Invited talks**

* Welcome and objectives
* ONNX: current status and roadmap
* ONNX specification and implementation challenges
* Requirements from critical-system applications
* Current initiatives and SONNX
* Invited industrial or research perspectives

**Afternoon — Community contributions**

* Industrial experience reports
* Technical problems and open issues
* Research and ongoing developments
* Tools and demonstrations
* Discussion

**End of Day 1**

* Consolidation of the main technical questions
* Preparation of Day 2 working groups

### Day 2 — Experiment and Contribute

**Morning**

* Introduction to hands-on activities
* Working Session 1: specifying an ONNX operator
* Working Session 2: specification-to-implementation conformance

**Afternoon**

* Working Session 3: end-to-end critical-system deployment case and/or additional parallel working groups
* Consolidation of results
* Identification of ONNX/SONNX contributions
* Definition of follow-up actions

### Closing session

