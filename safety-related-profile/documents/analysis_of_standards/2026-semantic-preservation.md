
### The initial question 
**Do we need bit-to-bit equivalence between the trained model and the implemented model? If not, what is an acceptable tolerance? How to determine it?**

The following sections are given in the temporal order. 

### What do we what to preserve and why (eric)

#### Definitions

In a ML process, we have two different artifacts: a trained model and an implemented model. The trained model is executed in a "host environment" while the implemented model is executed on the target environment, the two environment being usually different. 

The trained model is developed in the first part of the W from the requirements, ODD, data, via a training process.

The implemented model is obtained by a series of transformations of the trained model, possibly going through a serialization into a SONNX model.

Note that in what follows, when I use "implemented model", I mean the implemented model running on the target platform. I don't simply mean, for instance, "the source code of the implemented model".

#### The problem

The problem is to demonstrate that if I verify some property P on the trained model (TM), - is it preserved (or "it is still valid") on the implemented model (IM)?
- with what level of confidence? 

Stated differently, if P holds on the trained model, does it holds on the implemented model?

This shows that the problem is related to the property at stake. (Some properties may be preserved and others not.) 

Demonstrating "bit-to-bit" equivalence seams to guarantee that any functional property (*) verified on TM will be preserved on IM since the only output of the execution of a model is a vector of numerical values represented by bit vectors.

(*) This doesn't hold for temporal properties. 

Stated differently, if bit-to-bit equivalence can be demonstrated, then problem is solved.

The difficulty lies in the fact that "bit-to-bit" equivalence can usually not be demonstrated. 

The next questions are then

- Q1: Are there any properties $P_i$ that can only be verified on the training model? Indeed, in that case, there is no other solution than to check those properties on the TM and to demonstrate that the property is preserved by the IM. Reciprocally, if I have no such property, then it means that all verification activities can be done -- in principle, see below -- on the IM. 
- Q2: Are there any property $P'_i$ for which it is much more economical (measured in €) to verify on the TM than on the IM, even when integrating the cost of demonstrating property preservation. Note that the economy may be due to the technical environment that facilitate verification activities, but it may simply be due the fact that the verification is done earlier in the process, so that error are found earlier too...
  
Concerning Q1, the set ${P_1, P_2,...,P_i}$ contains at least properties that concern the training process itself such as:
- Training stability, 
- Generalization capability, 
- etc.

Those properties can only be verified during training, but they also do not concern the implemented model. So "preserving them" makes no sense. 

[Note that the question can be stated as follows: "Are there any property that can only be verified on the training model and that must be preserved? " I would say that the answer is logically : no, since "if a property can only be verified on the training model" then, by definition,  "it cannot be verified on the implemented model", so preservation makes no sense. Or, stated differently, those properties concern the learning process as a while, not the sole model...]  

Concerning Q2, there are many good reasons to perform verification activities on the trained model (on the host platform), including
- host execution may be massively parallelized;
- batch execution is easier;
- observability is greater;
- gradients and internal activations are available;
- debugging is easier;
- the verification of some properties may be very computationally expensive (adversarial searches, ODD exploration, etc.)

In addition, some verification methods using specific tools (e.g., some formal verification methods) may be only applicable in the host context, on the trained model.

So, I end up with:  
- our problem depends on the properties at stake, so we have to identify precisely the properties we are interested in,
- our problem is essentially an industrial problem, not a development assurance problem, which means that there is no **fundamental** reason to ensure that all properties are preserved ; again, the problem must be addressed on a per property basis, considering the verification effort / cost. 

#### Let's go back to the function (Nicolas)

It might be interesting to start from the aircraft function.
The specific nature of A/C functions allocated to ML engineering, is that human reasoning is not able to elicit unambiguous verifiable requirements from the function.

The intent of ED324 is to provide guidelines to perform requirement engineering with data and an optimization process.

The outcome of the 1st V of the W shape life-cycle is to obtain a non ambiguous, validated,  verifiable  requirement: the trained model.

> [eric] Fully agree...

The trained model is what the system shall do to perform the intended function.

To validate that this model==requirement is the right one, we use metrics with thresholds to assess the properties of this model==requirement, i.e. the performance, stability, robustness, generalisation, explainability...

> [eric] Fully agree...

This model==requirement is non ambiguous if there is a single possible interpretation (ED324 definition).

This is where the MLMD comes into play. 

If the MLMD does not contain the full semantics, there might be several interpretations, even non deterministic ones (i.e. atomic_add). 

The ONNX level of semantics is not sufficient to cover the full semantics.

> [eric] I guess that you are considering elements related to the functional semantic, not the pure mathematical semantic...
 
NB: the ONNX format contains doc_string properties which could be used to complement the semantics.

The model runtime used for validation is part of the model semantics, and consequently part of the requirement.

> [eric] I agree. That is what I actually called "training model", actually (the model and its execution platform). 

Unless the low level details can be encompassed in an epsilon, which can be the trick to solve the ambiguity. Whatever implementation bounded by this epsilon satisfies the model==requirement.

The MLMD being a non-ambiguous description of the model==requirement, the 2nd-V of the W is its implementation as a SW/HW item, guided by DO178/254.

The DO178/254 verification of this model==requirement is to ensure that on the target it produces the expected output defined by the  model==requirement. 

As the trained model is the validated requirement, the target implementation should produce the same output as the trained model. 

> [eric] That's the point.  

The purpose in the DO178 verification is not to re-validate the properties of a requirement which have already been validated.

> [eric] No, it is not, but if I have a strong way to validate the "requirement model" (i.e., it does what it is expected to do), then it make sense to use the same method to validate the implementation method  without having to introduce the intermediate MLMD step. To make it clear, note that I am not considering the ED324 has the Bible which says "There shallt be a MLMD and the MLMD shallt be the Truth". My point is basically: there is a model called a "training model" that is considered to be OK, so there is a method (criteria) that allows someone to claim that it is OK, so let's use the same method to verify the implemented model...

After integration at system level, the system verification is able to confirm with some functional tests that the intended function is implemented as expected.

There is not any objective in the ED324 2nd-V of the W. Its sole purpose is to reference DO178/254.
This 2nd-V could be removed.

ED324 mainly defines the process to elicit and validate this model==requirement 
When it's done, the algebraic  model==requirement , i.e.   f(x)=...  (captured by MLMD) can be implemented and verified with bit2bit or differential testing ( epsilon )  or formal method.

>[eric] Definitely. But my point is not to discuss the ED, but to understand WHY, TECHNICALLY we are doing the things that way and, for the moment, it is still not clear to me...

I do not consider a metric as a requirement. The metric is a means to validate a property (performance,...) of the functional requirement, way before implementation and verification. It is a way to validate that the model is the right function, not to verify that the model is implemented right.

>[eric] Yes, sure. But if if I can demonstrate that the implemented model does the right function, isn't it sufficient? 


#### (Jean-Loup)

I am not sure about the scope of this discussion because if we are trying to address the objective SU-IMP-06 of the version 3 of EASA's concept paper, i.e. "The performance of the implemented model when integrated on the target platform should be evaluated based on the test data set, and the result of the model verification should be documented.", a property not related to the test data set is not relevant and a sample per sample run of the implemented model should allow to compute any property related to the test data set. Did I miss something?

>[eric] Yes. The test dataset may be designed to cover the ML performance, the robustness, etc. and be executed on the implementation model. In that case, I am wondering why we need this 
>[eric] In fact, I feel that the MLMD is just there to give the spec that the developers need to develop the implementation model. It is a development artefact, not an element of development assurance.

##### From High Level Requirements to Low Level Requirements

Hypothesis: The neural network solves a binary classification problem and the main high level requirement is stated in terms of accuracy.
Note: Accuracy, i.e. the number of correct predictions divided by the total number of predictions, is defined w.r.t. a database, usualy the test database.

Hypothesis: The low level requirements are related to numerical precision, i.e. the maximum difference between a value computed in real numbers and a value computed in floating point numbers, at the level of operators beloning to the neural network. Note: Because the the network solves a binary classification problem, its last layer is a comparision, i.e. if the logit associated to class 1 is larger than the logit associated to class 2 the result is class 1 otherwise it is class 2.

Definition: Perfect replication. For a database a perfect replication is obtained when for each sample the results of the predictions are equal, i.e. the same class is predicted by both classifiers.

Perfect replication implies accuracy preservation.

Network numerical precision implying perfect replication. When the numerical precision of the neural network is such that for any sample of the database the result of the test on logits doesn't change then there is perfect replication. This can be translated in terms of maximal error by stating that the maximal error multiplied by two shall be less than the minimum, among the samples $i$ with input $x_i$ of the database $D$, of the absolute value of the difference between the logit associated to class 1 $l_1(x_i)$ and the logit associated to class 2 $l_2(x_i)$. 

Hypothesis: The neural network is a serie of $L$ operators, each operator $j$ multiplies the maximum error of its input by a factor $A_j$ and add its own maximal error $B_j$.

Hypothesis there is no error on the input.

The maximum error on the output is given by $B_1A_2 \dots A_L + B_2A_3 \dots A_L + \dots + B_{L-1}A_L + B_L$. Thus we should have:

$B_1A_2 \dots A_L + B_2A_3 \dots A_L + \dots + B_{L-1}A_L + B_L < \frac{1}{2} \min_{i \in D} |l_1(x_i) - l_2(x_i)|$

There is a simple low level requirement satisfying the high level requirement. For any operator, $j$:
- the input error multiplicative factor $A_j$ is less than one and
- its own maximal error $B_j$ is less than $\frac{1}{2L} \min_{i \in D} |l_1(x_i) - l_2(x_i)|$.

Note that this could also lead to add requirements to the first V of the W:
- in order to have a small $L$, the network should not be so deep and
- the differences between logits shall be large for any sample, this may be linked to some definition of robustness.
