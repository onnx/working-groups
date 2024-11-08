This document contains comments and elements of discussions about the concept of "replication" introduced in the ARP6983.

This discussion is necessary since the replication objectives (i.e., the replication criteria that are satisfied) are directly linked with the contents of the MLMD and, eventually, with the language used to express the MLMD (in our case: SONNX).

*Please add your own comments / remarks. Use ``[my name]`` (e.g., ``[eric]``*) to indentify your comment. 

# Exact replication
## Statement (from ARP683) 
> [...] the ML Model description should contain sufficient details on the ML Model semantic to fully preserve this semantic in the implemented ML Model. For example, an exact replication criterion may be the direct and faithful implementation of the ML Model description so that the implemented ML Model meets the same performance, generalization, stability, and robustness requirements.

## Comments and discussions 

- "[...] sufficient **details** on the ML model semantic [...]"
- What does "details" mean here? 
- As written, it seems as if "contain[ing] sufficient details" will ensure *de facto* that the semantic will be preserved. In reality, the MLMD shall provide sufficient "details" to allow the implementer to preserve the semantic of the "ML model". 
- The definition makes reference to a "ML Model" whose semantic must be captured and expressed (and "preserved" by the MLMD. 
  - This means that we have another model with its own semantic. 
  - Where is this semantic defined? This model is different from the MLMD . So it must be described using another language than the MLMD. And this language should be defined too.
  - We may also consider that the MLMD **is** the model. 
- The first part of the definition expresses a first objective: "to preserve the semantic of the **ML model**". But the second part of the definition makes no more reference to the "ML model":  it only constrains the relation between the MLMD and the implementation of the MLMD. 
  - In fact, it may be wise to remove the reference to the "ML model" in this definition in order to focus exclusively on the relation between the MLMD and the implementation of the MLMD. Or, at least, to clearly distinguish the relation between the ML model and the MLMD, and the relaton between the MLMD and the implemented MLMD model (or introduce one relation between the "ML Model" and the "implemented ML Model" and to refine it into the previous two relations).  
- The definition states that "an exact replication criterion **may be** the direct and faithfull implementation of the ML Model description". 
  - The use of "For example" and "may be" seems to indicate that there could be other criteria. 
    - Does this mean that the definition of the criterion is up to the model designer?
    - And if it is the case, called it a "exact replication criterion"  
  - On the contrary, the second part of the sentence seems to express the actual replication criteria since having a "direct and faithful" implementation is only one possible means to satisfy performance, robustness, etc. criteria. In that sense, "exact replication" would actually mean that the performance, generalization, stability and/or robustness" of the implementation are the same of the MLMD model. 
    - The definition identifies 4 quantities (performance, generalization, ...)". Is this list exhaustive? and what do we mean exactly by "performance" (there are quite a few performance metrics in ML) or "robustness" (local? global?). 
      - As previously, the exact criteria would have to be explicitly defined by the designer. 


  - In "an exact replication criterion may be the **direct** and faithful implementation of the ML Model", what it the exact meaning of "direct"? 
    - "direct" could refer to some traceability property such as "all elements of the MLMD are traceable to the implementation of the MLMD and reciprocally". In practice, this could mean that we expect each element of the MLMD ("graph", "node",...) to be found in the implementation and that each operation is done (e.g.,) in the same order as in the MLMD (which, then, has to specify this order). 
    - In that sense, an implementation "exactly replicate" the MLMD if it replicates its "structure".  
    
# Approximate definition 

## Statement (from ARP683) 
> [...] the ML Model description should contain sufficient details on the ML Model semantics to approximate this semantic in the implemented ML Model with a specified tolerance. For example, an approximation metric may be expressed for a given dataset by the maximal gap between the trained ML Model outputs and the
implemented ML Model outputs. The corresponding approximation replication requirement may be that this maximal gap should not exceed a given value epsilon.

## Comments and discussions
- The notion of "gap" is not precise. We may use the term "distance" and, in this case, the metric that is used must be defined. 
  - This metric will depend on the model. Nota that it may be easier to define for a regression function than for a classifier.  
  - If the metric is "user dependant", it means that it should be specified in the MLMD. 
- Normally, we would expect "exact replication" to be a specific case of "approximate replication", i.e., an "exact replication" is a replication  for which $\epsilon=0".
  - However, this is not the case for the moment since the definition of "exact replication" does not refer to the ouputs of the model...
  - Basicaly, we would expect a unique criterion, let's call it "replication criterion" that will refer to $\epsilon". Then, the definition of "exact replication" would not be necessary any more. 
- If replication is defined using an $\epsilon$, how will a designer estimate this value?

