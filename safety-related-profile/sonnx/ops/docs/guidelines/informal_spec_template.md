# Contents

- **Op** operator for type [int8](#int8)


Based on ONNX documentation [Op version 14](https:/...).

<a id="int8"></a>
# **Op** (int8, int8)

## Signature
Definition of operator $\text{Op}$ signature:
$Y = \textbf{Op}(A, B)$

where:
- $A$: first input
- $B$: second input
- $Y$: first result
   
## Restrictions

[General restrictions](/working-groups/safety-related-profile/sonnx/ops/spec/informal/common/general_restrictions.md) are applicable.

The following specific restrictions apply to the **Op** operator:

| Restriction | Statement                                                   | Origin                                                                                      |
|-------------|-------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| `[R1]` <a id="R1"></a>    | First restriction                             | Type of restriction

## Informal specification

Operator **Op** ...


The effect of the operator is illustrated on the following examples.

### Example 1
...


## Error conditions
....

## Attributes

### $\text{ATTR}$: int8

*Attribute description*

#### Constraints

 - `[C1]` <a id="C1iattr"></a> [See constraint (C1) on A](#C1ia). First constraint on $ATTR$
   - Statement: Description of the first constraint on $ATTR$

## Inputs

### $\text{A}$: int8

*First input description*

#### Constraints

 - `[C1]` <a id="C1ia"></a> First constraint on $A$
   - Statement: Description of the first constraint on $A$
    
### $\text{B}$: int8

*Second input description*

#### Constraints

 - `[C1]` <a id="C1ib"></a> First constraint on $B$
   - Statement: Description of the first constraint on $B$

## Outputs

### $\text{Y}$: int8

*Output description*

#### Constraints

 - `[C1]` <a id="C1iy"></a> First constraint on $Y$
   - Statement: Description of the first constraint on $Y$

