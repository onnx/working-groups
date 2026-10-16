*This template only covers one datatype. Do not forget to describe the operator for real numbers and all applicable data types. For structural operators (i.e., operators whose behaviour do not depend on the data type), a single section may suffice.* 

*The text in italics gives indications. It shall not be retained the specification document.*

# Contents

- **Op** operator for type [int8](#int8)


Based on ONNX [Op version 14](https:/...).

<a id="int8"></a>
# **Op** (int8, int8)

## Signature

$Y = \textbf{Op}(A, B)$

where:
- $A$: *brief description of the first argument*
- $B$: *brief description of the second argument*
- $Y$: *brief description of the output*
   
## Restrictions

[General restrictions](/working-groups/safety-related-profile/sonnx/ops/spec/informal/common/general_restrictions.md) are applicable.

The following specific restrictions apply to the **Op** operator:

| Restriction | Statement                                                   | Origin                                                                                      |
|-------------|-------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| `[R1]` <a id="R1"></a> | *Brief decsription of the restriction* | Transient |
| `[R2]` <a id="R2"></a> | *Brief decsription of the restriction*  | [Link to the restriction in the req document](../../../deliverables/reqs/reqs.md#restriction)

*Note: If the restrictions apply to all types, they can be described only once and be replaced by the following text:

`See [Restrictions](#restrictions).` 

*See for instance the case of operator [**MaxPool**](../../spec/informal/maxpool/maxpool.md)*. 

## Informal specification

Operator **Op** [...] *description of the purpose of the operator* [...]


The effect of the operator is illustrated on the following examples.

### Example 1
*Example of usage of operator **Op**".*


## Error conditions
*Description of "error conditions", i.e.,cases where the value produced may be unexpected.*

## Attributes

### `ATTR`: int8

*Attribute description.*

*Note: if the attribute does not depend on the type of the argument (real, float, etc.), then it can be described only once (e.g., in the section for real numbers).* 
*See for instance the case of operator [**MaxPool**](../../spec/informal/maxpool/maxpool.md)*. 

#### Constraints

 - `[C1]` <a id="C1iattr"></a> [See constraint (C1) on A](#C1ia). First constraint on $ATTR$
   - Statement: *Description of the first constraint on `ATTR`.


## Inputs

### $\text{A}$: int8

*Description of the first input.*

#### Constraints

 - `[C1]` <a id="C1ia"></a> First constraint on $A$
   - Statement: Description of the first constraint on $A$
    
### $\text{B}$: int8

*Description of the second input.*

#### Constraints

 - `[C1]` <a id="C1ib"></a> First constraint on $B$
   - Statement: Description of the first constraint on $B$

## Outputs

### $\text{Y}$: int8

*Description of the output.*

#### Constraints

 - `[C1]` <a id="C1iy"></a> First constraint on $Y$
   - Statement: Description of the first constraint on $Y$

