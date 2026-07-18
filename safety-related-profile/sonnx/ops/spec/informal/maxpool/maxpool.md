# Contents

- **MaxPool** operator for type [real](#real)
- **MaxPool** operator for types [float16, float, double](#float)
- **MaxPool** operator for types [int8, uint8](#int)

Based on ONNX [MaxPool version 22](https://onnx.ai/onnx/operators/onnx__MaxPool.html).

<a id="real"></a>
# **MaxPool** (real)

## Signature
($Y, \textit{Indices}) = \textbf{MaxPool}(X)$

where:
- $X$: Input tensor
- $Y$: Output tensor containing max value selected from $X$
- $\textit{Indices}$: Output tensor containing the indices in $X$ from where the max values are taken.

<a id="restrictions"></a> 
## Restrictions

[General restrictions](../common/general_restrictions.md) are applicable.

The following specific restrictions apply to the **MaxPool** operator:

| Restriction | Statement                                                   | Origin                                                                                      |
|-------------|-------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| `[R1]` <a id="R1"></a> | Input tensor $X$ has 2 spatial axes | Transient |
| `[R2]` <a id="R2"></a> | All attributes must be explicitly set  | [No default values](../../../../../deliverables/reqs/reqs.md#no_default_value)
| `[R3]` <a id="R3"></a> | Attribute `auto_pad` is restricted to NOTSET  | Transient
| `[R4]` <a id="R4"></a> | Attribute `ceil_mode` is set to zero  | Transient
| `[R5]` <a id="R5"></a> | Attribute `storage_order` is set to zero | Transient

<a id="Informal_spec"></a>
## Informal specification

Operator **MaxPool** consumes an input tensor $X$ and applies max pooling across the tensor according to the kernel shape, strides, dilations and pads. Max pooling consists of computing the max on all values of a subset of the input tensor according to the kernel shape and downsampling the data into the output tensor $Y$.

**MaxPool** is a sliding window operator like **Conv**, for instance. At a given position, the sliding window, called "kernel" or "$W$" in this document, is only there to select the set of elements of $X$ of which the maximum shall be computed. Therefore, only the shape of the kernel matters for **MaxPool**. The shape of $W$ ($dW_0,dW_1$) is given by attribute `kernel_shape`.  
 
Operator **MaxPool** stores in $\textit{Indices}$ the indices of the input tensor $X$ from which the max values are taken. The index values are those of a flatten 1-D view of $X$.

In any position of the kernel over $X_p$, if the max value is present more than once, then the corresponding index value in $\textit{Indices}$ is the one with the lowest value in first spatial dimension (third dimension of $X$), then lowest value in the second spatial dimension (fourth dimension of $X$) that belongs the input tensor $X$.

The mathematical definition of output $Y$ and $\textit{Indices}$ are given hereafter:


$$\begin{gathered}
    Y[b, c, m, n] = \text{max}_{h=0}^{dW_0-1} \text{max}_{w=0}^{dW_1-1} \\ X_p[b,c,m \cdot \text{strides}[0]+ h \cdot \text{dilations}[0], n \cdot \text{strides}[1]+ w \cdot \text{dilations}[1] ]
\end{gathered}$$

Let 

$$I = \{ (h,w)~|~Y[b,c,m,n] = X[b,c,h,w]\}$$

$$(h_{min},w_{min})=\text{argmin}_{(h,w) \in I} h.dW_3+w $$ 

$$\begin{gathered}
    \textit{Indices}[b, c, m, n] = b \cdot (dX_1 \cdot dX_2 \cdot dX_3) + c \cdot (dX_2 \cdot dX_3) + h_{min} \cdot dX_3 + w_{min} 
\end{gathered}$$

Where
- $b \in [0,dY_0-1]$ is the batch index. $dY_0$ is the batch size of output $Y$
- $c \in [0,dY_1-1]$ is the data channel. $dY_1$ is the number of data channels of output $Y$
- $dW_0$ is the dimension of the first spatial axis of the kernel, i.e., the first value of attribute `kernel_shape`
- $dW_1$ is the dimension of the second spatial axis of the kernel, i.e., the second value of attribute `kernel_shape`
- `strides` is an attribute of the operator. It will be described later in this section.
- `dilation` is an attribute of the operator. It will be described later in this section.
- $X_{p} = \text{pad}(X,pads)$ is the padded version of the input tensor $X$. Function $\text{pad}$ applies padding as specified by attribute [pads](#real_pads).

### A graphical view of MaxPool

<img src="./assets/imgs/MaxPool_with_dilation.drawio.png" width="650" />

### Example

$\textit{Y},\textit{Indices} = \text{MaxPool}(X)$

- Shape of $X$ = [1, 1, 8, 8]
- kernel\_shape = [3,3]
- pads = [0,0,0,0]
- dilation = [1,1]
- strides = [1,1]
- Shape of $Y$ = [1, 1, 6, 6]
- Shape of $\textit{Indices}$ = [1, 1, 6, 6]


```math
X =
\begin{bmatrix}
  \begin{bmatrix}
    \begin{bmatrix}
        5.67591154 & -0.04859958 & 2.94203104 & 3.70327292 & 2.47014306 & 4.12455586 & 5.81838665 & 1.84118807 \\
        -0.05267874 & 2.75227858 & 2.16608732 & 4.03416243 & 1.28184638 & 4 81748948 & 4.64878412 & 3.31626988 \\
        3.55427648 & 0.39997585 & 4.45761508 & 4.82722666 & 0.18843372 & 0.49564314 & 7.96647029 & 4.82851447 \\
        1.52417623 & 2.28965587 & 0.36251913 & 1.64413983 & 4.67267459 & 3.73167179 & 2.20052118 & 2.06720836 \\
        -1.22446366 & -0.86469519 & 6.01461967 & -1.08813165 & 2.11920055 & 0.78561867 & 0.29834533 & 1.94499626 \\
        1.57776732 & 3.64260188 & 3.47181319 & 4.83723727 & 1.49868674 & 3.27683692 & 2.42625178 & 0.4401565 \\
        6.8972704 & 5.51113868 & 5.99293336 & 4.24088721 & 1.94993561 & -0.04040625 & 3.07940675 & 3.06769141 \\
        3.1299626 & 4.5546675 & 3.5008191 & 2.06181403 & 3.27400104 & 6.70386189 & 0.92777015 & -1.29092574
    \end {bmatrix}
  \end {bmatrix}
\end {bmatrix}
```

```math
Y =
\begin{bmatrix}
  \begin{bmatrix}
    \begin{bmatrix}
        5.67591154 & 4.82722666 & 4.82722666 & 4.82722666 & 7.96647029 & 7.96647029 \\
        4.45761508 & 4.82722666 & 4.82722666 & 4.82722666 & 7.96647029 & 7.96647029 \\
        6.01461967 & 6.01461967 & 6.01461967 & 4.82722666 & 7.96647029 & 7.96647029 \\
        6.01461967 & 6.01461967 & 6.01461967 & 4.83723727 & 4.67267459 & 3.73167179 \\
        6.8972704 & 6.01461967 & 6.01461967 & 4.83723727 & 3.27683692 & 3.27683692 \\
        6.8972704 & 5.99293336 & 5.99293336 & 6.70386189 & 6.70386189 & 6.70386189
    \end {bmatrix}
  \end {bmatrix}
\end {bmatrix}
```

```math
\textit{Indices} = 
\begin{bmatrix}
  \begin{bmatrix}
    \begin{bmatrix}
        0 & 19 & 19 & 19 & 22 & 22 \\
        18 & 19 & 19 & 19 & 22 & 22 \\
        34 & 34 & 34 & 19 & 22 & 22 \\
        34 & 34 & 34 & 43 & 28 & 29 \\
        48 & 34 & 34 & 43 & 45 & 45 \\
        48 & 50 & 50 & 61 & 61 & 61
    \end {bmatrix}
  \end {bmatrix}
\end {bmatrix}
```


## Error conditions
No error conditions.

<a id="real_attributes"></a>
## Attributes

### `auto_pad`: string

The `auto_pad` attribute determines if and how automatic padding is done for the input tensor X.

#### Constraints
-  `[C1]`: Value domain 
    - Statement: `auto_pad` shall be in set {NOTSET, VALID, SAME_UPPER, SAME_LOWER}. 
    - Rationale: [`[R2]`](#R2)
-  `[C2]`: Explicit padding 
    - Statement: `auto_pad` shall be set to NOTSET. 
    - Rationale: [`[R3]`](#R3)

<a id="ceil_mode"></a>
### `ceil_mode`: int

Whether to use floor (0, default) or ceil (1) to compute the output shape. See the description of output $Y$.

#### Constraints
-  `[C1]`: Value domain 
    - Statement: `ceil_mode` shall be in {0, 1}.
    - Rationale: [`[R2]`](#R2)
-  `[C2]`: floor mode is selected 
    - Statement: `ceil_mode` shall be set to 0.
    - Rationale: [`[R4]`](#R4)

### `dilations`: list of ints

Dilation value along each spatial axis of filter.

Attribute `dilations` specifies the spacing between the elements of $W$. The ith value in the list gives the dilation factor for spatial axis $i$. If the dilation factor is greater than 1 for axis $i$, then the kernel elements are spaced out by the dilation factor for that axis. 

The effect of the `dilations` attribute for a tensor with two spatial axes is depicted on the following figure.  

<img src="../common/assets/sliding_window_ops/imgs/dilation.png" width="300" />

In the example above:
- `dilations`=(2,2)
- Before dilation, $W$ contains only 1s. Those 1s are used as selectors of values of $X$.
- After dilation, a '0' means that the value in $X$ is not selected.
- The offset between two '1' in the dilated $W$ along one spacial axis equals the dilation value for that axis, i.e., '2' in the example. Therefore, at a given position of $W$ on $X$, one value of $X$ over two is selected for computing the max along each spatial axis. 
  
#### Constraints
- `[C1]`: Value domain
    - Statement: `dilations` is a list of strictly positive integers
    - Rationale: The dilation is a *factor of expansion* along a certain axis.
- `[C2]`: Relation between `dilations` and $X$ 
    - Statement: the length of the `dilations` list is the number of spatial dimensions of $X$ ([see constraint `C1` of $X$](#C1ia)).
    - Rationale: Dilation is defined for all spatial axes of $X$.
- `[C3]`: Consistency between the shape of tensors $Y$, $X$ and attributes `kernel_shape`, `pads`, `dilations` and `strides`  
    - Statement: [see constraint `C2` of $Y$](#shape_consist)


### `kernel_shape`: list of ints

The size of the kernel along each spatial axis.

#### Constraints
- `[C1]`: Value domain
    - Statement: `kernel_shape` is a list of strictly positive integers
    - Rationale: The max must be computed on at least one element.
- `[C2]`: Relation between `kernel_shape` and $X$ 
    - Statement: the length of `kernel_shape` is the number of spatial axes of $X$.
    - Rationale: `kernel_shape` is defined for all spatial axes of $X$.
- `[C3]`: Relation between `kernel_shape`and `pads`
    - Statement: [see constraint `[C2]` of `pads`](#Keff_less_than_pads)
- `[C4]`: Consistency between the shape of tensors $Y$, $X$ and attributes `kernel_shape`, `pads`, `dilations` and `strides`  
    - Statement: [see constraint `[C1]` and `[C2]` of $Y$](#shape_consist)

<a id="real_pads"></a>
### `pads`: list of ints

Attribute `pads` determines the padding at the beginning and end along each spatial axis of the input tensor $X$.

`pads` is a list of the form (x1_begin, x2_begin, x1_end, x2_end), where xi_begin is the number of elements (possibly zero) added at the beginning of axis $i$ and xi_end is the number of elements added at the end of axis $i$.

The value of the padding constant depends on the input tensor data type. Therefore:
- see [floating-point value to pad](#pad_const_float_val)
- see [integer values to pad](#pad_const_int_val)

The effect of the `pads` attribute is illustrated on the following figure on integers. In this example,  `pads`=(2,1,2,2) and the padded value is the one for type uint8, i.e., zero.

<img src="../common/assets/sliding_window_ops/imgs/onnx_conv_padop2.png" alt="drawing" width="80%"/>

#### Constraints
- `[C1]`: Consistency between the shape of $X$ and the length of `pads`
    - Statement: The length of the `pads` list is twice the number of spatial axes of $X$
    - Rationale: Padding shall be given for all spatial axes, and a begining value and an end value must be given for each axis.
- `[C2]`<a id="Keff_less_than_pads"></a> : Consistency between `pads`, `kernel_shape`, and `dilation`
    - Statement: Each dimension of the possibly dilated kernel shall be strictly greater than the greatest value in `pads` for the same dimension, i.e.:
        $Ke_i > \text{max}(pads[i], pads[i+2])$
        where $Ke_i = (\texttt{dilations}[i] * (\texttt{kernel\_shape}[i] - 1) + 1)$
    - Rationale: This constraint guarantees that the max value returned by **MaxPool** belongs to $X$.
- `[C3]`: Consistency between the shape of tensors $Y$, $X$ and attributes `kernel_shape`, `pads`, `dilations` and `strides`  
    - Statement: [See constraint `[C1]` of Y](#shape_consist)

### `storage_order`: int

The storage order of the tensor. 0 is row major, and 1 is column major.

#### Constraints
-  `[C1]`: Explicit storage order
    - Statement: `storage_order` shall be set to zero.
    - Rationale: [`[R2]`](#R2), [`[R5]`](#R5)

### `strides`: list of ints

Attribute `strides` determines how the kernel is applied on tensor $X$ during the **MaxPool**.

For instance, with $\texttt{stride}[0]=3$ and $\texttt{stride}[1]=2$, the kernel is applied to data 2 units on right in the first spatial axis and to data 3 units down in the second spatial axis at each step of the max pooling.

The effect of the `strides` attribute is illustrated on the following figure. In this example, `strides`=(3,2).

<img src="../common/assets/sliding_window_ops/imgs/conv_stride3.png" width="300" />

#### Constraints
- `[C1]`: Value domain
    - Statement: `strides` is a list of strictly positive integers.
    - Rationale: Stride values represent the number of applications of the kernel in the two spatial dimensions
- `[C2]`: Relation between `strides` and $X$ 
    - Statement: the length of the `strides` list is the number of spatial dimensions of $X$ ([see constraint `C1` of $X$](#C1ia)).
    - Rationale: Dilation is defined for all spatial axes of $X$.
- `[C3]`: Consistency between the shape of tensors $Y$, $X$ and  attributes `kernel_shape`, `pads`, `dilations` and `strides`
    - Statement: [See constraint `[C1]` of Y](#shape_consist)

## Inputs

### $\text{X}$: real

$X$ is the input tensor from which the max values are selected. 


#### Constraints

- `[C1]` <a id="C1ia"></a> Number of spatial axes
    - Statement: The number of spatial axes of tensor $X$ is 2. 
    - Rationale: [`[R1]`](#R1).
- `[C2]`: Consistency between the shape of tensors $Y$, $X$ and  attributes `kernel_shape`, `pads`, `dilations` and `strides`
    - Statement: [See constraint `[C1]` of Y](#shape_consist)


## Outputs

### $\text{Y}$: real

The shape of the output $Y$ is $(dY_0 , dY_1 , dY_2 , dY_3)$ where
- $dY_0$ is the number of batches
- $dY_1$ is the number of channels
- $dY_2$ and $dY_3$ are the sizes of the output for the two spatial axes

#### Constraints.
- `[C1]`: <a id="shape_consist"></a> Consistency between the shape of tensors $Y$, $X$, and attributes `kernel_shape`, `pads`, `dilations` and `strides`
    - Statement:
        - $dY_2 = \left\lfloor{((dX_2 + pad\_shape[0] - (\texttt{dilations}[0] * (\texttt{kernel\_shape}[0] - 1) + 1)) / \texttt{strides}[0]) + 1}\right\rfloor$
        - $dY_3 = \left\lfloor{((dX_3 + pad\_shape[1] - (\texttt{dilations}[1] * (\texttt{kernel\_shape}[1] - 1) + 1)) / \texttt{strides}[1]) + 1}\right\rfloor$
        - where $pad\_shape[i]$ is the sum of the pads along spatial axis $i$ 
        - In the previous formulae, `ceil_mode`(#ceil_mode) is considered set to 0 ([see `ceil_mode` definition](#ceil_mode)).
  

### $\text{Indices}$: int64

$\textit{Indices}$ contains the indices of the input tensor $X$ from which the max values are taken.

#### Constraints

 - `[C1]` <a id="C1iy"></a> First constraint on $\textit{Indices}$
   - Statement: $\textit{Indices}$ and $Y$ shall have the same shape

<a id="float"></a>
# **MaxPool** (float)
where float is in {float16, float, double}


## Signature
($Y, \textit{Indices}) = \textbf{MaxPool}(X)$

where:
- $X$: Input tensor
- $Y$: Output tensor containing max value selected from $X$
- $\textit{Indices}$: Output tensor containing the indices in $X$ from where the max values are taken.
   
## Restrictions

See [Restrictions](#restrictions).

## Informal specification
The specification of **MaxPool** for the floating point numbers is identical to the specification for reals, with the following modifications:
- The $\text{Max}$ operator becomes $\text{Max}_F$
- The padding value becomes -Inf.

The effect of the operator is illustrated on the following examples.

### Example 1

$\textit{Y},\textit{Indices} = \text{MaxPool}(X)$

- Data type: double
- Shape of $X$ = [1, 1, 3, 3]
- kernel_shape = [2,2]
- pads = [0,0,0,0]
- dilation = [1,1]
- strides = [1,1]
- Shape of $Y$ = [1, 1, 2, 2]
- Shape of $\textit{Indices}$ = [1, 1, 2, 2]


```math
X =
\begin{bmatrix}
  \begin{bmatrix}
    \begin{bmatrix}
        1.70792822 & 1.59383029 & 2.22933891 \\
        1.39774388 & 2.03411151 & 3.15139065 \\
        2.81201102 & 5.85721996 & 3.55039159 \\
    \end {bmatrix}
  \end {bmatrix}
\end {bmatrix}
```

```math
Y =
\begin{bmatrix}
  \begin{bmatrix}
    \begin{bmatrix}
        2.03411151 & 3.15139065 \\
        5.85721996 & 5.85721996 \\
    \end {bmatrix}
  \end {bmatrix}
\end {bmatrix}
```

```math
\textit{Indices} = 
\begin{bmatrix}
  \begin{bmatrix}
    \begin{bmatrix}
        4 & 5 \\
        7 & 7 \\
    \end {bmatrix}
  \end {bmatrix}
\end {bmatrix}
```

### Example 2

$\textit{Y},\textit{Indices} = \text{MaxPool}(X)$

- Data type: double
- Shape of $X$ = [1, 1, 3, 3]
- kernel\_shape = [2,2]
- pads = [1,0,1,0]
- dilation = [1,1]
- strides = [1,1]
- Shape of $Y$ = [1, 1, 4, 2]
- Shape of $\textit{Indices}$ = [1, 1, 4, 2]


```math
X =
\begin{bmatrix}
  \begin{bmatrix}
    \begin{bmatrix}
        2.41529657 & 0.12586645 & 5.17877496 \\
        5.82770299 & 3.77328965 & 3.51988829 \\
        1.40679595 & 3.95043140 & -1.37421443 \\
    \end {bmatrix}
  \end {bmatrix}
\end {bmatrix}
```

```math
Y =
\begin{bmatrix}
  \begin{bmatrix}
    \begin{bmatrix}
        2.41529657 & 5.17877496 \\
        5.82770299 & 5.17877496 \\
        5.82770299 & 3.95043140 \\
        3.95043140 & 3.95043140 \\
    \end {bmatrix}
  \end {bmatrix}
\end {bmatrix}
```

```math
\textit{Indices} = 
\begin{bmatrix}
  \begin{bmatrix}
    \begin{bmatrix}
        0 & 2 \\
        3 & 2 \\
        3 & 7 \\
        7 & 7 \\
    \end {bmatrix}
  \end {bmatrix}
\end {bmatrix}
```

### Example 3
 
> Rajouter la contrainte sur la taille du padding (inférieure taille kernel)

$\textit{Y},\textit{indices} = \text{MaxPool}(X)$

- Data type: double
- Shape of $X$ = [1, 1, 3, 3]
- kernel\_shape = [2,2]
- pads = [0,0,0,0]
- dilation = [1,1]
- strides = [1,1]
- Shape of $Y$ = [1, 1, 2, 2]
- Shape of $\textit{indices}$ = [1, 1, 2, 2]


```math
X =
\begin{bmatrix}
  \begin{bmatrix}
    \begin{bmatrix}
        -inf & -inf & 4.56432533 \\
        -inf & -inf & 2.55354471 \\
        2.83691720 & 3.46789489 & 5.23979851 \\
    \end {bmatrix}
  \end {bmatrix}
\end {bmatrix}
```

```math
Y =
\begin{bmatrix}
  \begin{bmatrix}
    \begin{bmatrix}
        -inf & 4.56432533e+000 \\
        3.46789489e+000 & 5.23979851e+000 \\
    \end {bmatrix}
  \end {bmatrix}
\end {bmatrix}
```

```math
\textit{Indices} = 
\begin{bmatrix}
  \begin{bmatrix}
    \begin{bmatrix}
        0 & 2 \\
        7 & 8 \\
    \end {bmatrix}
  \end {bmatrix}
\end {bmatrix}
```

### Example 4

$\textit{Y},\textit{Indices} = \text{MaxPool}(X)$

- Data type: double
- Shape of $X$ = [1, 1, 3, 3]
- kernel\_shape = [2,2]
- pads = [1,1,1,1]
- dilation = [1,1]
- strides = [1,1]
- Shape of $Y$ = [1, 1, 4, 4]
- Shape of $\textit{Indices}$ = [1, 1, 4, 4]


```math
X =
\begin{bmatrix}
  \begin{bmatrix}
    \begin{bmatrix}
        -inf & 9.57875561 & 4.56432533 \\
        2.72844928 & 3.54234851 & 2.55354471 \\
        2.83691720 & 3.46789489 & 5.23979851 \\
    \end {bmatrix}
  \end {bmatrix}
\end {bmatrix}
```

```math
Y =
\begin{bmatrix}
  \begin{bmatrix}
    \begin{bmatrix}
        -inf & 9.57875561e+000 & 9.57875561e+000 & 4.56432533e+000 \\
        2.72844928e+000 & 9.57875561e+000 & 9.57875561e+000 & 4.56432533e+000 \\
        2.83691720e+000 & 3.54234851e+000 & 5.23979851e+000 & 5.23979851e+000 \\
        2.83691720e+000 & 3.46789489e+000 & 5.23979851e+000 & 5.23979851e+000 \\
    \end {bmatrix}
  \end {bmatrix}
\end {bmatrix}
```

```math
\textit{Indices} = 
\begin{bmatrix}
  \begin{bmatrix}
    \begin{bmatrix}
        0 & 1 & 1 & 2 \\
        3 & 1 & 1 & 2 \\
        6 & 4 & 8 & 8 \\
        6 & 7 & 8 & 8 \\
    \end {bmatrix}
  \end {bmatrix}
\end {bmatrix}
```

### Discrepancies observed in an existing implementations

**WARNING: Non compliances with the SONNX specification have been observed on the ONNX Runtime implementation (version 1.23.2).**

> S'assurer que les tests suivants ont été exécutés sur la bonne version d'ORT.

Non compliance concern both the max values ($Y$) and the indices ($\text{indices}$). Refer to this [jupyter notebook](../../tests/maxpool/maxpool_divergence.ipynb) for further details on the observed problems.

> Mettre les exemples dans `maxpool_doc.ypnb`.  

For instance, example 3 above executed on ONNX runtime with CPU provider produces the following output tensors:

```math
Y =
\begin{bmatrix}
  \begin{bmatrix}
    \begin{bmatrix}
        -1.79769313e+308 & 4.56432533e+000 \\
        3.46789489e+000 & 5.23979851e+000 \\
    \end {bmatrix}
  \end {bmatrix}
\end {bmatrix}
```

```math
\textit{Indices} = 
\begin{bmatrix}
  \begin{bmatrix}
    \begin{bmatrix}
        -4 & 2 \\
        7 & 8 \\
    \end {bmatrix}
  \end {bmatrix}
\end {bmatrix}
```

Two discrepancies appear:
- in $Y$: -1.79769313e+308 instead of -inf as first element.
- in $\textit{Indices}$: $-4$ instead of $0$ (first element of $X$).

## Error conditions
No error conditions.

## Attributes

Cf. float.

## Inputs

Cf. float.

## Outputs

Cf. float.

<a id="int"></a>
# **MaxPool** (int)
where int is in {int8, uint8}.

## Signature

($Y, \textit{Indices}) = \text{MaxPool}(X)$

where:
- $X$: input tensor
- $Y$: output tensor containing max value selected from $X$
- $\textit{Indices}$: output tensor containing the indices in $X$ from where the max values are taken.
   
## Restrictions

See [Restrictions](#restrictions).


## Informal specification
The specification of **MaxPool** for integer numbers is identical to the specification for reals, with the following modification:
- The padding value becomes the minimum value for the type (minint8 for int8 and 0 for uint8).

The effect of the operator is illustrated on the following examples.

### Example 1:

$\textit{Y},\textit{indices} = \text{MaxPool}(X)$

- Data type: int8
- Shape of $X$ = [1, 1, 3, 3]
- kernel\_shape = [2,2]
- pads = [0,0,0,0]
- dilation = [1,1]
- strides = [1,1]
- Shape of $Y$ = [1, 1, 2, 2]
- Shape of $\textit{Indices}$ = [1, 1, 2, 2]


```math
X =
\begin{bmatrix}
  \begin{bmatrix}
    \begin{bmatrix}
        -12 & -13 &  5 \\
        -14 & -15 &  6 \\
        7 &  8 & -1 \\
    \end {bmatrix}
  \end {bmatrix}
\end {bmatrix}
```

```math
Y =
\begin{bmatrix}
  \begin{bmatrix}
    \begin{bmatrix}
        -12 & 6 \\
        8 & 8 \\
    \end {bmatrix}
  \end {bmatrix}
\end {bmatrix}
```

```math
\textit{Indices} = 
\begin{bmatrix}
  \begin{bmatrix}
    \begin{bmatrix}
        0 & 5 \\
        7 & 7 \\
    \end {bmatrix}
  \end {bmatrix}
\end {bmatrix}
```

### Example 2:

$\textit{Y},\textit{indices} = \text{MaxPool}(X)$

- Data type: int8
- Shape of $X$ = [1, 1, 3, 3]
- kernel\_shape = [2,2]
- pads = [0,0,0,0]
- dilation = [1,1]
- strides = [1,1]
- Shape of $Y$ = [1, 1, 2, 2]
- Shape of $\textit{Indices}$ = [1, 1, 2, 2]


```math
X =
\begin{bmatrix}
  \begin{bmatrix}
    \begin{bmatrix}
        -128 & -128 & 5 \\
        -128 & -128 & 6 \\
        7 & 8 & -1 \\
    \end {bmatrix}
  \end {bmatrix}
\end {bmatrix}
```

```math
Y =
\begin{bmatrix}
  \begin{bmatrix}
    \begin{bmatrix}
        -128 & 6 \\
        8 & 8 \\
    \end {bmatrix}
  \end {bmatrix}
\end {bmatrix}
```

```math
\textit{Indices} = 
\begin{bmatrix}
  \begin{bmatrix}
    \begin{bmatrix}
        0 & 5 \\
        7 & 7 \\
    \end {bmatrix}
  \end {bmatrix}
\end {bmatrix}
```

### Example 3

$\textit{Y},\textit{indices} = \text{MaxPool}(X)$

- Data type: int8 
- Shape of $X$ = [1, 1, 3, 3]
- kernel\_shape = [2,2]
- pads = [0,1,1,1]
- dilation = [1,1]
- strides = [1,1]
- Shape of $Y$ = [1, 1, 3, 4]
- Shape of $\textit{Indices}$ = [1, 1, 3, 4]


```math
X =
\begin{bmatrix}
  \begin{bmatrix}
    \begin{bmatrix}
        1 & 2 & 0 \\
        0 & 3 & 5 \\
        -2 & 5 & 6 \\
    \end {bmatrix}
  \end {bmatrix}
\end {bmatrix}
```

```math
Y =
\begin{bmatrix}
  \begin{bmatrix}
    \begin{bmatrix}
        1 & 3 & 5 & 5 \\
        0 & 5 & 6 & 6 \\
        -2 & 5 & 6 & 6 \\
    \end {bmatrix}
  \end {bmatrix}
\end {bmatrix}
```

```math
\textit{Indices} = 
\begin{bmatrix}
  \begin{bmatrix}
    \begin{bmatrix}
        0 & 4 & 5 & 5 \\
        3 & 7 & 8 & 8 \\
        6 & 7 & 8 & 8 \\
    \end {bmatrix}
  \end {bmatrix}
\end {bmatrix}
```

### Example 4

$\textit{Y},\textit{indices} = \text{MaxPool}(X)$

- Data type: int8
- Shape of $X$ = [1, 1, 3, 3]
- kernel\_shape = [2,2]
- pads = [1,1,1,1]
- dilation = [1,1]
- strides = [1,1]
- Shape of $Y$ = [1, 1, 4, 4]
- Shape of $\textit{Indices}$ = [1, 1, 4, 4]


```math
X =
\begin{bmatrix}
  \begin{bmatrix}
    \begin{bmatrix}
        -128 & -127 & 5 \\
        -128 & -127 & 6 \\
        7 & 8 & -128 \\
    \end {bmatrix}
  \end {bmatrix}
\end {bmatrix}
```

```math
Y =
\begin{bmatrix}
  \begin{bmatrix}
    \begin{bmatrix}
        -128 & -127 & 5 & 5 \\
        -128 & -127 & 6 & 6 \\
        7 & 8 & 8 & 6 \\
        7 & 8 & 8 & -128 \\
    \end {bmatrix}
  \end {bmatrix}
\end {bmatrix}
```

```math
\textit{Indices} = 
\begin{bmatrix}
  \begin{bmatrix}
    \begin{bmatrix}
        0 & 1 & 2 & 2 \\ 
        3 & 1 & 5 & 5 \\
        6 & 7 & 7 & 5 \\
        6 & 7 & 7 & 8 \\
    \end {bmatrix}
  \end {bmatrix}
\end {bmatrix}
```

### Example 5

$\textit{Y},\textit{indices} = \text{MaxPool}(X)$

- Data type: uint8
- Shape of $X$ = [1, 1, 3, 3]
- kernel\_shape = [2,2]
- pads = [1,1,1,1]
- dilation = [1,1]
- strides = [1,1]
- Shape of $Y$ = [1, 1, 4, 4]
- Shape of $\textit{Indices}$ = [1, 1, 4, 4]


```math
X =
\begin{bmatrix}
  \begin{bmatrix}
    \begin{bmatrix}
        0 & 1 & 5 \\
        1 & 1 & 6 \\
        7 & 8 & 0 \\
    \end {bmatrix}
  \end {bmatrix}
\end {bmatrix}
```

```math
Y =
\begin{bmatrix}
  \begin{bmatrix}
    \begin{bmatrix}
        0 & 1 & 5 & 5 \\
        1 & 1 & 6 & 6 \\
        7 & 8 & 8 & 6 \\
        7 & 8 & 8 & 0 \\
    \end {bmatrix}
  \end {bmatrix}
\end {bmatrix}
```

```math
\textit{Indices} = 
\begin{bmatrix}
  \begin{bmatrix}
    \begin{bmatrix}
         0 & 1 & 2 & 2 \\
         3 & 1 & 5 & 5 \\
         6 & 7 & 7 & 5 \\
         6 & 7 & 7 & 8 \\
    \end {bmatrix}
  \end {bmatrix}
\end {bmatrix}
```


### Discrepancies observed in an existing implementation

> Reporter les modifs ci-dessus.

Runnning Example 4 above on ONNX runtime with CPU as provider produces the following $\textit{Indices}$ output tensor:

```math
\textit{Indices} = 
\begin{bmatrix}
  \begin{bmatrix}
    \begin{bmatrix}
        -4 & 1 & 2 & 2 \\ 
        -4 & 1 & 5 & 5 \\
        6 & 7 & 7 & 5 \\
        6 & 7 & 7 & -4 \\
    \end {bmatrix}
  \end {bmatrix}
\end {bmatrix}
```

The following discreapancies of the same kind appear in it:
- $-4$ instead of $0$ (first element of $X$).
- $-4$ instead of $3$ (fourth element of $X$).
- $-4$ instead of $8$ (ninth element of $X$).


## Error conditions
No error conditions.

## Attributes

See reals.

## Inputs

See reals.

## Outputs

See reals.
