
# Purpose of tests in SONNX

In SONNX, functional tests are provided to check consistency between the SONNX specification and some existing implementations of the ONNX standard. 
As of Feb 2026, tests are performed against ONNX runtime (Python API, x64 architecture, default CPU, version ). 

The objective is to challenge our specification against de facto standard implementation, in addition to the inspection and review process. No conclusion can be drawn on the quality of the specification if test passes, but if tests do not pass, this may reveal a problem (either in the specificaiton or in the implementation). 
In addition, in cases where specificiers are faced to choices, tests can also serve as a means to ensure that the SONNX specification remains as much as possible aligned with them.

Out of SONNX, those tests can be used, for instance, to verify a user-implementation of the SONNX specification against the SONNX reference implementation (back-to-back testing). 

Note that only **input** values are defined. Expected output values are those produced by the reference implementation. 

# Disclaimer
The test developed by SONNX are **functional tests** aimed at covering the function realized by operators, with no consideration about their actual implementation. 

Those tests may reused as part of users' verification activities, but with no guarantee of completeness. It is the responsibility of the user to ensure that his/her test set complies with his/her test objectives. 

# Test strategy

This section defines the strategy that must be applied to define SONNX tests.

## Definitions and abbreviations
- dut: device/unit under test (the ONNX operator implementation function)
- oracle: trusted mechanism to determine expected output
- ulp: unit in the last place (floating-point comparison measure)
- special values: IEEE-754 values including ±0, ±inf, NaN, subnormals
- rbt: requirements-based testing
- robustness testing: tests beyond nominal requirements to show predictable behavior under abnormal conditions

## Configuration
For any test, the following information must be provided:
- opset (the one indicated in the specification)
- datatype
- full chacterization of the test execution platform including
  - compile-time options affecting numerics (*to be completed:* fast-math, fused ops, SIMD, etc.)
  - hardware target (x86_64)
  - operating system (linux)
  - compiler version
  - floating-point mode: default IEEE-754 rounding mode (round to nearest ties to even), denormal handling policy (e.g., preserve subnormals or flush-to-zero)
  - environment (python version, library versions,...)


## Reproducibility
Tests must be reproducible.

The following elements must be defined precisely 
- random seeds for randomized tests or test of random operators
- non deterministic execution order that would raises issues related to the non-associativity of floating point operations 
- single-thread in unit tests unless testing determinism explicitly)

## Verification objectives
For each operator and each supported datatype/opset/attribute variant, demonstrate:
- correctness: outputs match specification (*to be completed*: what is the acceptable error margin for a test to pass)
- robustness: predictable failure mode on invalid inputs (no crashes, no undefined behavior)
- completeness: all requirements tested; traceability exists
  
## Requirement model
As of today, the SONNX specification is not expressed in terms of atomic and well-identified requirement. 
Therefore, as much information as possible shall be provided to link the test to the specification (e.g., line number?)

## Test approach and levels
### Level a: conformance (requirements-based)
- nominal functional tests for each datatype and opset variant
- attribute tests including defaults and boundary values
- broadcasting coverage
- shape and rank coverage
  
## Level b: numerical robustness (floating pints)
- ieee special values, overflow/underflow edges, cancellation scenarios
- stable tolerance rules (absolute/relative/ulp) defined in section 10

## Level c: integer robustness
- min/max boundaries, overflow semantics, division by zero, shifts, saturate vs wrap
- quantization-specific tests if relevant

## Level d: property-based testing (invariants)
- randomized inputs with invariants per operator
- used to discover corner cases; does not replace requirements-based tests

## Level e: negative tests (robustness beyond requirements)
- invalid dtype combinations, invalid ranks, invalid attribute combinations
- aliasing and overlapping buffers if supported

## Pass/fail criteria

### Comparisons for integer values 
- 	exact match required for integers and booleans unless the spec defines otherwise

### Comparisons for floating point values 
Define the project-wide float comparison policy, per operator category.

#### Mathematically exact ops (e.g., structural operations such as reshape, transpose)
- exact (bitwise comparison)

#### General elementwise arithmetic: compare with max(abs_err, rel_err, ulp_err) policy
- abs_err_threshold: default 1e-6 for float32, 1e-12 for float64 (adjust per op)
- rel_err_threshold: default 1e-5 for float32, 1e-12 for float64
- ulp_threshold: default 2 ulp for float32, 4 ulp for float16 if supported

#### Numerically sensitive ops (e.g., softmax, log, exp, normalization)
Use tighter spec-driven criteria such as:
- softmax: sum(output) within 1e-5 of 1 for float32; all outputs in [0,1] except NaN cases
- log/exp: handle saturation near overflow with expected inf behavior


## Test design rules (tricky cases coverage)
For every operator, generate tests covering the cartesian products of the following attributes
- dimension class
  - scalar
  - 1d
  - 2d (matrix)
  - nd (rank 3–Nmax)

- shapes
  - same shape
  - broadcasting:
    - trailing broadcast (e.g., [2,3,4] + [4])
    - middle broadcast (e.g., [2,3,4] + [1,3,1])
    - scalar broadcast
  - degenerate dims: include size-1 dims, empty dims if allowed by spec/runtime
  - large dims near capacity (stress subset)

value classes
- zeros (including +0 and -0 for float)
- ones
- small magnitudes (near epsilon)
- large magnitudes (near max normal)
- alternating signs
- random uniform
- adversarial patterns (monotonic sequences, repeated values)
  
special ieee values (float)
- NaN, +inf, -inf
- subnormals
- max/min normals

integer boundaries
- min, max, -1, 0, 1
- near overflow (max-1, max)
- division by zero inputs
- shift amounts: 0, 1, bitwidth-1, bitwidth, >bitwidth (expected error or masked behavior per spec)
  
attributes coverage
- default attribute path
- each attribute min/max
- invalid attribute values produce error
- conflicting attribute combos produce error

error handling
- invalid dtype combinations
- invalid ranks
- incompatible shapes
- empty tensors where applicable


## Test case template
Each test case shall be documented with the following fields:

- test id: tc----###
- operator:
- opset:
- datatype(s):
- input shapes:
- attributes:
- input values: (explicit vectors or generation rule)
- oracle: (onnxruntime / numpy / analytic formula / secondary oracle)
- expected output: (explicit or derived)
- comparison rule: (exact / abs+rel / ulp)
- expected errors: (if negative test)
- part of the specification covered
- notes: (special handling such as NaN, denormals, flush-to-zero)


