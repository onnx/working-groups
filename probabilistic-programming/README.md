# ONNX Probabilistic Programming (WG)

This repository is where the ONNX Probabilistic Programming Working Group captures artifacts, proposals, specifications, and deliverables related to extending ONNX with probabilistic modeling and Bayesian inference capabilities.

---

## Working Group Status

**ACTIVE**

---

## Slack Channel

onnx-probabilistic-programming
---

## WG Lead(s)

- Brian Parbhu, (February 11, 2026 – Current)  
- Adam Pocock (Oracle), (February 11, 2026 – Current)

---

## Logistics

WG leads will drive the meeting.

### WG Meeting Info
- Meeting: Friday @12pm EST every 2 weeks cadance  
- Zoom Meeting link: https://zoom-lfx.platform.linuxfoundation.org/meeting/91272546777?password=43562609-9034-428b-af28-7562be759814  
- Meeting ID: 91272546777  

### Meeting Notes

The meeting notes can be found [here](https://github.com/onnx/working-groups/probabilistic-programming/meetings)

---

# Mission

Define how ONNX infrastructure, operators, and runtime constructs can support:

- Probabilistic graphical modeling  
- Bayesian inference  
- Probabilistic programming languages (PPLs)  

This initiative extends ONNX beyond deterministic machine learning to support uncertainty-aware AI systems.

---

# What is Probabilistic Programming?

Probabilistic programming provides a unified framework for specifying statistical models and performing Bayesian inference automatically.

## Core Concepts

- Models are specified using **random variables with explicit probability distributions**
- Systems compute **log-likelihoods and posterior distributions**
- Inference returns **distributions over parameters**, not point estimates
- Model specification is separated from inference execution

## Common Inference Algorithms

- HMC
- NUTS
- SMC
- Variational Inference
- Laplace
- INLA
- Pathfinder
- Gibbs

Probabilistic programming languages act as compilers for Bayesian inference.

---

# Why Extend ONNX with Probabilistic Modeling?

## 1. Extends ONNX Beyond Deterministic ML

- Adds native uncertainty-aware AI
- Complements neural networks and GenAI systems

## 2. Unifies Fragmented Ecosystems

Today each PPL implements:

- Custom RNG systems
- Distribution libraries
- Special functions
- Inference engines

ONNX can provide a standardized IR for probabilistic computation.

## 3. Enables Portable Inference

ONNX Runtime enables execution across:

- CPUs
- GPUs
- Cloud
- Edge
- Accelerators

This removes reliance on framework-specific runtime engines.

## 4. Encourages Hardware Vendor Adoption

Standardized operator domains allow vendors to optimize:

- RNG
- Special functions
- Inference kernels

## 5. Supports Hybrid AI Systems

Enables models combining:

- Neural networks
- Bayesian inference
- Symbolic/statistical reasoning

---

# Problems This Initiative Solves

## No Standard IR for Probabilistic Models

Each framework emits its own internal representation, preventing:

- Interoperability
- Shared optimization
- Portable deployment

## Inconsistent RNG Semantics

Frameworks differ in:

- Seed handling
- Threading behavior
- Reproducibility guarantees

This breaks cross-platform determinism.

## Missing Special Functions & Bijectors

Re-implemented per framework, causing:

- Numerical drift
- Portability challenges
- Redundant engineering effort

## No Shared Accelerator Story

Current acceleration paths are fragmented:

- Python-bound runtimes
- Custom C++ kernels
- JAX-only acceleration

## No Portable Inference

Inference engines (HMC, NUTS, SMC, INLA, Laplace) are tightly coupled to specific frameworks.

ONNX can become the universal runtime for Bayesian inference.

---

# Alignment with ONNX Design Principles

## Preserves Functional Operator Model

- Operators remain pure and composable
- RNG is stateless and splittable
- Compatible with ONNX execution graphs

## Leverages ONNX Runtime Strengths

ORT already supports:

- GPU acceleration
- Parallel execution
- Subgraph execution

These are core requirements for MCMC and SMC workloads.

## Mirrors the GenAI Extension Strategy

- Introduces new operator domains
- Minimizes ONNX core modifications
- Provides incremental ecosystem adoption

## Supports ONNX 2.0 Vision

Probabilistic modeling becomes a foundational pillar alongside:

- Deterministic ML
- GenAI

---

# Working Group Structure

The ONNX Probabilistic Programming initiative is organized into three working groups.

---

## WG1 – Probabilistic Operators & Functions

### Scope

Standardize:

- RNG (SplitPRNG, stateless random ops)
- Distributions (Normal → Dirichlet; Mixtures; HMMs)
- Bijectors (parameter transforms, flow layers)
- Special functions (LogGamma, Digamma, Bessel, incomplete gamma, etc.)

### Deliverables

- New probabilistic operator domains (e.g., `ai.onnx.prob*`)
- Decomposable FunctionProto reference graphs
- CPU/CUDA reference kernels for ONNX Runtime
- Converter and backend alignment guidance

---

## WG2 – Inference & Pipelines

### Scope

Standardize inference operators:

- Laplace
- Pathfinder
- INLA
- HMC
- NUTS
- Gibbs
- SMC

### Pipeline Components

- Sampling
- Diagnostics (ESS, R-hat, divergences)
- Simulation-Based Calibration (SBC)

### Advanced Topics

- Warp-aware NUTS
- Batched MCMC
- Vectorized SMC
- Execution-provider integration

---

## WG3 – Exporters & Framework Alignment

### Initial Exporters

- Stan
- PyMC

### Next Phase

- NumPyro
- Pyro
- TensorFlow Probability
- JAX-native probabilistic models
- rxinfer
- BayesFlow

### Future Alignment

- R-INLA
- Turing.jl

### Responsibilities

- Standardize conversion patterns
- Provide exporter templates
- Maintain cross-framework semantics (shape, mask, plate notation)

Goal:

Create a unified ONNX-backed probability and inference layer that all frameworks can target.

---

# Technical Deliverables

## Operator-Level

- Seedable, reproducible, splittable PRNG semantics
- LogProb, Observe, Factor, Random* operators
- Distribution & bijector catalogs
- Special function operator domain

## Inference

- Approximate inference (Laplace, Pathfinder, INLA)
- MCMC (HMC, NUTS, Gibbs, Slice)
- SMC variants
- Diagnostics (ESS, R-hat, divergences, SBC)

## Runtime

- `onnxruntime-prob-extensions`
- GPU-accelerated special functions & inference kernels
- Subgraph APIs for log-joint invocation
- Reproducible multi-thread and multi-device execution

---

# Roadmap

## After Steering Committee Approval

- Formal WG charter
- RNG specification
- Base probabilistic operator set
- Special functions + initial distributions
- First exporters: Stan, PyMC
- Draft opset for `ai.onnx.prob*`

## Longer-Term Targets

- Full probabilistic opset v1
- Complete exporter suite
- GPU-optimized NUTS / SMC
- Turing.jl → ONNX interoperability
- R-INLA → ONNX interoperability
- Integration into ONNX 2.0 roadmap

---

# Deployment & Ecosystem Context

## Deployment Gap in Probabilistic Programming

Many probabilistic programming languages (PPLs) operate in siloed computational environments.

- Some use JAX or PyTorch
- Some rely on custom compute engines (e.g., Stan)
- Many are optimized for notebook-based workflows
- Deployment of inferred probabilistic models is often framework-specific

However, the core probabilistic operations across PPLs are structurally similar:

- Sampling from probability distributions
- Accumulating log-probability terms
- Executing iterative inference updates

ONNX provides a cross-platform runtime abstraction that can unify deployment across ecosystems and hardware targets.

---

# Operator & Runtime Constraints

Certain probabilistic primitives cannot be fully expressed as pure ONNX graph compositions.

Examples include:

- Special mathematical functions (LogGamma, Digamma, etc.)
- Distribution samplers that require unbounded looping

These require:

- Runtime-level implementations
- Reference CPU/CUDA kernels
- Explicit execution semantics inside ONNX Runtime

This working group will clearly define which constructs are:

- Primitive operators
- FunctionProto graph decompositions
- Runtime extension requirements

---

# Inference Operator Interface Model

Inference operators are typically iterative and update model state based on observed data.

For example, a proposed HMC operator would accept:

- A model graph
- A gradient graph
- A PRNG state
- Observed data
- Current model parameters

And emit:

- Updated model parameters

This allows ONNX to function not only as a model exchange format, but as a backend execution engine for probabilistic inference and deployment.

---

# Exporter Strategy & Scope Control

While many probabilistic frameworks are candidates for export:

- Stan
- PyMC
- Pyro
- NumPyro
- TensorFlow Probability
- JAX-native probabilistic systems
- rxinfer
- BayesFlow

The initial strategy is to focus on two exporters first.

This prevents overfitting the specification to too many framework-specific abstractions and ensures the operator design remains general and stable.

---

# Current Status

- Proposal presented to the ONNX Steering Committee in December.
- Feedback requested demonstrated interest from the probabilistic programming community.
- Prior PRNG specification work predates the formation of this WG and remains a foundational component.
- A formal PRNG specification and Python reference implementation are planned as early deliverables.
- Community outreach across the PPL ecosystem is ongoing.
