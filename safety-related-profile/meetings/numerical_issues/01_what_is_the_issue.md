# The issue

## Floating point computations
- Let us consider one operator. The operation is usually specified done using a mathematical formula 
  - showing how to compute the result considering "ideal" real or integer numbers, 
  - expressing the relations the inputs and the outputs (e.g., $y=\pm\sqrt x)$, or $y^2=x$.\
  Usually, operations are described using a small corpus of basic operators such as $+$, $-$, $\times$, etc. or $\surd$, etc. 

- *Floating-point* or *fixed-point* numbers are encoded on a finite number of bits. Since all real numbers can't be represented exactly, non-representable  numbers are rounded to representable numbers according to a rounding strategy. Concerning operations, the principle (IEEE 754) is that the result of an operation on rounded values shall be the same as the result that would be obtained by rounding the result computed using exact values.
-  In addition, due to the finitness of the nuber of bits, overflow and underflow conditions may occur.  Conditions may apply on input values to prevent runtime errors. At least, runtime errors shall be signaled. In principle, these preconditions should be be part of the specification of the network (otherwise, there may be conditions in which the model doesn't produce any sensible result).

## Non-reproductibility
- Depending on some internal conditions, the same piece of code given the same inputs may lead to different sequences of operations, then different numerical results due to the non associativity of floating point operations. Those internal conditions may be difficult to determine in the absence of a full description of the execution platform. See for instance [Dem-15, Col-15]. In [Dem-15], this effect is studied for a simple parallel summation.  
- Some operators ay use random number generation (which sequence depends on a seed). 


## IEEE-754 and non IEEE-754 data types

IEEE 754 provides a set of guarantees about floating point computations [IEEE-754], howwever :

- Are all hardware (GPUs, accelerators) implementing the IEEE-754 standard?
  - No: NVIDUA uses TF32.
- Are all hardware devices IEEE-754 compliant (GPUs, FPGA and ASIC accelerators)?
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
  - What do the industrial standards say about computation errors (in space, avionics, automotive)?
  - How are standard mathematical libraries specified?
    - The newlib mathematical library does not give the accuracy of operations. (Note that the way mathematical operations are described could be inspiring) In addition, as stated in [Dar-06] "current [as of 2006] libm implementation do not always return the floating point number that is closest to the exact mathematical result. As a consequence, different libm implementation will return different results fotr the same input, which prevents fill portability for floating-point applications". The same claim can be read in [Gla-24]:
    > The IEEE 754 standard, even in its latest 2019 revision [17], does not require correctly rounded mathematical functions, it only recommends them. In turn, current athematical libraries do not provide correct rounding, which is the best possible result. Thus, users might get different results with different libraries, or different versions of the same library. This can have dramatic consequences: for example missed collisions in the Large Hadron Collider [5] or reproducibility issues in neuroimaging [13].
    - BLAS is not accurately rounded. For an accurately rounded BLAS, see e.g., [Cho-16].
  - How are floating point operations specified in C and other languages?
    - In the C99 standard [C99], nothing is said about the accuraty of operator. For the sin operator, the specification is the following:
``` 
    Description
    The sin functions compute the sine of x (measured in radians).
    Returns
    The sin functions return sin x.
```
  - The [LibmCS Mathematical Library for Critical Systems](https://essr.esa.int/project/libmcs-mathematical-library-for-critical-systems) developed for ESA does not provide any data about the accuracy of operations. Special cases are well defined. An example of specification is given below, for the sin operator:
  > REQ-BL-0200//GTD-TR-01-BL-0015/T\
  > The sin and sinf procedures shall evaluate the sine of their argument x in radians. 

  > REQ-BL-0203//GTD-TR-01-BL-0015/R\
  >The sin and sinf procedures shall use a minimax polynomial for the calculation. 

  > REQ-BL-0210//GTD-TR-01-BL-0015, GTD-TR-01-BL-0026/T\
  > The sin and sinf procedures shall return NaN if the argument is NaN. 

  > REQ-BL-0220//GTD-TR-01-BL-0015, GTD-TR-01-BL-0026/T
  > The sin and sinf procedures shall return the value of the argument if the argument is ±0. 

> REQ-BL-0240//GTD-TR-01-BL-0015, GTD-TR-01-BL-0026/T\
> The sin and sinf procedures shall return NaN if x is ±Inf. 
  
- The "ground truth" could be computed using a multi-precision library. For instance, the [GNU mpfr, Hou-07](https://www.mpfr.org/) library "provide a library for multiple-precision floating-point computation which is both efficient and has a well-defined semantics"

# What we can / cannot do...
  - Specifying the error seems not possible...
  - Describing how operations are done seems to be the obly way to ensure replicability of results... 
  - Could we provide a test suite? (qualification kit as for [ESA's MLFS](https://nebula.esa.int/content/pre-qualification-mathematical-library-flight-software))

# Means of analysis techniques and tools
- What are the technical means available to estimate the impact of errors on results? (e.g., fluctuat, CADNA...)
 - See [Beu-24, Ch. 4] who proposes forward / backward error estiation for neural networks, taking into account nn linear activation functions.
- Do we need the intervention of some FP experts? Who?
 

# The needs
**What to we actually need, for what purpose?**

## Industrial needs
- [Needs] Inferences must be reproducible *to support* debugging activities. 
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
- [ieee754] IEEE Standard for Floating-Point Arithmetic, IEEE Computer Society, IEEE 754-2019, 2019/06/13
- [Mic-22] P. Micikeviciuset al., "[FP8 formats for deep learning](https://arxiv.org/abs/2209.05433)," arXiv (Cornell University), Sep. 2022, doi: 10.48550/arxiv.2209.05433
- [Dar-06]  C. Daramy-Loirat and D. Defour, ‘CR-LIBM A library of correctly rounded elementary functions in double-precision’. Dec. 2006. [Online](https://ens-lyon.hal.science/ensl-01529804/file/crlibm.pdf)
- [Sch-18] Fabian Schriever, Software User-Manual - Basic mathematical Library for Flight Software, E1356-GTD-SUM01, 2018/05/23
- [Mpfr-2023] GNU MPFR - The Multiple Precision Floating-Point Reliable Library, August 2013, [Online](https://www.mpfr.org/mpfr-current/mpfr.pdf)
- [Hou-07] L. Fousse, G. Hanrot, V. Lefèvre, P. Pélissier, and P. Zimmermann, ‘MPFR: A multiple-precision binary floating-point library with correct rounding’, ACM Trans. Math. Softw., vol. 33, no. 2, p. 13, Jun. 2007, doi: 10.1145/1236463.1236468.
- [Dyd-23] Anton Ry[Online](https://dl.acm.org/doi/fullHtml/10.1145/3624062.3624166)
- [Gla-24] B. Gladman, V. Innocente, J. Mather, and P. Zimmermann, ‘Accuracy of Mathematical Functions in Single, Double, Double Extended, and Quadruple Precision’. [Online](https://inria.hal.science/hal-03141101)
- [Cho-16] Chohra, C., Langlois, P., Parello, D. (2017). Reproducible, Accurately Rounded and Efficient BLAS. In: Desprez, F., et al. Euro-Par 2016: Parallel Processing Workshops. Euro-Par 2016. Lecture Notes in Computer Science(), vol 10104. Springer, Cham. https://doi.org/10.1007/978-3-319-58943-5_49
- [Dem-15] J. Demmel and H. D. Nguyen, ‘Parallel Reproducible Summation’, IEEE Transactions on Computers, vol. 64, no. 7, pp. 2060–2070, Jul. 2015, doi: 10.1109/TC.2014.2345391.
- [Col-15] C. Collange, D. Defour, S. Graillat, and R. Iakymchuk, ‘Numerical reproducibility for the parallel reduction on multi- and many-core architectures’, Parallel Computing, vol. 49, pp. 83–97, Nov. 2015, doi: 10.1016/j.parco.2015.09.001.
- [Bru-15] N. Brunie, F. De Dinechin, O. Kupriianova, and C. Lauter, ‘Code Generators for Mathematical Functions’, in 2015 IEEE 22nd Symposium on Computer Arithmetic, Lyon: IEEE, Jun. 2015, pp. 66–73. doi: 10.1109/ARITH.2015.22.

# Attic
- Do we really need to add the replication in the SONNX standard? I would say "yes" in the sense that the replication criteria (which I would call "implementation criteria" since these criteria allow discriminating a correct implementation from an incorrect one)
- Check if formal methods (e.g., *fluctuat*) could be used.
- Be careful of the input domain of variables... 
- The replication criterion can mention a reference implementation, otherwise, the replication refers to the formal specification given by the model itself (see above)
- - In practice, what are the verifications performed on the ML model that will not be performed on the implementation of the model? What shall the ML model contain to be able to preserve these properties?
- Do we have to care about *training* reproducibility?
- Up to what level of requirements shall we go considering (i) the type of algorithms (that are inherently erroneous in th general case) and (ii) the assurance level targeted (DAL C in aeronautics)?