
# Contents

- **Constant** operator for type [real](#real)
- **Constant** operator for types [float16, float, double](#float)
- **Constant** operator for types [int8, int16, int32, int64, uint8, uint16, uint32, uint64](#int)

<a id="real"></a>

# **Constant** (real)

## Signature

Definition of operator $\text{Constant}$ signature:
$C = \textbf{Constant}(\text{value})$

where:

* `value`: the constant value to fill the output tensor
* `C`: output tensor containing the constant value

## Restrictions

[General restrictions](./../common/general_restrictions.md) are applicable.

Specific restrictions for **Constant**:

- `[R1]` Attribute `value` must be defined.
- `[R2]` Sparse tensors are not supported.
- `[R3]` All elements in `value` must have the same type.

## Informal specification

Operator **Constant** generates a tensor filled with a single constant value specified by the attribute `value`. The output tensor `C` has the same shape and type as defined by `value`.

Mathematically, for all tensor indices $i$:

$$
C[i] = \text{value}[i]
$$

### Example 1

```math
\text{value} = 4.2
```

Result $C$:

```math
C = \begin{bmatrix} 4.2 \end{bmatrix}
```

### Example 2

```math
\text{value} = \begin{bmatrix} 1.1 & 2.2 \\ 3.3 & 4.4 \end{bmatrix}
```

Result $C$:

```math
C = \begin{bmatrix} 1.1 & 2.2 \\ 3.3 & 4.4 \end{bmatrix}
```

## Error conditions

No error condition.

## Attributes

### `value`

* **Description:** The constant value to fill the output tensor.
* **Type:** `tensor(real)`
* **Requirement:** Required `[R1]`.

## Inputs

Not applicable. **Constant** does not take any input tensors.

## Outputs

### `C`: real tensor

Output tensor filled with the constant value.

#### Constraints

- `[C1]` Value consistency

  - Statement: The shape and type of `C` are determined by the attribute `value`. `[R1]` `[R2]` `[R3]`



<a id="float"></a>

# **Constant** (float)

where float is in {float16, float, double}

## Signature

$C = \textbf{Constant}(\text{value})$

where:

- `value`: constant floating-point tensor
- `C`: output tensor containing the constant value

## Restrictions

[General restrictions](./../common/general_restrictions.md) are applicable.

Specific restrictions:

* `[R1]` Attribute `value` must be defined.
* `[R2]` Sparse tensors not supported.
* `[R3]` All elements must have the same floating-point type.

## Informal specification

Operator **Constant** produces a tensor of floating-point values where each element equals the corresponding value in the attribute `value`. Selection follows standard IEEE 754 semantics (NaN and infinity preserved).

### Example 1

```math
\text{value} = 3.14
```

Result $C$:

```math
C = \begin{bmatrix} 3.14 \end{bmatrix}
```

### Example 2

```math
\text{value} = \begin{bmatrix} -0.0 & -\inf \\ \text{NaN} & +\inf \end{bmatrix}
```

Result $C$:

```math
C = \begin{bmatrix} -0.0 & -\inf \\ \text{NaN} & +\inf \end{bmatrix}
```

## Error conditions

No error condition.

## Attributes

### `value`

* **Description:** Constant floating-point tensor to fill output.
* **Type:** `tensor(float16, float, double)`
* **Requirement:** Required `[R1]`.

## Inputs

Not applicable.

## Outputs

### `C`: floating-point tensor

#### Constraints

- `[C1]` Value consistency

  - Statement: Shape and type of `C` determined by attribute `value`. `[R1]` `[R2]` `[R3]`



<a id="int"></a>

# **Constant** (int)

where int is in {int8, int16, int32, int64, uint8, uint16, uint32, uint64}

## Signature

$C = \textbf{Constant}(\text{value})$

where:

- `value`: constant integer tensor
- `C`: output tensor containing the constant value

## Restrictions

[General restrictions](./../common/general_restrictions.md) are applicable.

Specific restrictions:

* `[R1]` Attribute `value` must be defined.
* `[R2]` Sparse tensors not supported.
* `[R3]` All elements must have the same integer type.

## Informal specification

Operator **Constant** produces a tensor of integer values where each element equals the corresponding value in the attribute `value`.

### Example 1

```math
\text{value} = 7
```

Result $C$:

```math
C = \begin{bmatrix} 7 \end{bmatrix}
```

### Example 2

```math
\text{value} = \begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}
```

Result $C$:

```math
C = \begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}
```

## Error conditions

No error condition.

## Attributes

### `value`

* **Description:** Constant integer tensor to fill output.
* **Type:** `tensor(int8, int16, int32, int64, uint8, uint16, uint32, uint64)`
* **Requirement:** Required `[R1]`.

## Inputs

Not applicable.

## Outputs

### `C`: integer tensor

#### Constraints

- `[C1]` Value consistency

  - Statement: Shape and type of `C` determined by attribute `value`. `[R1]` `[R2]` `[R3]`

