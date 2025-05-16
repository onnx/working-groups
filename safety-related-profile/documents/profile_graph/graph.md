## Restrictions
The following restrictions apply to graphs in the SONNX profile:

| Restriction    | Statement | Origin |
| -------- | ------- | ------- |
| `[R1]` | Each operation outputs must be used in the input mapping of at least one operation or be mapped to some graph output. | To be completed |


# Informal specification (V2) 



## Description
### Graph
A graph is defined by:
- A set of inputs and outputs, which are designated tensors.
- A set of tensors, each of which may initially be uninitialized (no value) or contain a value.
- A set of operations, each of which is an instance of an operator applied to tensors.

### Tensors
- A tensor is a variable that may hold a value or be uninitialized.
- Tensors are uniquely identified within a graph.
- Some tensors may be graph inputs (externally provided) or graph outputs (final results of the computation).

### Operators and Operations
- An operator is a template that defines a computation, including:
  - A fixed number of named inputs and outputs
  - A function that maps input values to output values
- An operation applies an operator to a specific set of input and output tensors:
  - It includes a mapping from operator inputs to graph inputs or other tensors
  - It includes a mapping from operator outputs to graph outputs or other tensors

### Execution Semantics
- Initially, only graph inputs have values.
- An operation is executable if all tensors mapped to its inputs have values.
- Executing an operation computes its outputs and assigns values to its output tensors.
- Execution proceeds by executing all executable operations until no further progress is possible.

### Constraints
- (C1) Single Assignment: A tensor must appear in the output mapping of exactly one operation except for the graph inputs
- (C2) Input Usage: Every graph input must be used in the input mapping of at least one operation.
- (C3) Completeness: At the end of execution, all tensors designated as graph outputs must have values. 

## Restrictions
The following restrictions apply to graphs in the SONNX profile:
- `[R1]` Each operation outputs must be used in the input mapping of at least one operation or be mapped to some graph output. 
  - Rationale: each operation of the graph shall contribute to the function of the graph (no "dead node").
 
## Examples

The following picture gives a simple example of a graph composed of 4 nodes. In this  example, the inputs of the graph are connected to the inputs of two nodes (`add` and `sub`) and the output of the `sub` node is not used.

<p align="center">
<img src="./imgs/graph.png" width="200" />
</p>

Here is a textual export of same model using `onnx.helper.printable_graph(model.graph)`. 

```
graph Test (
  %I1[FLOAT, ?x?]
  %I2[FLOAT, ?x?]
) {
  %O1 = Add(%I1, %I2)
  %op2_out = Constant[value = <Tensor>]()
  %O2 = Mul(%O1, %op2_out)
  %op4_out = Sub(%I1, %I2)
  return %O1, %O2
}
```

*(Note that ONNX also defines another textual serialization scheme (only available in C++)*


## Special nodes

The way graphs are described and executed is independent from the operators used in the graph. In other terms, the semantics of the graph (how the operators are called) and the semantics of the operators (what the operators do) are defined separately. This modularity applies to the standard operators (convolution, relu, etc.) and to the special function and control flow nodes.  

### Functions nodes
- A `function` operator encapsulates a graph. 
- Executing a function operator means executing the encapsulated graph according to the graph execution semantics described before. 
- An encapsulated graph may itself use `function` nodes, in a hierarchical manner. 
- A valid ONNX graph with function nodes must be always actually converted to an equivalent ONNX graph without any function nodes. This forbids any direct or indirect recursion. 

### Control-flow operators 
- ONNX provides a series of control flow operators such as `if`, `scan`, `loop`,...). 
- Those nodes take one (e.g, operators `for`, `loop`, `scan`,...) or two graphs (`if`) as attributes and execute this graph or those graphs according to their specific semantics. 
- An `if` node, for instance, takes one boolean input and two attributes, one attribute specifying the graph to be executed when the boolean input is true (the `then_branch`) and the other specifying the graph to be executed when the boolean is false (the `else_branch`). As for any other operator, the `if`node has a single list of outputs (e.g., [Y1, Y2, ..., Yn]). Both the `then_branch` and the `else_branch` subgraphs must produce the same number and types of outputs, and those are mapped to the outputs of the `if` node.

## Additional remarks

### Properties of a graph
- If all operators are purely functional (stateless), a graph is also purely functional, i.e., the values of its outputs only depends on the values of its inputs and the values of the attributes of its nodes. 
- If all operators are deterministic, a graph is also deterministic, i.e., for a  given set of input values, the execution of the graph always gives the same output values.
- A graph has no side effect, i.e., the only visible effects of a graph are via its outputs.

Note:
- The values of the outputs do not depend on the execution order of its nodes.
- By construction, a graph makes it explicit the order according to which terms of expressions are computed. For instance, expression `a+b+c` is either represented **explicitly** by `(a+b)+c`or `(a+(b+c)`


## Restrictions
The following restrictions apply to graphs in the SONNX profile:
- `[R1]` A graph shall not contain nodes with no connected outputs. 
  - Rationale: each node of the graph shall contribute to the function of the graph (no "dead node").
- `[R2]` A graph shall only contain deterministic operators.

# Formal specification

*Work in progress*