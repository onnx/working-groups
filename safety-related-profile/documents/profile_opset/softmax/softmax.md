# Contents

- **softmax** operator for type [real](#real)
- **softmax** operator for types [FP16, FP32, FP64](#float)

Based on ONNX documentation version 14.

<a id="real"></a>
# **softmax** (real)

## Signature
$output = \text{softmax}(input)$

where:
- $input$: input tensor
- $output$: output tensor
 
## Restrictions

The following restrictions apply to the **softmax** operator for the SONNX profile:

| Restriction | Statement                                                   | Origin                                                                                      |
|-------------|-------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| `[R1]`     | Sparse tensors are not supported                            | General restriction [GR1](../general_restrictions.md#GR1)
| `[R2]` <a id="R1"></a>     | Shape of tensors shall be explicit          | General restriction [GR2](../general_restrictions.md#GR2) |
| `[R3]` <a id="R1"></a>     | Attribute $axis$ must be defined          | to be complete |
| `[R4]` <a id="R1"></a>     | Attribute $axis$ must be positive or null    | to be complete |

## Informal specification

Operator **softmax** computes the following mathematical expression 

For any index $i$,

$$
output[i] = e^{input[i]-max(input)}/ \sum_{j_{axis}=0}^{dinput_{axis}-1} e^{input[i]-max(input)}[...,j_{axis},...] $$

Inthis formula, the exponentiation operation ($e^x$) refers to ONNX operator **exp**.

### Example 1

```math
input = \begin{bmatrix} 9.5 & 35.7 \end{bmatrix}
```


```math
output = \text{softmax}(input) = \begin{bmatrix} e^{-26.2} / (e^{-26.2}+1) & 1 / (e^{-26.2}+1)\end{bmatrix}
```


## Error conditions
No error condition: the denominator is always greater or equal to 1, so there cannot be a division by zero. This prevent the case of 0/0 that would lead to a Nan.

> À déplacer vers traitement des float et rajouter "The effect of the **softmax** operator is illustrated on the following example."

## Inputs

### $input$: real
Input of the **softmax** operator. 

#### Constraints

 - `[C1]` <a id="C1ra"></a> Shape consistency
   - Statement: Tensors $input$ and $output$ must have the same shape. 
 - `[C2]` <a id="C2ra"></a> Consistency between $input$ rank and $axis$ 
   - Statement: The rank of $X$ shall be greater or equal to $axis$. ($rinput -1\ge axis) 

## Outputs

### $output$: real

Output of the **softmap** operator.

### Constraints

 - `[C1]` Shape consistency
   - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C1]</span></b>](#C1ra) on tensor $A$.

## Attributes

### $axis$

Describes the dimension on which **softmax** is performed.

### Constraints

 - `[C1]` Value domain 
   - Statement: $ axis \ge 0 $
 - `[C2]` Consistency between $input$ rank and $axis$
  - Statement: see constraint [<b><span style="font-family: 'Courier New', monospace">[C2]</span></b>](#C1ra) on tensor $input$.
- 
## Formal specification
 
See the Why3 specification.

