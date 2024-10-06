# Preliminaries

## Replication criteria

The concept of "replication criteria" is introduced in the ARP. Two "levels" of replication are defined (the following paragraphs are excerpts from the ARP6983 preliminary version):
- "__Approximated replication__: ML inference model implemented in software or Airborne Electronic Hardware (AEH) in which some differences with regards to the ML model semantics are acceptable." 
- "__Exact replication__: ML inference Model implemented in software or Airborne Electronic Hardware (AEH) in which no difference is introduced with regards to the ML Model semantics."

More precisely (still from the ARP6983): 
>e. The replication criterion (either exact or approximated) is defined from the ML Constituent requirements and if applicable from the ML Model requirements:
>- Exact replication: In this first case, the ML Model description should contain sufficient details on the ML Model semantic to fully preserve this semantic in the implemented ML Model. For example, an exact replication criterion may be the direct and faithful implementation of the ML Model description so that the implemented ML Model meets the same performance, generalization, stability, and robustness requirements.
>- Approximated replication: ln this second case, the ML Model description should contain sufficient details on the ML Model semantics to approximate this semantic in the implemented ML Model with a specified tolerance. For example, an approximation metric may be expressed for a given dataset by the maximal gap between the trained ML Model outputs and the implemented ML Model outputs. The corresponding approximation replication requirement may be that this maximal gap should not exceed a given value epsilon.

Those definitions should probably be clarified a bit... 
For instance:
- The definition of "semantic" in this context is not clear. The usual meaning of the word "semantic" is "the meaning of something". But what is the "meaning" of a ML model? Furthermore, in the definition, the term semantic is associated with properties such as performance (ML performance?), generalization, stability,... Do these properties relate to the "semantic"?
- "[...] the ML Model description should contain sufficient details on the ML Model semantic to fully preserve this semantic in the implemented ML Model." : 
  - (wording) The model cannot "preserve [the] semantic of the implemented model".
  - What does "fully preserve" mean, precisely? 
    A naive (?) interpretation would be that the semantic of the model is "fully preserved" by an implementation iff, for any input, the outputs of the  implementation are strictly identical to the ones that would be produced by a strict interpretation of the model. 
    By "strict interpretation", I mean an interpretation strictly compliant with the mathematical definition of the model. Interpretation could be intellectual or based on some mathematical tooling. But since this is usually not applicable in practice, a more operational definition could refer to some well defined, or possibly "reference", implementation. In that case, an implementation would be considered "semantically identical" to the model if, for the same inputs, it provides exactly the same outputs as the reference implementation. By exactly, I mean "bitwise identical". 

- According to the ARP's definitions, the replication criteria could be expressed in terms of "high-level" (or "end-user') properties such as:  ML performance, stability, robustness, etc., which are all properties of the model, not properties of the implementation (as would be the "accuracy", for instance).

 In this context, providing a bitwise accurate implementation would be a means to satisfy *all* replication criteria (except temporal ones, if we consider that temporal criteria ust be expressed). 

- Do we have to specify the numerical accuracy of the implemented model with respect to the model? 
  - Would the accurate specified for each element of the model (e.g., all activations) or for a subset of them (e.g., the outputs of the network)?


- Accuracy of operators need to be specified, otherwise it will be impossible to assess an implementation of the operator. 

Other:
- Do we really need to add the replication in the SONNX standard? I would say "yes" in the sense that the replication criteria (which I would call "implementation criteria" since these criteria allow discriminating a correct implementation from an incorrect one)
-  Check if formal methods (e.g., *fluctuat*) could be used.
-  Be careful of the input domain of variables... 
- The replication criterion can mention a reference implementation, otherwise, the replication refers to the formal specification given by the model itself (see above)

# The current practice 
- How do we manage numerical errors (inc. floating point errors) in current, non-AI systems?
    - How are requirements about computation errors expressed for those systems?
    - How are those requirements verified?

# The needs

*What are the needs related to computational accuracy/precision*

## Industrial needs

- In practice, what are the verifications performed on the ML model that will not be performed on the implementation of the model? What shall the ML model contain to be able to preserve these properties?

- Do we have to care about *training* reproducibility?

- Up to what level of requirements shall we go considering (i) the type of algorithms (that are inherently erroneous in th general case) and (ii) the assurance level targeted (DAL C in aeronautics)?

## Certification "needs"

- What are the certification recommendations/objectives that may be impacted by computation errors (determinism, predictability, reproducibility...).

*See first section.*

# The requirements
*How do the previous needs translate to requirements __on the model__?*

- Can we specify errors bounds at the model level?
  - Does it make sense?
  - Will it be possible to provide a bound? How? and will is be possible *not* to provide a bound?
  - To what element must a bound be given (unitary operators, activations,...?)


# The issue

## The various sources of non-determinism
*What are the sources of non-determinism, non-predictability, non-reproducibility?

- rounding errors 
    - How does time impact numerical errors errors?
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
