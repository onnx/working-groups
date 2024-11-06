---
marp: true
---

# 2024-06-11 SONNX WG Meeting


SONNX and numerical accuracy 

---
<!-- theme: default --> 
<!-- paginate: true -->

<!-- footer: '_SONNX WG meeting 2024-11-06_' -->

- Numerical computations are not done in $\mathbb{R}$  
  - Numbers are represented with a finite number of bits
- All numbers can't be represented exactly
- When using ``float``, ``double``, etc. rounding occurs.
- The result of a computation depends on the implementation (even when using IEEE754...)
- Values may over- or under-flow...
- ___How shall we handle this in SONNX?___


---
# Questions 
- Is numerical accuracy a concern for us?
- Is it a new problem? Is it specific to ML?
- Is it solved by IEEE754?
- How is it handled today?
- Is it more crucial important for ML algorithms?

---
# Is it a problem for us?
(Element of context: we are not targeting DAL-A systems...)
- How is it related to our main objective, i.e,  __to be able to preserve the semantics of the model__ ?
- Level 1: operators are specified in $\mathbb{R}$
  - the implementation may be "completely different" from the specification
- Level 2: operators are specified for a given data type

---
# Is it a new problem? Is it specific to ML?
- It is not a new problem.
- ML involves many computations (esp. deep learning), for which errors may accumulate. This has to be compared with real-time system for which stated is renewed due to the renewal of inputs.
- On the other side: ML algorithms are pretty robust to computation errors (but potential way for attacks) [to be discussed]

---
# Is is solved by IEEE754
- IEE754 defines what a correctly rounded operation is: 
  > "[...] each of the computational operations specified by this standard that returns a numeric result shall be performed as if it first produced an intermediate result correct to infinite precision and with unbounded range, and then rounded that intermediate result, if necessary, to fit in the destination’s format"
- Not all hardware usd in ML computations are IEEE754 compliant: no, BF16, TF32,...

---
# How is it handled today?
- In industrial applications?
  - Testing? Formal verification (fluctuat)? 
- In development assurance standards
  - Aero.: nothing specifically said about computation errors. Covered by "normal" verification activities...
  - Other: ???
- In language standards
    - C99: 
      - Nothing is said about the accuracy of operators... 
      - Rule about associativity: left associativity is required... 
    - Ada: 
      - Section G.2.4 gives accuracy requiremnts for elementary functions (see [here](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/meetings/numerical_issues/01_what_is_the_issue.md))

--- 
- Mathematical libraries
  - ``libm``: no requirement about accuracy, not correctly rounded...
  - ``BLAS``: no requirement about accuracy, not correctly rounded...
  - ESA's ``libmCS`` does not give any accuracy requirement...

---
# Should we specify maximal errors on a per operator basis?
- What about the global error?
- 

---
# Over and under flow
- Define conditions on the inputs in which no overflow / underflow will never occur?
- Define the expected behaviour in case of over- under- flow?
- 

--- 
# Semantic preservation by design
- The description of the operation is prescriptive, i.e., operations shall be done in a specific way. 


---
# Semantic preservation by verification

---

# The question of replication [ARP6983, §6.4.3.6]
- Exact replication
  >- [...] the ML Model description should contain sufficient details on the ML Model semantic to fully ___preserve this semantic___ in the implemented ML Model. For example, an exact replication criterion may be the direct and faithful implementation of the ML Model description so that the implemented ML Model meets ___the same performance, generalization, stability, and robustness requirements___.

---

- Approximated replication 
  >- [...] the ML Model description should contain sufficient details on the ML Model semantics ___to approximate this semantic___ in the implemented ML Model with a specified tolerance. For example, an approximation metric may be expressed for a given dataset by __the maximal gap between the trained ML Model outputs and the implemented ML Model outputs___. The corresponding approximation replication requirement may be that this maximal gap should not exceed a given value epsilon.

---

# Needs / Industrial
- Reproducibility
    - 
- Preservation of properties: __if a property holds on a given "source" model, the SONNX model must preserve the property in the sense that an implementation that follows strictly the specification will satisfy the property...
  - If verificaton activities are done on implement #1

---
# Requirements (illustration)
- [**REQ**] The MLMD shall specify the the exact ordering of operations, the representation of numbers, the roundings.
- [**REQ**] The MLMD shall specify the accuracy of all operations
- [**REQ**] The MLMD shall specify the exact input domain in which the model  shall provide an output.  
- [**REQ**] The SONNX standard shall specify th eexpected behaviour should a runtim error occur (over/under-flow, division by zero,...).
- [**REQ**] The SONNX standard shall provide exactly rounded operators.

---