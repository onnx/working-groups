
##  (§6.4.3.6) ML Model description 

### Q1: Model interfaces, control and data flows

In §6.4.3.6.a, we read:
> a. The ML Model architecture is described.\
Examples of ML Model architecture description content include (but are not limited to):
[...]\
o The logical structure of the proposed ML Model including the ML Model elements, their learning paradigm (e.g., supervised learning), the associated ML technology (e.g., neural networks), the function they perform in the architecture and **their interfaces in terms of data and control flows**

Using the terms "interfaces" and "control flow" seems a bit strange here since the model is a concrete representation of a graph, which is itself an abstract mathematical construct. 

So: 

*What is the actual intent for using the terms "interfaces", "control flow" here?*

### Q2: Hyperparameters

In §6.4.3.6, we read:
> b. The ML Model hyperparameters are described.\
For example, in the case of a neural network, the description of the ML Model hyperparameters should include, but is not limited to: the input layer, the number of hidden layers with the number of neurons per layer, the output layer with its number of neurons, the type of all activation functions, weight initialization, etc.

Hyperparameters are also defined in §(6.4.3.3): 
> Examples of model building hyperparameters for neural networks include (but are not limited to): number of layers, number of neurons in each layer, and their connections, selection of the activation functions in each layer, algorithm hyperparameters **such as learning rate**.

If the intent is to support a completely reproducible training phase, it seems that other data should also be included such as the training dataset, the exact description of the target machine, the training framework, etc. 

So:

*What is the actual intent of providing parameters related to the training phase (e.g., learning rate)?*


## (§7.1) ML Constituent Architecture Design Process

### Q1: ML Constituent architecture design 

In §7.1.3, we read: 
> Inadequate or incorrect **inputs** detected during the ML Constituent architecture design process should be provided to the Machine Learning lifecycle processes as feedback for clarification or correction.

*What are those "inputs"? Are they the inputs of the design process (i.e., the engineering items used to perform the design) or to the actual inputs of the ML consitutent?*


## (§7.3) ML Constituent Architecture Design Process

### Q1: Stability

In §7.3.3, we read:
> The assessment should provide justification that stability on the target platform is unchanged from the ML Model in the training environment. This may be accomplished by comparison of the characteristics of the training and target platforms (if they can be shown to be **similar enough** to preserve **these properties**), by analysis, or by additional testing to demonstrate the equivalence.

*What are the properties mentioned here?*\
*What do you mean precisely by "similar enough"?*


## (§8.4) Development And Verification Artifacts – Contents

### Q1 - On the relation between the ML model and the MLMD
The ML Model and the MLMD are two different artifacts (cf. §8.4.6 and §8.4.7).

In §8.4.7, the MLMD is said to **include** 
> [...] for each model individually, at least:
> - ML Model architecture,
> - ML Model hyperparameters,
> - ML Model parameters description,
> **The analytical/algorithmic syntax and semantic of the ML Model, including all ML Model internal operation that are
> necessary to compute the output(s) of the ML Model from its inputs,**
> ...

*What does the sentence starting with "The analytical/algorithmic..." actually mean?*
- *Does it mean that the (e.g.) Python ML model (described in §8.4.6) is a "part of" the MLMD?* 
- *Stated differently, does this mean that the MLMD is "composed of" the Python ML model plus the hyperparameters, parameters description, etc.? Or does this mean that we have to trace the elements of the MLMD to the ML Model? For instance, if the MLMD is expressed using ONNX and the ML Model is described using Python and Keras, do we have to provide a means to trace the Python statement to the elements of the ONNX model? Do we have to embed traceability data in the MLMD?* 

### Q2 - Internal operations

In the sentence:
> The analytical/algorithmic syntax and semantic of the ML Model, including all ML Model **internal operations** that are
> necessary to compute the output(s) of the ML Model from its inputs,

*What are the "internal operations"?*\
*Do they refer to the "operators" of the ML graph? or to some more primitive operations?*\
*Does it mean that the structure of the MLMD in terms of operators and graph must be strictly identical to the one of the ML model?*

### Q3 - Execution environment

The ML model is required to include data about the "model execution environment".

*What is actually required? Any data characterizing an element of the execution platform that may have an impact on the behavior of output of the ML model (e.g., target proc, operating system, ML framework, Python version, etc.) or, stated differently, all data allowing the strict (or approximate) replication of the ML model behaviour and output?*

### Q4 - "not part of the ML model description"

We read:
> NOTE: Additional information may be included for clarification purposes, 
> but must be clearly identified as "not part of the
> ML Model description".

*What is the exact criterion to discriminate what is provided "for clarification" and the other element. Can we say that "is a clarification element any element which value does not determine the behaviour and output of the model"?*

## Section 6.4.3.6 (ML Model Description) 

### Q1 - Definition of exact replication

We read: 
> EXACT REPLICATION: ML Inference Model implemented in software or Airborne Electronic Hardware (AEH) in which **no
> difference** is introduced with regards **to the ML Model semantics**.

This definition is further refined in §6.4.3.6.e:
> [...] the ML Model description should contain sufficient details on the ML Model semantic to fully preserve this semantic in the implemented ML Model. For example, an exact replication criterion may be the direct and faithful implementation of the ML Model description so that the implemented ML Model meets the same performance, generalization, stability, and robustness requirements.

A first look, the two definitions do not seem to be identical. The first one express the fact that the semantics must be the same where as the second one express that the "performance, generalization, ..." must be preserved.

So:

*What is exactly the "exact" replication?*\
*Is the definition of the criterion left to the "user" and be part of the model description?*

### Q2 - On the relation between the ML model and the MLMD

The definition of "exact replication" makes reference to a "ML Model" whose semantic must be captured and expressed (and "preserved") by the MLMD. 
  
  This model is different from the MLMD, so it must be described using another language than the MLMD. And this language should be defined too.

The first part of the definition expresses a first objective: "to preserve the semantic of the **ML model**". But the second part of the definition makes no more reference to the "ML model":  it only constrains the relation between the MLMD and the implementation of the MLMD. In fact, it may be wise to remove the reference to the "ML model" in this definition in order to focus exclusively on the relation between the MLMD and the implementation of the MLMD. Or, at least, to clearly distinguish the relation between the ML model and the MLMD, and the relation between the MLMD and the implemented MLMD (or introduce one relation between the "ML Model" and the "implemented ML Model" and to refine it into the previous two relations).  

### Q3 - "may be"
It is written that "an exact replication criterion **may be** the direct and faithful implementation of the ML Model description". 

The use of "For example" and "may be" seems to indicate that there could be other criteria. 

So: 
*Does this mean that the definition of the criterion is left to the model designer?*

The second part of the sentence seems to express the actual replication criteria since having a "direct and faithful" implementation is only one possible means to satisfy performance, robustness, etc. criteria. In that sense, "exact replication" would actually mean that the performance, generalization, stability and/or robustness" of the implementation are the same of the MLMD model.

The definition identifies 4 quantities (performance, generalization, ...)". 

*Is this list exhaustive? and what do we mean exactly by "performance" (there are quite a few performance metrics in ML) or "robustness" (local? global?).* 

Again, the exact criteria would have to be explicitly defined by the designer. 

*Is this the intent?*

### Q4 - "Direct and faifthful implementation"

It is written that in "an exact replication criterion may be the **direct** and faithful implementation of the ML Model".

*What is the exact meaning of "direct"?*

(The word "direct" could refer to traceability such as "all elements of the MLMD are traceable to the implementation of the MLMD and reciprocally". In practice, this could mean that we expect each element of the MLMD ("graph", "node",...) to be found in the implementation and that each operation is done (e.g.,) in the same order as in the MLMD (which, then, has to specify this order). In that sense, an implementation "exactly replicates" the MLMD if it replicates its "structure".)

    
## Concerning the concept of "approximate replication"

### Q1 - "acceptable"

The definition given in the glossary is the following: 
> APPROXIMATED REPLICATION: ML Inference Model implemented in software or Airborne Electronic Hardware (AEH)
> in which some differences with regards to the ML Model semantics are **acceptable**.

*What is the definition of "acceptable"?*\
*Is the acceptability criterion user defined?*\
*Shall the "acceptability" criterion be part of the MLMD?*

### Q2 - "gap"

The previous definition of "approximated replication" is refined in §6.4.3.6.e:
> [...] the ML Model description should contain sufficient details on the ML Model semantics to approximate this semantic in the implemented ML Model with a specified tolerance. For example, an approximation metric may be expressed for a given dataset by the maximal **gap** between the trained ML Model outputs and the implemented ML Model outputs. The corresponding approximation replication requirement may be that this maximal gap should not exceed a given value epsilon.

The concept of "gap" is not defined precisely. We may use the term "distance" and, in this case, the metric that is used must be defined. This metric will depend on the model. Note that it may be easier to define for a regression function than for a classifier.  
  
If the metric is "user dependant", it means that it should be specified in the MLMD. 

*Is this correct?*

### Q3 - On the relation between exact and approximate
Normally, we would expect "exact replication" to be a specific case of "approximate replication", i.e., the one where $\varepsilon=0$". However, this does not seem to be the case since the definition of "exact replication" does not refer to the outputs of the model (whereas the "approximate replication" does.)...

*What is the relation between "exact replication" and "approximate replication"?*

### Q4 - Denotational and operational semantics
It may be the case that the definitions of "exact replication" and "approximate replication" actually refer to two classical way to define a semantics in computer science: 
- **denotationally**, by expressing the relationship between inputs and outputs, as it is more or less the case for the approximate replication (denotation)
- **operationally**, by describing the sequence of operations to be carried out. 

Should this interpretation be the actual one, we would have to distinguish "exact" and "approximate" denotational and operational semantics. Two implementations would be approximately identical in the operational sense if the sequence of operations carried out would be "approximately" the same. 

*Is this interpretation correct?*





