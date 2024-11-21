Dear Colleagues,

We are working on a specific profile of the ONNX standard for "critical" systems.
Our objective is to 
- provide a clear (consistent, non ambiguous, etc.) definition of operators and graoh semantics 
- provide a clear definition (consistent, non ambiguous, etc.) of the ONNX file format
  
This activity is hosted by the ONNX community. The material produced as of today is available at XXX.

Our work is guided by industrial and standards.

In this regards, we are considering the recommandations given by the ARP 6983, and in particular those related to "replication".

The standard distinguishes two levels of replications (exact and approximate) that raise several questions.

## §8.4

### Q1 - On the relation between the ML model and the MLMD
The ML Model and the MLMD are two different artifacts (scf/ §8.4.6 and §8.4.7).

In §8.4.7, the MLMD is said to include 
> for each model individually, at least:
> - ML Model architecture,
> - ML Model hyperparameters,
> - ML Model parameters description,
> The analytical/algorithmic syntax and semantic of the ML Model, including all ML Model internal operation that are
> necessary to compute the output(s) of the ML Model from its inputs,
> ...


### Q2 
What does the sentence statring with "The analytical/algorithmic..." actually mean? 
- Does it mean that the (e.g.) Python ML model (described in §8.4.6) is a "part of" the MLMD? 
- Stated differently, does this mean that the MLMD is "composed of" the Python ML model plus the hyperparameters, parameters description, etc.? Or does this mean that we have to trace the elements of the MLMD to the ML Model? For instance, if the MLMD is expressed using ONNX and the ML Model is described using Python and Keras, do we have to provide a means to trace the Python statement to the elements of the ONNX model? do we have to embed traceability data in the MLMD? 

### Q3
- One reads
> [...] including all ML Model internal operation that are necessary to compute the output(s) of the ML Model from its inputs
    - What are those "internal operations"? Do they refer to the "operators" of the ML graph? or to some more primitive operations?
    - Does it mean that the structure of the MLMD in terms of operators and graph must be strictly identical to the one of the ML model? 

### Q4 - Execution environment

The ML model is required to include data about the "model execution environment".

What is actually required? Any data characterizing an element of the execution platform that may have an impact on the behavior of output of the ML model (e.g., target proc, operting system, ML framework, Python version, etc.) or, stated differently, all data allowing the strict (or approximate) replication of the ML model behaviour and output?

### Q5 - "not part of the ML model description"

Considering the following note:
> NOTE: Additional information may be included for clarification purposes, 
> but must be clearly identified as "not part of the
> ML Model description".

What is the exact criterion to discriminate what is provided "for clarification" and the other element. Can we say that "is a clarification element any element which value does not determine the behaviour and output of the model"?


# Concerning the concept of "exact replication"

The definition given in the glossary is the following : 
> EXACT REPLICATION: ML Inference Model implemented in software or Airborne Electronic Hardware (AEH) in which no
> difference is introduced with regards to the ML Model semantics.

This definitin is further refined in §XXX:
> [...] the ML Model description should contain sufficient details on the ML Model semantic to fully preserve this semantic in the implemented ML Model. For example, an exact replication criterion may be the direct and faithful implementation of the ML Model description so that the implemented ML Model meets the same performance, generalization, stability, and robustness requirements.

### Q1 - Equivalence of definitions

A first look, the two definitions do not seem to be identical. The first one express the fact that the semantics must be the same where as the second one express that the "performance, generalization, ..." must be preserved. 

Is this correct?


### Q2 - On the relation between the ML model and the MLMD
The definition makes reference to a "ML Model" whose semantic must be captured and expressed (and "preserved") by the MLMD. 
  - This model is different from the MLMD, so it must be described using another language than the MLMD. And this language should be defined too.

### Q2 

The first part of the definition expresses a first objective: "to preserve the semantic of the **ML model**". But the second part of the definition makes no more reference to the "ML model":  it only constrains the relation between the MLMD and the implementation of the MLMD. In fact, it may be wise to remove the reference to the "ML model" in this definition in order to focus exclusively on the relation between the MLMD and the implementation of the MLMD. Or, at least, to clearly distinguish the relation between the ML model and the MLMD, and the relation between the MLMD and the implemented MLMD model (or introduce one relation between the "ML Model" and the "implemented ML Model" and to refine it into the previous two relations).  

### Q3

The definition states that "an exact replication criterion **may be** the direct and faithfull implementation of the ML Model description". 
- The use of "For example" and "may be" seems to indicate that there could be other criteria. 
  - Does this mean that the definition of the criterion is up to the model designer?
  - And if it is the case, called it a "exact replication criterion"  
- On the contrary, the second part of the sentence seems to express the actual replication criteria since having a "direct and faithful" implementation is only one possible means to satisfy performance, robustness, etc. criteria. In that sense, "exact replication" would actually mean that the performance, generalization, stability and/or robustness" of the implementation are the same of the MLMD model. 
  - The definition identifies 4 quantities (performance, generalization, ...)". Is this list exhaustive? and what do we mean exactly by "performance" (there are quite a few performance metrics in ML) or "robustness" (local? global?). 
    - As previously, the exact criteria would have to be explicitly defined by the designer. 

### Q4 

It is written that in "an exact replication criterion may be the **direct** and faithful implementation of the ML Model".

What it the exact meaning of "direct"? 
  - "direct" could refer to some traceability property such as "all elements of the MLMD are traceable to the implementation of the MLMD and reciprocally". In practice, this could mean that we expect each element of the MLMD ("graph", "node",...) to be found in the implementation and that each operation is done (e.g.,) in the same order as in the MLMD (which, then, has to specify this order). In that sense, an implementation "exactly replicate" the MLMD if it replicates its "structure".  
    
## Concerning the concept of "approximate replication"

The definition given in the glossary is the following: 

> APPROXIMATED REPLICATION: ML Inference Model implemented in software or Airborne Electronic Hardware (AEH)
> in which some differences with regards to the ML Model semantics are acceptable.

- What is the definition of "acceptable"? Is the acceptability criterion user defined? 
- Shall the exact definition of "acceptable" be part of the MLMD ?


The definition, given in §XXX is the following:
> [...] the ML Model description should contain sufficient details on the ML Model semantics to approximate this semantic in the implemented ML Model with a specified tolerance. For example, an approximation metric may be expressed for a given dataset by the maximal gap between the trained ML Model outputs and the implemented ML Model outputs. The corresponding approximation replication requirement may be that this maximal gap should not exceed a given value epsilon.


### Q1

The concept of "gap" is not precise. We may use the term "distance" and, in this case, the metric that is used must be defined. 

This metric will depend on the model. Note that it may be easier to define for a regression function than for a classifier.  
  
If the metric is "user dependant", it means that it should be specified in the MLMD. 

Is this correct?

### Q2
Normally, we would expect "exact replication" to be a specific case of "approximate replication", i.e., the one where $\epsilon=0". However, this does not seem to be the case since the definition of "exact replication" does not refer to the ouputs of the model (whereas the "approximate replication" does.)...

Is this correct?

### Q3
It may be the case that the two definition actually refer to two classical way to define a semantics in computer science: 
- **denotationally**, by expressing the relationship between inputs (memory before) and outputs (memory after), as it is more or less the case for the approximate replication (denotation)
- **operationally**, by descring the sequnce of operations to be carried out. 

Should this interpretation be the actual one, we would have to distribguish "exact" and "approximate" denotational and operational semantics. Two implementations would be approximately identical in the operational sense if the sequence of operations carried out would be "approximately" the same. 

Is this interpretation correct?