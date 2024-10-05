# Miscelleeous

- The replication croteria must be expresse din terms of ML performance, stability, robustness, etc. that are properties of the ML model.
- The replication creterion can mention a reference implementation, otherwise, the replication refers to the formal specification given by the model itself
  -  Providing a bitwise accurate implementation is a means to satisfy *all* replication criteria (except temporal ones, if we consider that temporal critera ust be expressed)
-  The accurracy of operator need to be specified *if we want a developper to to be able to provide a useful library*. It could be possible to provide a implementation without specifying accuracies of operators, but in this case, verifiyng the satisfaction of the replication criteria will be extremely difficult (it could still be feasible if the test can be exhaustive).
-  Check if formal methods (e.g., fluctuat) could be used.
-  Be careful of the input domain of variables... 


# The needs

*What are the needs related to computational accurracy/precision*

- Reproducibility: an experiment (learning or inference) must be reproducible.
  - For training: *to be clarified*
  - For inference:
    - given the same input the implementation of the model must provide the same outputs...

## Industrial needs

- Do we care about *training* reproducibility?

## Certification "needs"

What are the certification recommandations/objectives that may be impacted by computation errors (determinism, predictibility, reproducibility...).

# The requirements
*How do these needs translate to requirements __on the model__?*

- Can we specify errors bounds at the model level?
  - Will it be possible to provide a bound? How? 
  - Will is be possible *not* to provide a bound?
  - To what element must a bound be given (each activation, the on on the last layer?)
- Instead, can we just 
  - express design/implementation requirements to "minimize" errors
  - express that the values must be "identical to some $\epsilon$" to the result of the reference implementation? 

# The current practice 
- How do we manage numerical errors (inc. floating point errors) in the current, non-AI systems?
    - How are requirements about computation errors expressed for those systems?
    - How are those requirements verified ?


# The issue

## The various sources of non-determinism
*What are the sources of non-determinism, non-predictbility, non-reproducibility?

- rounding errors 

- Sources of errors
    - What are the sources of errors ?
    - How does time impact errors ?
    - Are all hardware (GPUs, accelerators) implementing the IEEE754 standard ?
    - Are all hardware devices IEEE754 compliant (GPUs, FPGA and ASIC accelerators) ?
    - What about the ML-specific formats (Tensor32,...) ?

## Numerical errors in GPUs

### Issues
- See NVIDIA's presentation at GTC 2019 ([video](https://www.youtube.com/watch?v=TB07_mUMt0U), [slides](https://drive.google.com/file/d/18pmjeiXWqzHWB8mM2mb3kjN4JSOZBV4A/view?pli=1))

### Mitigation means

- See previous links.

## Numerical errors in CPUs / DSPs
*(To be completed)*

## Numerical errors in ASIC accelerators (NPUs)
*(To be completed)*

## Numerical errors in FPGAs
*(To be completed)*

## How is this issue related to...

### MLperformance
- To what extent is the question of computation errors pertinent with respect to the other sources of errors in Machine Learning algorithms (or "how do computaton errors compare to other sources of errors")?
  
### Robustness

*(To be completed)*

### Quantification

*(To be completed)*

# The State-o-the-art 

*(to be completed)*

# Means of analysis 
- What are the technical means available to estimate the impact of errors on results? (e.g., fluctuat...)
- Do we need the intervention of some FP experts? Who?
