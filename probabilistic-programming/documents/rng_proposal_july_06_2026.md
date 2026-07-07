# Stateless and Splittable PRNGs for ONNX

## Introduction

Pseudo-Random Number Generators (PRNGs) provide a stream of random numbers produced by computing specific functions of some hidden state variables. The generation of each random number modifies the state of the PRNG, and the generated random number is a deterministic function of the state. The initial state is a function of some seed value; when left unset this is typically chosen based on the system clock, though this makes the sequence of numbers not reproducible.

PRNGs are designed such that the sequence of generated values has as little statistical correlation as possible, though different PRNG algorithms have different detectable biases. For many PRNGs, repeatedly seeding them and drawing a single value produces a lower quality stream of random numbers than having a single PRNG and drawing from it sequentially.

This proposal uses the **Threefry** PRNG algorithm, as implemented in JAX, as the reference PRNG algorithm.

The deterministic nature of PRNGs makes them extremely attractive for reproducible computations, allowing the same sequence of outputs for the same seed. When used in multithreaded environments it is important to control access to the PRNG if a deterministic sequence is required, as otherwise there could be multiple interleavings of different threads and it will be unclear which thread received which random numbers.

### Running Examples

Throughout this proposal we use two motivating examples.

#### Large Language Model (LLM)

Sampling a token from an LLM output.

Concretely, we have a *d*-dimensional vector containing a probability distribution over *d* vocabulary items. We sample a single uniform value from the interval `[0,1]`, compute the cumulative distribution function (CDF), locate the bucket containing the sampled value, and emit the corresponding token.

#### Diffusion Models

Initial image generation for diffusion models.

A tensor of shape `[w, h, d]` is sampled from a normal distribution, scaled to the appropriate mean and variance, and used as the initial noise for image generation.

---

# Current State of ONNX RNGs

The existing ONNX specification defines four operators that sample from pseudorandom number generators:

- `RandomNormal`
- `RandomNormalLike`
- `RandomUniform`
- `RandomUniformLike`

`RandomNormal` produces values from a normal distribution with the shape, mean, variance, and dtype specified as attributes.

`RandomUniform` produces values from a uniform distribution with the shape, lower bound, upper bound, and dtype specified as attributes.

`RandomNormalLike` and `RandomUniformLike` derive the output shape (and optionally the output dtype) from an input tensor.

The current specification does not define:

- whether the underlying PRNG is stateful or stateless,
- what should occur when a graph is executed multiple times,
- or the behavior when the seed attribute is omitted.

The current specification states:

> "Seed to the random generator, if not specified we will auto generate one."

However, it is unclear whether the seed is generated:

- once when the graph is instantiated, or
- every time the operator executes.

As a result, multiple compliant implementations may exhibit significantly different behavior, reducing portability across ONNX runtimes.

---

# Reference Implementation

The reference implementation in the ONNX repository currently exhibits two behaviors.

### Seeded

When seeded, each execution of the operator produces exactly the same values.

#### LLM

Each token generation receives the same sampled random value. Although different probability distributions may still produce different tokens, this introduces undesirable correlations into generated text.

#### Diffusion

Exactly the same initial noise tensor is generated for every graph execution.

Changing the seed requires rebuilding the ONNX graph because the seed is stored as an attribute.

---

### Unseeded

When unseeded, NumPy initializes a new PRNG using the current time.

#### LLM

Each execution produces different random values.

The sequence cannot be reproduced, and multiple executions occurring within the same timestamp may receive identical random values.

#### Diffusion

Each execution generates different initial noise.

Images are no longer reproducible because the underlying PRNG state is unknown.

Again, multiple executions sharing the same timestamp may generate identical noise tensors.

---

# ONNX Runtime

The ONNX Runtime CPU execution provider initializes a C++ PRNG for every random operator when the graph is constructed.

The PRNG is initialized using either:

- the supplied seed attribute, or
- a seed generated from the startup time combined with the node identifier.

Each operator therefore owns mutable PRNG state that advances as random numbers are generated.

This provides desirable behavior for many workloads but makes deterministic replay difficult in multithreaded execution because concurrent execution changes the ordering of PRNG state updates.

### Seeded Execution

#### LLM

Single-threaded execution produces a deterministic stream of random values.

Multi-threaded execution introduces scheduling-dependent interleavings that prevent exact reproduction.

#### Diffusion

The same behavior applies.

Each image begins from a deterministic starting point in single-threaded execution but loses reproducibility under concurrent execution.

### Unseeded Execution

The behavior is similar except that the initial PRNG state cannot be recovered, making replay impossible even in single-threaded execution.

---

# Splittable and Stateless PRNGs

Repeatable deterministic PRNG computation in parallel environments originally relied on allocating a separate PRNG to each thread.

However, these PRNGs must be initialized carefully to avoid introducing statistical correlations.

This motivated the development of **splittable PRNGs**, which allow one PRNG state to deterministically generate multiple statistically independent PRNG states.

Splittable PRNGs are particularly useful when computations are recursively divided across multiple worker threads.

Examples include:

- Java 8+
- Java 17
- Google's JAX

If task partitioning is deterministic, the same sequence of random numbers is produced regardless of whether execution occurs sequentially or in parallel.

Most computational graph frameworks prefer operators to be pure functions.

While ONNX Runtime currently allows stateful PRNG operators, JAX instead represents PRNG state explicitly.

A stateless PRNG accepts a PRNG state as input and returns both:

- generated random values
- an updated PRNG state

This preserves purely functional graph semantics.

---

# Proposed Behaviour

This proposal introduces:

- updated versions of the existing ONNX random operators
- two new operators for explicit PRNG state management

PRNG state becomes an explicit tensor flowing through the graph.

The updated operators become both:

- stateless
- splittable

following the same functional PRNG model adopted by JAX.

Implementations may optionally provide graph validation to ensure that each PRNG state is consumed at most once within a graph, helping detect incorrect reuse of PRNG state.

The proposed operator definitions are described in the following sections.

---

# Summary

This proposal enables deterministic PRNG state evolution and reproducible stochastic computation by making PRNG state explicit within the graph.

It allows independent random streams to be generated for concurrent execution while remaining compatible with existing ONNX execution semantics.

### LLM

Each generation has a deterministic PRNG stream that may be replayed simply by supplying the same initial PRNG state.

Generating a different response requires only supplying a different initial PRNG state.

### Diffusion

Diffusion models become reproducible while allowing different images to be generated by changing only the initial PRNG state.

---

# Proposed Operator Scope

This proposal intentionally limits the initial operator surface to the minimum required to make ONNX random number generation stateless, splittable, and reproducible.

The proposal introduces **two new operators**:

- `SplitPRNG`
- `InitPRNG`

and updates **four existing operators**:

- `RandomUniform`
- `RandomUniformLike`
- `RandomNormal`
- `RandomNormalLike`

Additional sampling operators and debugging utilities are intentionally left for future proposals.

This keeps the initial proposal focused on introducing an explicit PRNG state model rather than expanding ONNX's sampling functionality.

## SplitPRNG Operator Spec

### Version

| Field | Value |
|-------|-------|
| **name** | `SplitPRNG` |
| **domain** | `main` |
| **since_version** | `X` |
| **function** | `False` |
| **support_level** | `SupportType.COMMON` |
| **shape inference** | `True` |

This version of the operator has been available since version **X**.

---

### Summary

Split a PRNG state into one or more deterministic PRNG states.

This operator enables explicit derivation of independent PRNG streams for parallel, distributed, and structured stochastic computation.

---

### Attributes

None.

---

### Inputs

| Name | Type | Description |
|------|------|-------------|
| **prng_state** | `tensor(int64)` | Input PRNG state. |
| **data** *(optional)* | `tensor(int64)` | Optional rank-1 tensor used to derive structured PRNG states. |

If `data` is supplied:

- The tensor **SHALL** contain one element for each output PRNG state.
- Element *i* is used to derive output state *i*.
- Values **SHOULD** be unique.
- Distinct values **MUST** generate distinct derived PRNG states for a fixed input `prng_state`.

---

### Outputs

| Name | Type | Description |
|------|------|-------------|
| **split_prng_states** | `variadic tensor(int64)` | One or more output PRNG states. |

The number of output PRNG states is determined by the number of graph outputs connected to the `SplitPRNG` operator.

---

### Type Constraints

None.

---

### Semantics

Given the same `prng_state`, optional `data` input, and graph output structure, `SplitPRNG` produces the same ordered sequence of output PRNG states.

`SplitPRNG` is a pure function of its inputs.

The operator does not read from or modify hidden RNG state.

The outputs are deterministic derived states suitable for independent downstream random computation.

Output ordering is part of the operator semantics and **MUST** be stable.

`SplitPRNG` may be used to create:

- Parallel random streams
- Subgraph random streams
- Per-chain MCMC streams
- Graph-boundary PRNG splitting
- Structured key derivation when `data` is supplied

The output PRNG states may be consumed by additional `SplitPRNG` operators or by random sampling operators that accept explicit PRNG state.

Each output state **SHOULD** be treated as an independent PRNG stream and **SHOULD** be consumed at most once unless intentionally reproducing the same random sequence.

`SplitPRNG` follows the stateless PRNG semantics defined by this proposal and is compatible with deterministic PRNG state threading through ONNX graphs.

## InitPRNG Operator Spec

### Version

| Field | Value |
|-------|-------|
| **name** | `InitPRNG` |
| **domain** | `main` |
| **since_version** | `X` |
| **function** | `False` |
| **support_level** | `SupportType.COMMON` |
| **shape inference** | `True` |

This version of the operator has been available since version **X**.

---

### Summary

Create an initial PRNG state from a user-supplied seed.

This operator provides a graph-level way to construct PRNG state. Alternatively, a model may accept `prng_state` directly as a graph input.

---

### Attributes

None.

---

### Inputs

| Name | Type | Description |
|------|------|-------------|
| **seed** | `tensor(int64)` | Input seed value. |

---

### Outputs

| Name | Type | Description |
|------|------|-------------|
| **prng_state** | `tensor(int64)` | Initial PRNG state. |

---

### Type Constraints

None.

---

### Semantics

Given the same `seed`, `InitPRNG` produces the same initial `prng_state`.

`InitPRNG` is a pure function of the `seed` input.

The operator does not read from or modify hidden RNG state.

The output `prng_state` may be consumed by `SplitPRNG` or by random sampling operators that accept explicit PRNG state.



## RandomUniform Op Spec Update

Generate random values from a uniform distribution using explicit PRNG state.

### Version

| Field | Value |
|-------|-------|
| **Version** | 23 |
| **name** | `RandomUniform` |
| **domain** | `main` |
| **since_version** | `22` |
| **function** | `False` |
| **support_level** | `SupportType.COMMON` |

**Other versions of this operator:** 22, 1

This version of the operator has been available since version **22**.

---

### Summary

Generate a tensor with random values drawn from a uniform distribution using explicit PRNG state. The shape of the tensor is specified by the `shape` argument and the range by `low` and `high`.

The data type is specified by the `dtype` argument. The `dtype` argument must be one of the data types specified in the `DataType` enum field in the `TensorProto` message.

---

### Attributes

| Name | Type | Description |
|------|------|-------------|
| **dtype** | `INT` (default is `1`) | The data type for the elements of the output tensor. If not specified, default is `TensorProto::FLOAT`. |
| **high** | `T` | Upper boundary of the output values. |
| **low** | `T` | Lower boundary of the output values. |
| **shape** | `INTS` (required) | The shape of the output tensor. |

Candidate values:

- `uniform_float`
- `raw_bits`

---

### Inputs

| Name | Type | Description |
|------|------|-------------|
| **prng_state** | `tensor(int64)` | Input PRNG state. |

---

### Outputs

| Name | Type | Description |
|------|------|-------------|
| **output** | `T` | Generated output tensor. |
| **prng_state** | `tensor(int64)` | Output successor PRNG state. |

---

### Type Constraints

`T` in (`tensor(bfloat16)`, `tensor(double)`, `tensor(float)`, `tensor(float16)`):

Constrain output types to float tensors.

Should be `INT64`.

---

### Semantics

`RandomUniform` is a pure function of `prng_state`, attributes, and output shape.

The operator does not read or modify hidden RNG state.

The output `prng_state` represents the successor PRNG state after generating the requested output.

The `seed` attribute is removed from this version of the operator. Reproducibility is controlled by the explicit `prng_state` input.



## RandomUniformLike Op Spec Update

Generate random values from a uniform distribution using the shape and optionally dtype of an input tensor.

### Version

| Field | Value |
|-------|-------|
| **Version** | 23 |
| **name** | `RandomUniformLike` |
| **domain** | `main` |
| **since_version** | `X` |
| **function** | `False` |
| **support_level** | `SupportType.COMMON` |
| **shape inference** | `True` |

This version of the operator has been available since version **X**.

**Other versions of this operator:** 22, 1

---

### Summary

Generate a tensor with random values drawn from a uniform distribution using explicit PRNG state. The shape of the output tensor is copied from the shape of the input tensor, and the parameters of the uniform distribution are specified by `low` and `high`.

The data type is specified by the `dtype` argument, or copied from the input tensor if not provided. The `dtype` argument must be one of the data types specified in the `DataType` enum field in the `TensorProto` message and be valid as an output type.

This updated version removes the `seed` attribute and instead uses an explicit `prng_state` input and output.

---

### Attributes

| Name | Type | Description |
|------|------|-------------|
| **dtype** | `INT` | (Optional) The data type for the elements of the output tensor. If not specified, the data type of the input tensor is used, provided the input tensor type is a valid output type. |
| **high** | `T` | Upper boundary of the output values. |
| **low** | `T` | Lower boundary of the output values. |

---

### Inputs

| Name | Type | Description |
|------|------|-------------|
| **input** | `T1` (heterogeneous) | Input tensor to copy shape and optionally type information from. |
| **prng_state** | `tensor(int64)` | Input PRNG state. |

---

### Outputs

| Name | Type | Description |
|------|------|-------------|
| **output** | `T2` (heterogeneous) | Output tensor of random values drawn from the uniform distribution. |
| **prng_state** | `tensor(int64)` | Output successor PRNG state. |

---

### Type Constraints

**T1** in (`tensor(bfloat16)`, `tensor(bool)`, `tensor(complex128)`, `tensor(complex64)`, `tensor(double)`, `tensor(float)`, `tensor(float16)`, `tensor(int16)`, `tensor(int32)`, `tensor(int64)`, `tensor(int8)`, `tensor(string)`, `tensor(uint16)`, `tensor(uint32)`, `tensor(uint64)`, `tensor(uint8)`):

Constrain to any tensor type. If the `dtype` attribute is not provided, this must be a valid output type.

**T2** in (`tensor(bfloat16)`, `tensor(double)`, `tensor(float)`, `tensor(float16)`):

Constrain output types to float tensors.

---

### Semantics

`RandomUniformLike` follows the same PRNG semantics as `RandomUniform`, except that the output shape and optionally `dtype` are derived from the input tensor unless overridden by attributes.

`RandomUniformLike` is a pure function of the input tensor shape, `dtype` behavior, `prng_state`, and attributes.

The operator does not read from or modify hidden RNG state.

The output `prng_state` represents the successor PRNG state after generating the requested output tensor.

The `seed` attribute is removed from this version of the operator. Reproducibility is controlled by the explicit `prng_state` input.


## RandomNormal Op Spec Update

Generate random values from a normal distribution using explicit PRNG state.

### Version

| Field | Value |
|-------|-------|
| **name** | `RandomNormal` |
| **domain** | `main` |
| **since_version** | `X` |
| **function** | `False` |
| **support_level** | `SupportType.COMMON` |
| **shape inference** | `True` |

This version of the operator has been available since version **X**.

**Other versions of this operator:** 22, 1

---

### Summary

Generate a tensor with random values drawn from a normal distribution using explicit PRNG state. The shape of the tensor is specified by the `shape` argument and the parameters of the normal distribution specified by `mean` and `scale`.

The data type is specified by the `dtype` argument. The `dtype` argument must be one of the data types specified in the `DataType` enum field in the `TensorProto` message.

This updated version removes the `seed` attribute and instead uses an explicit `prng_state` input and output.

---

### Attributes

| Name | Type | Description |
|------|------|-------------|
| **dtype** | `INT` (default is `1`) | The data type for the elements of the output tensor. Default is `TensorProto::FLOAT`. |
| **mean** | `FLOAT` (default is `0.0`) | The mean of the normal distribution. |
| **scale** | `FLOAT` (default is `1.0`) | The standard deviation of the normal distribution. |
| **shape** | `INTS` (required) | The shape of the output tensor. |

---

### Inputs

| Name | Type | Description |
|------|------|-------------|
| **prng_state** | `tensor(int64)` | Input PRNG state. |

---

### Outputs

| Name | Type | Description |
|------|------|-------------|
| **output** | `T` (heterogeneous) | Output tensor of random values drawn from the normal distribution. |
| **prng_state** | `tensor(int64)` | Output successor PRNG state. |

---

### Type Constraints

**T** in (`tensor(bfloat16)`, `tensor(double)`, `tensor(float)`, `tensor(float16)`):

Constrain output types to float tensors.

---

### Semantics

`RandomNormal` is a pure function of `prng_state`, attributes, and output shape.

The operator does not read from or modify hidden RNG state.

The output `prng_state` represents the successor PRNG state after generating the requested output tensor.

The `seed` attribute is removed from this version of the operator. Reproducibility is controlled by the explicit `prng_state` input.

Given the same `prng_state`, attributes, and output shape, `RandomNormal` produces the same sequence of PRNG state transitions and the same underlying random stream according to the selected PRNG implementation.

`RandomNormal` follows the stateless PRNG semantics defined by this proposal and is compatible with deterministic PRNG state threading through ONNX graphs.

---

## RandomNormalLike Op Spec Update

### Version

| Field | Value |
|-------|-------|
| **Version** | 23 |
| **name** | `RandomNormalLike` |
| **domain** | `main` |
| **since_version** | `22` |
| **function** | `False` |
| **support_level** | `SupportType.COMMON` |
| **shape inference** | `True` |

This version of the operator has been available since version **X**.

**Other versions of this operator:** 22, 1

---

### Summary

Generate a tensor with random values drawn from a normal distribution using explicit PRNG state. The shape of the output tensor is copied from the shape of the input tensor, and the parameters of the normal distribution are specified by `mean` and `scale`.

The data type is specified by the `dtype` argument, or copied from the input tensor if not provided. The `dtype` argument must be one of the data types specified in the `DataType` enum field in the `TensorProto` message and be valid as an output type.

This updated version removes the `seed` attribute and instead uses an explicit `prng_state` input and output.

---

### Attributes

| Name | Type | Description |
|------|------|-------------|
| **dtype** | `INT` | (Optional) The data type for the elements of the output tensor. If not specified, the data type of the input tensor is used, provided the input tensor type is a valid output type. |
| **mean** | `FLOAT` (default is `0.0`) | The mean of the normal distribution. |
| **scale** | `FLOAT` (default is `1.0`) | The standard deviation of the normal distribution. |

---

### Inputs

| Name | Type | Description |
|------|------|-------------|
| **input** | `T1` (heterogeneous) | Input tensor to copy shape and optionally type information from. |
| **prng_state** | `tensor(int64)` | Input PRNG state. |

---

### Outputs

| Name | Type | Description |
|------|------|-------------|
| **output** | `T2` (heterogeneous) | Output tensor of random values drawn from the normal distribution. |
| **prng_state** | `tensor(int64)` | Output successor PRNG state. |

---

### Type Constraints

**T1** in (`tensor(bfloat16)`, `tensor(bool)`, `tensor(complex128)`, `tensor(complex64)`, `tensor(double)`, `tensor(float)`, `tensor(float16)`, `tensor(int16)`, `tensor(int32)`, `tensor(int64)`, `tensor(int8)`, `tensor(string)`, `tensor(uint16)`, `tensor(uint32)`, `tensor(uint64)`, `tensor(uint8)`):

Constrain to any tensor type. If the `dtype` attribute is not provided, this must be a valid output type.

**T2** in (`tensor(bfloat16)`, `tensor(double)`, `tensor(float)`, `tensor(float16)`):

Constrain output types to float tensors.

---

### Semantics

`RandomNormalLike` follows the same PRNG semantics as `RandomNormal`, except that the output shape and optionally `dtype` are derived from the input tensor unless overridden by attributes.

`RandomNormalLike` is a pure function of the input tensor shape, `dtype` behavior, `prng_state`, and attributes.

The operator does not read from or modify hidden RNG state.

The output `prng_state` represents the successor PRNG state after generating the requested output tensor.

The `seed` attribute is removed from this version of the operator. Reproducibility is controlled by the explicit `prng_state` input.

Given the same input tensor shape, `dtype` behavior, `prng_state`, and attributes, `RandomNormalLike` produces the same sequence of PRNG state transitions and the same underlying random stream according to the selected PRNG implementation.

`RandomNormalLike` follows the stateless PRNG semantics defined by this proposal and is compatible with deterministic PRNG state threading through ONNX graphs.


## Revised Determinism Language

The purpose of this proposal is to make PRNG behavior deterministic, not to require bitwise-identical floating-point results across all ONNX execution providers.

Given the same graph, inputs, and `prng_state`, compliant implementations should produce the same PRNG state transitions and the same underlying PRNG-derived random stream according to the chosen PRNG semantics.

However, ONNX execution providers may still produce small numerical differences in floating-point results due to:

- Hardware-specific floating-point behavior
- Fused operations
- Optimized kernels

Therefore, this proposal requires deterministic PRNG state behavior and execution-order independence for random number generation, but it does not require global bitwise equivalence of all floating-point model outputs across execution providers.

---

## Testing and Conformance

Conforming implementations should demonstrate:

- Deterministic replay from identical seeds.
- Deterministic PRNG state transitions.
- Correct propagation of PRNG state through ONNX graphs.
- Statistical correctness of the updated sampling operators.
- Independence of PRNG streams generated by `SplitPRNG`.

Existing statistical testing methodologies, including those used by probabilistic programming systems such as Stan and established PRNG test suites, should be considered when developing an ONNX conformance test suite.