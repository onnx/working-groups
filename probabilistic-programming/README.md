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

- Brian Parbhu  
- Adam Pocock (Oracle)  
(February 11, 2026 – Current)

---

## Logistics

WG leads will drive the meeting.

### WG Meeting Info
- Meeting: Friday @12pm EST every week cadance  
- Zoom Meeting link: https://zoom-lfx.platform.linuxfoundation.org/meeting/91272546777?password=43562609-9034-428b-af28-7562be759814  
- Meeting ID: 91272546777  

### Meeting Notes
(To be added)

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