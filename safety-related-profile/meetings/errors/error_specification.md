# TOPICS : Specification of behavior in the presence of error (action: 1812-2)

By "error", we mean an undefined behaviour, not a deviation with respect to some expected result due to the differences between real and floating point operations. A "division by zero" that would occur during the computation of some operator is an example of such error. 

Conditions on inputs leading to such errors must be described in the specification. They ar part of the domain of the operator's *domain of definition*.

The *domain of definition* shall be expressed by a set of constraints on the operator's inputs and attributes.

We have to consider two types of constraints: *explicit constraints* and *implicit constraints*.

## A. - Expressed constraints

Déf. : a constraint that is expressed in the specification as a relation involving  inputs, outputs, and attributes. 

Those constraints are pre-conditions for the operator. Note that outputs are considered to be potentially part of the precondition to cover the cases where we want the shape of the output to be explicitly given by the user (and not "inferred"). 
** This is to be discussed...**

### A.1 - Statically verifiable constraints
Those constraints may depend on tensor's values, but those tensors are constants given in the ONNX file (e.g., biases, weights, etc.)

### A.2 - Non-statically verifiable constraints
Those constraints cannot be checked on the ONNX file because they depend on the values of non-constant tensors. This is the case for simple operators such as "log" (values must be strictly positive)  or for more complicated operators such as "unsqueeze" (input "axes"  must not contain duplicate values).

## B. - Non expressed constraints

Déf. : A constraint that is not expressed in the specification, because defining the points where the function is not defined in terms of its inputs can't be done or would be extremely difficult to do (imagine an hypothetical operator that would do x/f(y) with f a function for which f(y)=0 can hardly be solved...).


# Preventing the occurrence of errors

- Case A.1 : Error conditions can be checked on the ONNX file.
- Case A.2 : Error conditions cannot be checked on the ONNX file, but they can be checked at runtime by considering inputs, outputs and attributes
- Case B : Error conditions cannot be checked neither the ONNX file nor on the (inputs,outputs,attributes). hose errors can be checked by instrumenting the code (in the previous example, by checking that f(y) is not zero before doing the division), by hardware error handling mechanims (traps) or by using singular values (NaN, inf, etc.).


## Recommandations 

### All cases

- The specification of operators shall state that the behaviour of the operator is undefined should any constraints (in A or B) be violated. 

### Case A.1 

- A model that violates constraints in class A.1 is an **invalid model**. 
- An **invalid model** can be detected by a "model checker"
- Those constraints must be clearly identified because they will constitute the specification of the model checker.

### Case A.2 
- Option 1: 
  - The error condition is specified and the behaviour (incl. output) in case of error is precisely defined.
- Option 2:  
  - The error condition is specified but the behaviour (incl. output) in case of error is not specified. The specification only states that the behaviour is undefined. 

Note that this may be part of the specification of the graph execution, not only the operator. 

### Case B

The specification shall indicate that an error may occur during computations even though we may not be able to describe precisely the conditions at the (inputs, outputs, attributes) level. 

The low-level error condition (e.g., "division by zero") must be described.

- Option 1: 
  - The low-level error condition is specified and the behaviour (incl. output) in case of error is precisely defined.
- Option 2:  
  - The error condition is specified but the behaviour (incl. output) in case of error is not specified. The specification only states that the behaviour is undefined. 

We consider the **two options** because checking the occurrence of the low-level error condition may be more or less difficult to detect. For instance, to detect that no overflow occur when adding integer numbers would require specific code on most architectures... 


# Remarks

## Jean-Loup (Dec. 19th) 
(Translated from French by ChatGPT and reformated by me.)

### Remark #1: explicit constraints

In the statement:
> Explicit constraints: a constraint that is expressed in the specification as a relation between inputs, outputs, and attributes."

I would not include outputs because, for an operator $f$, the output is defined as $\text{output} = f(\text{input})$.
In fact, a so-called explicit constraint like $\text{input} + \text{output} > 0$ is, if $f$ is complex, actually an implicit constraint on the input:
$\text{input} + f(\text{input}) > 0$

### Remark #2: Restricting SONNX to Explicit Constraints

In my opinion, it would be wise to restrict the scope of SONNX to operators whose domain of definition corresponds to explicit constraints on inputs and attributes.

Of course, it would be necessary to verify that this restriction does not overly impact the expressiveness of SONNX.

### Remark #3: Domains and Ranges for Operators
For an operator, one can associate not only a domain for its inputs but also a range for its outputs. For example, the sigmoid function has a range:
$\text{range} = [0, 1]$

By defining both domains and ranges, it becomes possible to impose constraints on the model:

The inputs of the model must necessarily fall within the domain of the operators in the corresponding first layer.
The range of an operator upstream of another operator must be included in the domain of the latter.

These constraints lead to graph-level requirements aimed at ensuring error-free inference in the model.