# The issue

## Numerical errors
- Let us consider one operator. The operation is usually specified done using a mathematical formula 
  - showing how to compute the result considering "ideal" real or integer numbers, 
  - expressing the relations the inputs and the outputs (e.g., $y=\pm\sqrt x)$, or $y^2=x$.\ 
  Usually, operations are described using a small corpus of basic operators such as $+$, $-$, $\times$, etc. or $\surd$, etc. 

- When using *floating-point* or *fixed-point* numbers,  computations are done with some slight error with respect to what would be obtained by calculating the formula in R. Those numbers being represented by a finite number of bits, not all numbers can be represented exactly, leading to rounding error (including representation errors). 
- In addition, due to the finitness of the nuber of bits, overflow and underflow conditions may occur.  
  
- In order to prevent errors, input values of operators may require to belong to some input domain (preconditions). In principle, these preconditions should be be part of the specification of the network (otherwise, there may be conditions in which the model doesn't produce any sensible result).

## Non-determinism
- Depending on some internal conditions, the same piece of code given the same inputs may lead to different sequences of operations, then different numerical results due to the non associativity of floating point operations. Those internal conditions may be difficult to determine in the absence of a full description of the execution platform. 
- Some operators ay use random number generation (which sequence depends on a seed). 


## IEEE-754 and non IEEE-754 data types

IEEE 754 provides a set of guarantees [ieee754]. However :

- Are all hardware (GPUs, accelerators) implementing the IEEE-754 standard ?
  - No: NVIDUA uses TF32.
- Are all hardware devices IEEE-754 compliant (GPUs, FPGA and ASIC accelerators) ?
- Some of the data types used in machine learning to not belong to the IEEE 754 standards. For example: [BF16](https://en.wikipedia.org/wiki/Bfloat16_floating-point_format) (bfloat16), [TF32](https://en.wikipedia.org/wiki/TensorFloat-32) (TensorFlow 32 bits)
  - What are the properties of those representations (do they respect the same principle as IEEE 754 numbers?)
  - Should we only allow IEEE 754 standard?


## Numerical errors in GPUs

### Issues
- See [Precision and performance: Floating point and IEEE 754 Compliance fir NVIDIA GPUs](https://developer.download.nvidia.com/assets/cuda/files/NVIDIA-CUDA-Floating-Point.pdf)
- See NVIDIA's presentation at GTC 2019 ([video](https://www.youtube.com/watch?v=TB07_mUMt0U), [slides](https://drive.google.com/file/d/18pmjeiXWqzHWB8mM2mb3kjN4JSOZBV4A/view?pli=1))


### Mitigation means

- See previous links.

## Numerical errors in CPUs / DSPs
*(To be completed)*

## Numerical errors in ASIC accelerators (NPUs)
*(To be completed)*

## Numerical errors in FPGAs
*(To be completed)*

## Relation between accuracy and other properties...

### ML performance
- To what extent is the question of computation errors pertinent with respect to the other sources of errors in Machine Learning algorithms (or "how do computaton errors compare to other sources of errors")?
  
### Robustness

- See Th. Beuzeville about floating point errors and robusteness attacks. e.g., [Beu-24]

### Quantification
*(To be completed)*


# The current practice 
- How do we manage numerical errors (inc. floating point errors) in current, non-AI systems?
    - How are requirements about computation errors expressed for those systems?
    - How are those requirements verified?

# Means of analysis techniques and tools
- What are the technical means available to estimate the impact of errors on results? (e.g., fluctuat, CADNA...)
  - See [Beu-24, Ch. 4] who proposes forward / backward error estiation for neural networks, taking into account nn linear activation functions.
- Do we need the intervention of some FP experts? Who?
- 

# The needs
## Industrial needs
- [Needs] If a property is verified on a given source model (e.g, a PyTorch model) $M_{org}$, the SONNX model generated from the PyTorch model $M_{saved}$ must preserve the property in the sense that if P hold on $M_{org}$, then $P$ also holds on $M_{saved}$.\
In particular, this means that the (meta-) model (i.e., the SONNX standard) must preserve the data ensuring the property.\
For instance, using floating point can lead to unsound verification results in the sense that a model that is robust in $\mathbb{R}$ (i.e, verified formally to be robust considering  values in R) may not be robust when implemented using finite precision numbers [???]. In this example, the MLMD would have to be implemented in R (if it were possible) for the robustness property to be preserved. 
- [Needs] For a given model $M$, for a given execution platform, for the same set of inputs, the maximal difference between the values produced by multiple executions of the same implementation of $M$ shall be bounded.\
  The bound may depend on the application. It goes from strict (or "bitwise") similarity to similarity expressed by an upper bound on the difference between the activations produced by the different executions.\
- [Needs] For the same set of inputs, the difference between the values produced by an implementation of a model and an ideal (mathematical) model shal be bounded. 

*Note a: "Reproduction" is different from "replication" because the former concerns the relation between different executions of the same model implementation, whereas the latter concerns the relation between the model and its implementation(s).*\
*Note b: Instead of specifiying requirements about accuracy and precision, couldn't we just specify implementation requirements, i.e, the way computations must be done.* 


## Certification "needs"

*What are the certification recommendations/objectives that may be impacted by computation errors (determinism, predictability, reproducibility...)*

### Replication criteria

The concept of "replication criteria" is introduced in the ARP6983. Two "levels" of replication are defined (the following definitions are taken from the ARP6983 preliminary version):
- "__Approximated replication__: ML inference model implemented in software or Airborne Electronic Hardware (AEH) in which some differences with regards to the ML model semantics are acceptable." 
- "__Exact replication__: ML inference Model implemented in software or Airborne Electronic Hardware (AEH) in which no difference is introduced with regards to the ML Model semantics."

More precisely (still from the ARP6983): 
>e. The replication criterion (either exact or approximated) is defined from the ML Constituent requirements and if applicable from the ML Model requirements:
>- Exact replication: In this first case, the ML Model description should contain sufficient details on the ML Model semantic to fully preserve this semantic in the implemented ML Model. For example, an exact replication criterion may be the direct and faithful implementation of the ML Model description so that the implemented ML Model meets the same performance, generalization, stability, and robustness requirements.
>- Approximated replication: ln this second case, the ML Model description should contain sufficient details on the ML Model semantics to approximate this semantic in the implemented ML Model with a specified tolerance. For example, an approximation metric may be expressed for a given dataset by the maximal gap between the trained ML Model outputs and the implemented ML Model outputs. The corresponding approximation replication requirement may be that this maximal gap should not exceed a given value epsilon.

Those definitions should probably be clarified a bit... 
For instance:
- The use of the term "replication" is misleading. To "replicate" means to reproduce. But we do not want to "reproduce" the model itself, but to implement it, i.e., to reproduce its behaviour. 
- The definition of "semantic" in this context is not clear. The usual meaning of the word "semantic" is "the meaning of something". But what is the "meaning" of a ML model? Furthermore, in the definition, the term semantic is associated with properties such as performance (ML performance?), generalization, stability,... Do these properties relate to the "semantic"?
- "[...] the ML Model description should contain sufficient details on the ML Model semantic to fully preserve this semantic in the implemented ML Model." : 
  - (wording) The model cannot "preserve [the] semantic of the implemented model".
  - What does "fully preserve" mean, precisely? 
    A naive (but clear) interpretation would be that the semantic of the model is "fully preserved" by an implementation iff, for any input, the outputs of the  implementation are strictly identical to the ones that would be produced by a strict interpretation of the model. 
    By "strict interpretation", I mean an interpretation strictly compliant with the mathematical definition of the model. Interpretation could be intellectual or based on some mathematical tooling. But since this is usually not applicable in practice, a more operational definition could refer to some well defined, or possibly "reference", implementation. In that case, an implementation would be considered "semantically identical" to the model if, for the same inputs, it provides exactly the same outputs as the reference implementation. By exactly, I mean "bitwise identical". 

- According to the ARP's definitions, the replication criteria could be expressed in terms of "high-level" (or "end-user') properties such as:  ML performance, stability, robustness, etc., which are all properties of the model, not properties of the implementation (as would be the "accuracy", for instance).

 - In this context, providing a bitwise accurate implementation would be a means to satisfy *all* replication criteria (except temporal ones, if we consider that temporal criteria ust be expressed). 

## Numerical accuracy

### Numerical accuracy of the model
- Do we have to specify the accuracy of the implementation of the model with respect to the model itself. For example: 
  - "The model implementation is correct if all of its activations are at $\epsilon$ to the values that would be produced by a perfect interpretation of the model".
- Would the accurate specified for each element of the model (e.g., all activations) or for a subset of them (e.g., the outputs of the network)?\
  For example:
  - Case #1: "The model implementation is correct if all of its activations  are at $\epsilon$ from to the values that would be produced by a perfect interpretation of the model".
  - Case #2: "The model implementation is correct if the outputs of the last layer are at $\epsilon$ from the values that would be produced by a perfect interpretation of the model".
- In practice, and besides the trivial case where $\epsilon=0$, will the user be able to specify such accurracy?

### Numerical accuracy the operators
- Accuracy of operators need to be specified, otherwise it will be impossible to assess any implementation. 
  - Well, this is not mandatory. Neither the BLAS library, not C99, nor.. give accuracies. 
  


# References

- [Deterministic and probabilistic backward error analysis of neural networks in floating-point arithmetic
](https://theses.hal.science/IRIT-APO/hal-04663142v1)
- [Jia-XX] Kai Jia and Martin Rinard, Exploiting Verified Neural Networks via Floating point Numerical Errors, [here](https://arxiv.org/abs/2003.03021)
- [Beu-24] Théo Beuzeville, [Analyse inverse des erreurs des réseaux de neurones artificiels avec applications aux calculs en virgule flottante et aux
attaques adverses ](https://theses.hal.science/tel-04622129v1/document)
- [Gu-13] Eric Goubault. “[Static Analysis by Abstract Interpretation of Numerical Programs and Systems, and FLUCTUAT](https://www.ensta-bretagne.fr/jaulin/MEAabstr_goubault.pdf)”. In: Static Analysis - 20th International Symposium, SAS 2013, Seattle, WA, USA, June 20-22, 2013. Proceedings. Ed. by Francesco Logozzo and Manuel Fähndrich. Vol. 7935. Lecture Notes in Computer Science. Springer, 2013, pp. 1–3.
- [Iou-19] Arnault Ioualalen and Matthieu Martel. “[Neural Network Precision Tuning](https://perso.univ-perp.fr/mmartel/qest19.pdf)”. In: Quantitative Evaluation of Systems, 16th International Conference, QEST 2019, Glasgow, UK, September 10-12, 2019, Proceedings. Ed. by David Parker
and Verena Wolf. Vol. 11785. Lecture Notes in Computer Science. Springer,
2019, pp. 129–143.
- [Sin-18] Gagandeep Singh, Timon Gehr, Matthew Mirman, Markus Püschel, and Martin T. Vechev. “[Fast and Effective Robustness Certification](https://papers.nips.cc/paper_files/paper/2018/file/f2f446980d8e971ef3da97af089481c3-Paper.pdf)”. In: Advances in Neural Information Processing Systems 31: Annual Conference on Neural Information Processing Systems 2018, NeurIPS 2018, December 3-8, 2018, Montréal, Canada. Ed. by Samy Bengio, Hanna M. Wallach, Hugo Larochelle, Kristen Grauman, Nicolò Cesa-Bianchi, and Roman Garnett. 2018, pp. 10825–10836.
- [ieee754] 
- [Mic-22] P. Micikeviciuset al., "[FP8 formats for deep learning](https://arxiv.org/abs/2209.05433)," arXiv (Cornell University), Sep. 2022, doi: 10.48550/arxiv.2209.05433


# Attic
- Do we really need to add the replication in the SONNX standard? I would say "yes" in the sense that the replication criteria (which I would call "implementation criteria" since these criteria allow discriminating a correct implementation from an incorrect one)
- Check if formal methods (e.g., *fluctuat*) could be used.
- Be careful of the input domain of variables... 
- The replication criterion can mention a reference implementation, otherwise, the replication refers to the formal specification given by the model itself (see above)
- - In practice, what are the verifications performed on the ML model that will not be performed on the implementation of the model? What shall the ML model contain to be able to preserve these properties?
- Do we have to care about *training* reproducibility?
- Up to what level of requirements shall we go considering (i) the type of algorithms (that are inherently erroneous in th general case) and (ii) the assurance level targeted (DAL C in aeronautics)?