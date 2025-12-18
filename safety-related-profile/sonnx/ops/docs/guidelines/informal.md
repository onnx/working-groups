# Introduction

This document gives the guidelines to be followed when writing an operator's **informal** specification.

# Informal specification guidelines
This section is composed of two sub-sections:
- *General guidelines*, which defines the use of fonts, notations (e.g., for tensor) and tags (e.g., for constraints), and, finally, specifies how to deal with the numerical types involved in the operator at stake.
- *Structure of the informal specification*, which defines the structure and contents of the informal specification of an operator. This section applies the general guidelines.

## General guidelines  
The informal specification is intended for both users *and* implementers of operators who both need to understand what an operator does and how to use it. For instance, the first kind of readers might be satisfied with one or two sentences about the semantics of an operator whereas the second category of readers would like to get all the details of the semantics.

More precisely, the informal specification:
- Is aimed at showing clearly what a given operator is supposed to do,
- Without calling on a strict formal, mathematical language,
- Knowing that the exact and complete specification is given in the "formal" specification.
- May provide diagrams and examples to make things clear.
- Follows ONNX nomenclature, which includes naming convention, for operator names, types, identifiers of operator inputs, outputs and attribute, etc.
  - Examples: 
    - The element-wise addition of tensors is $Add$, not $add$
    - The 16-bit floating-point type is $float16$, not $FP16$

The writer of the informal specification must take care to keep it readable and understandable by a ML developer. The recommendations given in the following guidelines target this objective.

### Styling
- Mathematical objects are represented using *italic*. LaTeX formulae are used.

### Naming conventions
- As far as possible, ONNX names for inputs, outputs, and attributes must be used.

### Notations
#### Tensors
- A tensor is always represented in uppercase letters (e.g., $A, B,...,X, Y, Z$).
- In the case of a variadic operator (e.g., **Concat**), the tensor parameters are designated by an index: $A0$, $A1$, etc. Indexes start at 0 to be consistent with the other use of indexes. 
- The rank of a tensor $T$, i.e., the number of its dimensions, is denoted $rT$. 
- The shape of a tensor $A$ is denoted by a vector $(dA_0, ..., dA_i, ..., dA_n)$ where $dA_i$ refers to the dimension along axis $i$ and $n=rA-1$.
- For a tensor used as a variadic parameter (denoted $Ai$), the shape is denoted by $(dAi_{0}, dAi_{1}, ...)$.
- A specific element of a tensor is denoted:
  - either as: $A[i]$, where $i$ is a [tensor index](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/sonnx/ops/spec/informal/common/definitions.md#tensor_index)
  - or as: $A[i_0, i_1, ..., i_{rA-1}]$. 
 
#### Tags
The informal specification makes use of three different types of tags:
- A **restrictions tag** expresses a restriction with respect to the ONNX standard (see the section about restriction below). They are indicated by tag `[R<i>]` where `<i>` is a number.\
A synthesis of all restrictions is given in section "Restrictions" (see below).
- A **constraints tag** expresses a constraint on one or several inputs, outputs, or attributes. They are indicated using `[C<i>]` where `<i>` is a number.
- A **traceability tag** identifies a specific location in the informal specification. These tags are used to establish traceability between the informal and formal specifications. They are indicated by `[T<i>]` where `<i>` is a number.
 
For instance, here is a tag introducing a constraint relating some input and output tensors:
>`[C1]` Shape consistency \
> Statement: Tensor $A$ and $Y$ shall have the same shape.
  
When part of the documentation refers to a tag, an hyperlink is used. This is achieved using the following elements: 
```
  `[T1]`<a name="my_tag_name"></a>
```
   to declare the location of the tagged element and 
  ```
  [`[T1]`](#my_tag_name).
```
to refer to the tagged element. 

Here is an example: <br>
`[T1]` <a name="my_tag_name"></a> This is a tagged paragraph.

This is a reference to the tagged paragraph  [`[T1]`](#my_tag_name).


### Types
- The type names shall be the ones used in the ONNX description of the operators, without surrounding them with "tensor()".
  - Example: "tensor(double)" in ONNX becomes "double" in the informal specification.
- The data types allowed in SONNX operators are: 
  - IEEE 754 floating-point types: double, float, float16
  - Signed integer types: int64, int32, int16, int8
  - Unsigned integer types: uint64, uint32, uint16, uint8
  - bool
  - string
- IEEE 754 floating-point types, i.e., double, float and float16 have the following special numbers:
  - +0 and -0
  - +Inf and -Inf
  - NaN (Not a Number)
- All operators applicable to numeric values shall be specified for values in the domain of real numbers. 
- Specific description shall be given for the other types (float, double, etc.).
- A description can be applicable to multiple types as long as its **semantics description** remains the same for all types.  

## Structure of the informal specification

This Section describes the required structure $and$ contents of the informal specification of an operator.

The [informal specification template](informal_spec_template.md) gives the required structure.

### Contents

This section gives the list of all informal specifications of the operator, for each of the applicable types, with hyperlinks to the sections (see [template](informal_spec_template.md)). 

- **Op** operator for type real
- **Op** operator for types &lt;T1&gt;, &lt;T2&gt;,...
- **Op** operator for types &lt;T1&gt;, &lt;T2&gt;,...
- etc.

The reference, with link, to the ONNX definition of **Op** shall be inserted in this section. See **Div** example below. 

Here is an example for operator **Div**:
> Contents
>- **Div** operator for type real
>- **Div** operator for types float16, float32, float64
>- **Div** operator for types int8, int16, int32, int64, uint8, uint16, uint32, uint64
>
> Based on ONNX [Div version 14](https://onnx.ai/onnx/operators/onnx__Div.html).

The following section must be repeated for each set of types for which the semantics is the same. One section corresponds to one entry in the "Contents" list. 

## **Op**  (<type 1>, <type 2>,...)

### Signature

Definition of operator **Op** signature:

 $O = \textbf{Op}(X,Y,...,Z)$

 where
 - $X$: Brief description of argument $X$
 - $Y$: Brief description of argument $Y$
 - ...
 - $O$: Brief description of output 
 
Arguments shall have different names. For instance 

$O = \textbf{Op}(X, Y)$

When the same name is used for different arguments such as in 

 $O = \textbf{Op}(X0,X1,...,XL)$

 this means that the operator is **variadic**, i.e., it accepts a variable number of arguments. In this example, there are n arguments that are discriminated by their index.  

### Restrictions
This section lists all restrictions applicable to the operator. A restriction is a limit with respect to the normal usage domain of the ONNX operator. A restriction may concern the dimension of tensors, values of attributes, etc. 

There are SONNX general restrictions that apply to all the operators. Therefore, this section shall contain the following markdown link:

`\[General restrictions](../common/general_restrictions.md)`

Restrictions marked as "Transient" are introduced by the working group in order to reduce the specification effort. Such restrictions, which are not traceable to a need, are aimed at being eventually relaxed. However, in the meantime, both transient and non-transient restrictions are applicable by the operator user or implementer. 

Restrictions not marked as "transient" are traceable to some requirement. The requirement is identified using an hyperlink.
 
An example is given hereafter

| Restriction    | Statement | Origin |
| -------- | ------- | ------- |
| `[R1]` | Input tensor $X$ has 2 spatial axes | Transient |
| `[R2]` | Attribute `auto_pad` is restricted to NOTSET  | [No default values](../../../deliverables/reqs/reqs.md#no_default_value) |

 ### Informal specification
 
 This section contains the informal specification of the operator. By "informal", we mean that the description does not rely on a formal language, even though it usually uses some mathematical formulae. The specification shall be readable, understandable, and self-contained. It can include figures if deemed necessary. The objective is that a human being can fully understand the domain, range, and semantic of the operator with no additional information. Stated differently, he/she should be able to implement the operator with no additional information.
 
The informal specification shall be composed of the following parts:
- A short description of the operator. For instance, for the $conv$ operator: 

> Operator **Conv}** computes the convolution of the input tensor $A$ with the kernel $W$ and adds bias $B$ to the result. Two types of convolutions are supported: standard convolution and depthwise convolution.

- A detailed description that:
  - Uses the notations proposed in section "Notations" of these guidelines
  - Implements the traceability tags proposed in Section "Tags" of these guidelines
  - Presents the mathematical formulae, if necessary, according to the following pattern: the complete formula is first given and its atomic elements and sub-expressions are defined afterward, by introducing them with "Where" or "In which".
  - Insert a blank line before and after each formula so that it renders correctly in the browser.
        
For instance, for the **Conv** operator:

> $$
    Y[b, c, m, n] = \sum_{i=0}^{dW_1-1} \sum_{j=0}^{dW_2-1} \sum_{z=0}^{dW_3-1} \\ (X_p[b,i,m \cdot \text{strides}[0]+ j , n \cdot \text{strides}[1]+ z ] \cdot W_d[c, i, j, z]) \\ + B_b[c]
$$
> Where
>- $b \in [0,dY_0-1]$ is the batch index. $dY_0$ is the batch size of output $Y$
>- $c \in [0,dY_1-1]$ is the data channel. $dY_1$ is the number of data channels of output $Y$
>- $m \in [0,dY_2-1]$ is the index of the first spatial axis of output $Y$
>- $n \in [0,dY_3-1]$ is the index of the second spatial axis of output $Y$
>- etc.

## Error conditions

This section identifies the errors that may occur during the execution of the operator (or *runtime errors*).

When writing a specification, the writer must identify the following failure conditions:
- for floating point computations 
  - invalid operation as defined in IEEE 754 section 7.2, i.e.
    - $0 \times\infty$ or $\infty \times 0$
    - addition or subtraction or fusedMultiplyAdd: magnitude subtraction of infinities, such as addition $(+\infty, -\infty)$ 
    - division $(0, 0)$ or division ($\infty, \infty)$
    - remainder(x, y), when y is zero or x is infinite and neither is a NaN
    - square root if the operand is less than zero
    - etc. Refer to the standard for a complete list of error conditions.
  - overflows (computations leading to +Inf or -Inf)
- for integer computations 
  - division by zero,
  - overflows, i.e., operations leading to a value out of the range (e.g., addition of two large int32 values non representable in int32)

The following rules must be applied.
  - Restrict the input domain to prevent the occurrence failures if it is not too conservative. for instance, $x \ge 0$ for $sqrt(x)$ is deemed acceptable whereas, using uint32, $A\leq2^{31}$ and $B\leq2^{31}$ for $A+B$ is deemed too conservative.
  - Give the most detailed description of the conditions in which a failure can occur, and the possible expected result. For instance for a matrix multiplication in int32, explain that the accumulator may overflow and may wrap around, leading to an incorrect and inconsistent result. If possible, point out the location in the specification where the error may occur. 
- If no indication is given about occurrence of a "failure", this means that the operator returns a correct value (as per specification) for **any** input value in the domain defined by the type.  
- If applicable and possible, provide "recommendations" about the implementation to prevent failure. For instance, propose to substract $max(Xi)$ to the argument to make the **Softmax** operator more robust.

Note that these rules concern the *specification* of the operation. Therefore,  they must be independent from implementation choices. For instance, *generally speaking* it* is always possible for the operation to overflow if the domain is output domain limited (e.g., int32), so there must be a warning about this failure condition. Nevertheless, a specific implementation may be failure-free if, for example, the size for the matrices is limited and the accumulator is sufficiently large. In that case, the implementation must give these conditions. Otherwise, the implementation is deemed compliant with the specification. 

## Attributes
This section describes the operator's attributes. 

### $\text{name}$: \<type\>
where $\text{name}$ is the attribute's name and \<type\> is the attribute's type.

 #### Constraints
This section gives all constraints applicable to the attribute.

- When a constraint involves several inputs/outputs/attributes, it is only described once when the first input or attribute concerned by the constraint is described. Then, for the other inputs, attributes, or outputs concerned by the same constraint, a cross-reference is given. 
The description is structured as follows:*

 - `[C<i>]` &lt;Title of constraint&gt;
   - Statement: &lt;Expression of the constraint&gt; or cross-reference to the previous location where this constraint was first introduced.
   - Rationale: &lt;Justification for the constraint&gt;. When the title and/or the statement of the constraint are sufficiently explicit, the rationale may be omitted. 

## Inputs

This section describes the operator's inputs.
 
### $\text{name}$: \<type\>

where $\text{name}$ is the name of the input and \<type\> is the type of the input.

#### Constraints
Same as for the attributes.

### Outputs
 This section describes the operator output.

### $\text{name}$: \<type\>
where $\text{name}$ is the output's name and \<type\> is the output's type.

 #### Constraints
Same as for the inputs.

                          End of the document.
