
# `LSTM` operator (real)

## DRAFT : NOT READY TO BE REVIEWED

### Restrictions
The following restrictions apply to the `LSTM` operator for the SONNX profile:
- The number of spatial axes of the tensors is restricted to 2 ========TBC======`[R1]`
- initial_h, initial_c shall be explicitely set to 0. ========TBC======`[R2]`
- `B` bias tensor is not optional. ========TBC======`[R3]`
- `sequence_length` is not supported . ========TBC======`[R4]`
- `P` is not supported . ========TBC======`[R5]`

### Notations
$\odot$ identifies the Hadamard product, i.e. element wise multiplication.

### Signature
`Y = LSTM(X,W,R,B,initial_h,initial_c)`
where
- `Y`: output tensor
- `X`: input tensor
- `W`: weight tensor
- `R`: recurrence weight tensor  
- `B`: bias tensor
- `initial_h`: value of hidden vector h at $t_0$
- `initial_c`: value of the cell tensor c at $t_0$

#### Informal specification

Operator `LSTM` computes the Long Term Short Term Memory Cell forward, backward, or bidirectional.

The mathematical definition of the LSTM_Forward operator is given hereafter.
$$
\forall t \in [1, seq\_length],
$$
$$
h_0 = initial\_h
$$
$$
c_0 = initial\_c
$$
$$
x_t = X[t-1]
$$
$$
\begin{bmatrix}
i_t \\
o_t \\
f_t \\
g_t 
\end{bmatrix}
=
\begin{bmatrix}
W_{i} & R_{i} \\
W_{o} & R_{o} \\
W_{f} & R_{f} \\
W_{g} & R_{g}
\end{bmatrix}
\times
\begin{bmatrix}
x_t \\
h_{t-1}
\end{bmatrix}
+
\begin{bmatrix}
B_{wi} + B_{ri} \\
B_{wo} + B_{ro} \\
B_{wf} + B_{rf} \\
B_{wg} + B_{rg}
\end{bmatrix}
$$
$$
c_t = act1(f_t) \odot c_{t-1} + act1(i_t) \odot act2(g_t)
$$
$$
h_t = act1(o_t) \odot act3(c_t)
$$
$$
Y[t-1] = h_t
$$

Where
- $i$ is the input gate matrix,
- $o$ is the output gate matrix,
- $f$ is the forget gate matrix,
- $g$ is the cell input gate matrix,
- $c$ is the cell state,
- $h$ is the hidden state,

#### Inputs and outputs

##### `X`

Tensor `X` is the input tensor.
The shape of tensor `X` is $(seq\_length \times batch\_size \times input\_size)$.

###### Constraints

- (C1) Number of spatial axes of tensor `X`
    - Statement: The number of spatial axes of tensor `X` is 2. `[R1]`
    - Rationale: This restriction is intoduced to simplify the implementation considering the actual industrial use cases.

##### `W`

Tensor `W` is the weight input tensor.

The shape of tensor `W` is $(num\_directions \times 4*hidden\_size \times input\_size)$.

$ 
W = 
\begin{bmatrix}
W_{i} \\
W_{o} \\
W_{f} \\ 
W_{g} \\
\end{bmatrix}
$

##### `R`

Tensor `R` is the recurrence weight input tensor.

The shape of tensor `R` is $(num\_directions \times 4*hidden\_size \times hidden\_size)$.

$ 
R = 
\begin{bmatrix}
R_{i} \\
R_{o} \\
R_{f} \\ 
R_{g} \\
\end{bmatrix}
$

##### `B`

Tensor `B` is the bias input tensor.

The shape of tensor `B` is $(num\_directions \times 8*hidden\_size)$.

$
B =
\begin{bmatrix}
B_{wi} \\
B_{wo} \\
B_{wf} \\ 
B_{wg} \\
B_{ri} \\
B_{ro} \\
B_{rf} \\
B_{rg}
\end{bmatrix}
$

##### `Y`

Tensor `Y` is the output tensor.

The shape of tensor `Y` is $(seq\_length \times num\_directions \times batch\_size \times hidden\_size)$.

#### Attributes

##### `direction` - STRINGS

Specify if the RNN is forward, reverse, or bidirectional. Must be one of `forward` (default), `reverse`, or `bidirectional`.
```
Y = LSTM(X){
   num_directions = 1
   if direction == bidirectional
        num_directions = 2
        Y_for = LSTM_Forward(X)
        Y_rev = revert(  LSTM_Forward  (revert(X)))
        Y = concat(Y_for, Y_rev)
   else if direction == forward
        Y =  LSTM_Forward  (X)
   else if direction == backward
        Y =  LSTM_Forward  (revert(X))
}
```


##### `activations` - STRINGS

The value is a coma separated $3 \times STRINGS$ where 'act1, act2, act3' values can be taken in {`Relu`, `Tanh`, `Sigmoid`}.

Defaults to 'Sigmoid, Tanh, Tanh'.

if `direction` is `bidirectional`, the value is a coma separated $6 \times STRINGS$.

Defaults to 'Sigmoid, Tanh, Tanh, Sigmoid, Tanh, Tanh'.

# Graph execution semantics

<div class="note">

Elements of the execution semantics is given on the [IR (Intermediate
Representation) page](https://onnx.ai/onnx/repo-docs/IR.html) of the
ONNX web site. In addition, a Python “reference implementation” is also
provided (see <https://onnx.ai/onnx/api/reference.html>). The source
code of this implementation can be found at
<https://github.com/onnx/onnx/tree/main/onnx/reference>.

Very informally, the semantics is pretty simple: each operator (or
function) is called according to its position in the topological sorting
of the operators. The topological order is a partial order that ensures
that an operator is executed only when its inputs are available. Being a
partial order, it means that several valid orders exist for a given
graph. Normally (?) each order should generate the same result, even in
the presence of floating point operations.

The Python code to execute a graph is given in class
[`ReferenceEvaluator`](https://github.com/onnx/onnx/blob/main/onnx/reference/reference_evaluator.py)).
After having processed the inputs and the initializers (i.e., fed the
`results` dictorionary with these data), the nodes are executed in
sequence. For each operator, the interpretor checks that its inputs are
in the `results` dictionary. If they are not, an error is raised (if the
operators are listed in topological order, this situation should not
occur). Otherwise, the operator is simply executed (method `run`) with
or without a context (composed of the current results) depending on the
type of operators. (Check that this does not create a dependency to the
total order of operators.)

</div>

### Informal specification

<div class="note">

The semantics of an ONNX model is given in Section "Model Semantics" of
the [Intermediate
Representation](https://github.com/onnx/onnx/blob/main/docs/IR.md) page.
Basically, an inference-model is a stateless function (except possibly
for some specific nodes such as a random-generation node) represented by
an acyclic `graph` of nodes. The `graph` is mainly represented by a set
of inputs and outputs and a topologically sorted list of nodes. Each
node represents a call to an operator or a function. A `function` is
itself a graph.

Note that the types of inputs and outputs are not systematically
required because they can be inferred. In our case, I guess that we will
forbib shape inference and rely on static tensor shapes (or, at least,
shape inference can be bone before serializing the model). The proecss
of shape inference is described in Section  [ONNX Shape
Inference](https://onnx.ai/onnx/repo-docs/ShapeInference.html).

</div>

### Formal specification

*To be completed.*

[^3]: See [Why3 documentation](https://www(W)hy3.org/)

[^4]: See [Frama-C
    documentation](https://www.frama-c.com/html/documentation.html)
