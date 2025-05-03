> **_NOTE:_**  Copy of "graph.md" with notes by Edoardo Manino

# Preamble

This document gives a high level description of how the execution execution of an ONNX graph. How the graph graph elements are described in the ONNX file is given in the Intermediate Representation (IR) specification document.

In the context of SONNX, the specification of the semantics of an ONNX graph is limited to the inference phase.  

> **_NOTE:_**  Typos: "execution" and "graph" are repeated twice. The first sentence is broken: maybe it is meant to say "how the execution of an ONNX graph _takes place_"?

# Informal specification

> **_NOTE:_**  The document does not contain a _formal_ specification (yet?). If it exists in another document, mention that. Also, it may be worth having a little table of content listing the main sections: i.e. structure, behaviour, special nodes, additional remarks.

## Structure 

### Graph
- In ONNX, a **model** is represented by a **graph**. Evaluating a model means evaluating the graph. 
- A **graph**
  - is composed of a set of  **nodes** and **edges**
  - has zero or more inputs and at least one output.

> **_NOTE:_**  Later we state that nodes in the graph may have unused outputs. I can see how that could be helpful, e.g. use a complicated operator for just a few of its outputs, or pad a computational graph with irrelevant operators to avoid side-channel attacks. However, we are losing the nice recursive property that any subgraph of an ONNX graph is also a valid ONNX graph, because an arbitrary subgraph _may not have any outputs_. For an example, see the illustration below: the subgraph containing only the "Sub" node is not a valid ONNX graph. Do we care about this recursive definition? Should we change the definition of ONNX graphs to include graphs without any outputs?

- An **input** or an **output** is either undefined or has a value.

> **_NOTE:_**  Maybe it is worth clarifying the last sentence. By "undefined" do we mean we have not computed its value yet, its value does not matter, or that its value is non-deterministic? When an input/output has a value, can the value change during this specific execution or is it constant once it is computed?

- A **node** 
  - refers to a fully qualified and configured ONNX **operator** (the version of the operator is defined, the attributes of the operators are set). 
  - has inputs and outputs corresponding to the inputs and outputs of the referenced operator.  
- An **edge** 
  - is a connection between an input and an output of two different nodes, or a connection between an input (resp. output) of the graph and an input (resp. output) of a node so that, 

> **_NOTE:_**  I would complete the sentence with "...so that the following constraints hold." and rename the next section as "Graph Constraints".
   
### Constraints
- (C1) Each input of the graph is connected to one or more inputs of its nodes.
- (C2) Each output of the graph is connected to the output of one of its nodes.
- (C3) A graph is acyclic.

> **_NOTE:_**  Should we mention that the graph is also directed? We clearly imply it, since all edges connect the output of a node to the input of another (C5-6).

- (C4) A node has zero or more inputs and at least one output.
- (C5) A node's input is either connected to the output of another node or to an input of the graph.
- (C6) A node's output is either connected to the input of another node, to an output of the graph, or remains unconnected.

> **_NOTE:_**  Typo: "node" is inanimate so we cannot use the Saxon genitive. Say "The input/output of a node" instead of "A node's input/output".

### Illustration
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

## Behaviour
- Evaluating a graph's output requires evaluating the output of the node it is connected to.
- Evaluating a node's output is done by executing the node.

> **_NOTE:_**  Typos: "Evaluating an output of a graph/node"

- Executing a node means computing its outputs based on the specification of the referenced operator.
- A node can only be executed if all its input values are defined.
- Initially, all input values are defined

> **_NOTE:_**  I presume we are referring to the graph inputs, rather than all node inputs? I would also say "before execution", as it is more precise than "initially".

- Initially, all output values are undefined
- All inputs and outputs connected by an edge are either both undefined or have the same value.


## Special nodes

### Functions nodes

> **_NOTE:_** In this section we are using "encapsulate" and "embed" as synonym. I would pick only one for consistency.

- A `function` operator encapsulates a graph. 
- Executing a function operator means executing the embedded graph according to the graph execution semantics described before. 
- An embedded graph may itself use `function` nodes, in a hierarchical manner. 

> **_NOTE:_** We are not saying explicitly whether the same function definition can be reused (called) in more than one node of the graph.

- In ONNX, a `function` node is conceptually expanded ("inlined") at the place where it is used. This forbids any direct or indirect recursion (incl. infinite recursion). 

> **_NOTE:_** The last requirement is crucial, but I feel it is expressed in a potentially ambiguous way. Possible alternative: "A valid ONNX graph with function nodes must be always convertible to an equivalent ONNX graph without any function nodes. This forbids any direct..." On this note, we might need to say explicitly (in the graph definition) that the number of nodes and edges must be finite.

### Control-flow operators 
- ONNX provides a series of control flow operators such as `if`, `scan`, `loop`,...). 
- Those nodes take one (e.g, operators `for`, `loop`, `scan`,...) or two graphs (`if`) as attributes and execute this graph or those graphs according to their specific semantics. 
- An `if` node, for instance, takes one boolean input and two attributes, one specifying the graph to be executed when the boolean input is true (the `then_branch`) and another graph when the boolean is false (the `else_branch`). 
  - Note that one of the graph is not executed. This seems to contradict the execution semantics of a graph bit but is not since executing the `then_branch` or the `else_branch` concerns the semantics of the `if` node, not of the graph. From the graph's perspective, the only node that is visible is the `if`. 
  
  > **_NOTE:_** Hmmm, this paragraph sounds a little defensive. Is this disclaimer really necessary? In section "Behaviour", we do not specify whether all outputs should become defined after execution. Thus, we already allow arbitrary sub-graphs to remain non-executed. Am I missing the point here?
  
  - The same applies for the other control flow nodes.  


## Additional remarks

### Properties of a graph
- If all operators are purely functional (stateless), a graph is also purely functional, i.e., the values of its outputs only only depends on the values of its inputs and the values of the attributes of its nodes. 

> **_NOTE:_**  Typo: "only only" is repeated.

- If all operators are deterministic, a graph is also deterministic, i.e., for a  given set of input values, the execution of the graph always gives the same output values.
- A graph has no side effect, i.e., the only visible effects of a graph are via its outputs.

> **_NOTE:_** Does the latter requirement mean that all operators _must_ be stateless and deterministic? The former two requirements begin with "if", which makes it sound like an option.

Note:
- The values of the outputs do not depend on the execution order of its nodes are executed.

> **_NOTE:_** Typo: "execution order ... are executed".

- By construction, a graph makes it explicit the order according to which terms of expressions are computed. For instance, expression `a+b+c` is either represented by `(a+b)+c`or `(a+(b+c)`

> **_NOTE:_** This requirement contradicts the previous one. The latter seems to forbid non-determinism in the execution order, the former seems to allow it as long as the output stays the same. I would prefer keeping only one of them, with strong preference towards fixing the execution order.

 
## Restrictions
The following restrictions apply to graphs in the SONNX profile:
- `[R1]` A graph shall not contain nodes with no connected outputs. 
  - Rationale: each node of the graph shall contribute to the function of the graph (no "dead node").
 
> **_NOTE:_** Shall we change the illustration then? It contains a node "Sub" with a dangling output. Also, clarify whether I can have a node with multiple outputs, some connected, some disconnected. I think R1 allows it, but another reader may not.
