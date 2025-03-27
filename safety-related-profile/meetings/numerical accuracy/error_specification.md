# TOPICS : Specification of behavior in the presence of error (action: 1812-2)

By "error", we mean an undefined behaviour, not a deviation with respect to some expected result due to the differences between real and floating point operations. A "division by zero" that would occur during the computation of some operator is an example of such error. 

Conditions on inputs leading to such errors must be described in the specification. They restrain the domain of the operator's *domain of definition*.

The *domain of definition* shall be expressed by a set of constraints on the operator's inputs and attributes.

We have to consider two types of constraints: *explicit constraints* and *implicit constraints*. Explicit constraints are expressed while implicit constraints aren't expressed.

## A. - Expressed constraints

Déf. : a constraint that is expressed in the specification as a relation involving inputs and attributes. 

Those constraints are pre-conditions for the operator. For this reason they don't involve outputs.

Note that outputs aren't considered to be potentially part of the precondition. The cases where we want the shape of the output to be explicitly given by the user (and not "inferred") shall be managed using attributes. 
**To be discussed...**

### A.1 - Statically verifiable constraints

Those constraints may depend on values, but those values are known before runtime (e.g., biases, weights, etc.). They are stored in the ONNX file or in some external  file.  

### A.2 - Non-statically verifiable constraints

Those constraints cannot be checked before execution because they depend on the values of non-constant inputs. This is the case for simple operators such as "log" (input values must be strictly positive)  or for more complicated operators such as "unsqueeze" (input "axes"  must not contain duplicate values).

## B. - Non expressed constraints

Déf. : A constraint that is not expressed in the specification, because defining the points where the function is not defined in terms of its inputs can't be done or would be extremely difficult to do (imagine an hypothetical operator that would do x/f(y) with f a function for which f(y)=0 can hardly be solved...).


# Preventing the occurrence of errors

- Case A.1 : Error conditions can be checked on the ONNX file.
- Case A.2 : Error conditions cannot be checked on the ONNX file, but they can be checked at runtime by considering inputs and attributes
- Case B : Error conditions cannot be checked neither the ONNX file nor on the (inputs,outputs,attributes). Those errors can be checked by instrumenting the code (in the previous example, by checking that f(y) is not zero before doing the division), by hardware error handling mechanims (traps) or by using singular values (NaN, inf, etc.).


## Recommendations  

### Case A.1 (Statically verifiable constraints)

- A model that violates constraints in class A.1 for at least one of its operators is an **invalid model**. 
- An **invalid model** can be detected by a "model checker"
- Those constraints must be clearly identified because they will constitute the specification for the model checker.

### Case A.2 (Non statically verifiable constraints)
The error condition is specified.
The behaviour in case of error is specified.

#### At operator level
For instance, considering the `div` operator:
- Error condition: "denominator equals 0"
- Behaviour
  - For real values, operation is "undefined".
  - For FP64, FP32, FP16, BFLOAT16, behaviour is "returns 'NaN'".
  - For INT8,  behaviour is "undefined". 

Note the difference between "operation is undefined" and "behaviour is undefined". 

#### At graph level
The only thing to be specified is how "inf" and "nan" propagate. 

### Case B (Non expressed constraints)

The specification shall indicate that an error may occur during computation even though we may not be able to describe precisely the conditions at the (inputs and attributes) level. 

The low-level error condition (e.g., "division by zero") must be described.

- Option 1: 
  - The low-level error condition is specified and the behaviour in case of error is precisely defined. This covers the case where `inf` and `nan` may be generated and propagated.  
- Option 2:  
  - The error condition is specified but the behaviour in case of error is not specified. The specification only states that the behaviour is undefined. 

We consider the **two options** because checking the occurrence of the low-level error condition may be more or less difficult to detect. For instance, to detect that no overflow occur when adding integer numbers would require specific code on most architectures... 

# Miscellaneous Remarks

## Remark #1: Restricting SONNX to Explicit Constraints

The impact of restricting the scope of SONNX to operators whose domain of definition corresponds to explicit constraints on inputs and attributes on its expressiveness should be assessed.

## Remark #2: Domains and Ranges for Operators
For an operator, one can associate not only a domain for its inputs but also a range for its outputs. For example, the sigmoid function has a range:
$\text{range} = [0, 1]$

By defining both domains and ranges, it becomes possible to impose  generic constraints on the model:

- The ODD of the model should be shuch that inputs of the model must necessarily fall within the domain of the operators in the corresponding first layer.
- The range of an operator upstream of another operator must be included in the domain of the latter.

These constraints lead to graph-level requirements aimed at ensuring error-free inference in the model.

## Remark #3: Handling of NaNs and INFs

Three cases must be considered : 
- real values
- floating point values 
	- IEEE floating point values (FP16, FP32, FP64)
	- Non IEEE floating point values (e.g., BFLOAT16, FP8, etc.)
- integers values


### Real values

For real values, we will simply indicate that the operation is not defined when the values are out of range. This will be expresses as constraint on the input parameters, attributes.

### Floating point values

#### IEEE floating point values (FP16, FP32, FP64)
For IEEE floating point value, we will simply indicate that the IEEE 754 rules applies, e.g., x/y returns "NaN" when y = 0. Note that this makes sense since Python follows IEEE.
This means that, e.g., a division by zero will lead to a NaN that will propagate in the rest of the computation. 
This value can be checked at the output level. 

Note that NaN can be detected in the hidden layers using the [IsNaN](https://onnx.ai/onnx/operators/onnx__IsNaN.html) ONNX operator. And, of course, they can be detected at the output.

So, in the standard, we may simply recall that the IEEE 754 applies and specify what the operator is expected to generate in case when a parameter is out of range. 

#### Non IEEE floating point values (e.g., BFLOAT16, FP8, etc.)

For BFloat16, the IEEE754 rules should apply for INF and NaNs. So we fall back to case 

As of today, ONNX does not support FP8...


#### Integer values

For integers values, two cases :
- division by zero conditions, which lead to a trap and a "core dump" (in the best case)
- overflow conditions, which are not detected

(I propose to postpone the case of integer values for a while.) 
