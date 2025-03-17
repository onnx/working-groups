## Preamble

This document gives a high level description of how the execution execution of an ONNX graph. How the graph graph elements are described in the ONNX file is given in the Intermediate Representation (IR) specification document.

In the context of SONNX, the specification of the semantics of an ONNX graph is limited to the inference phase.  

## Graph

- A **graph** is a set of  **nodes** and **edges**
- A **graph** has 
  - zero or more inputs and 
  - at least one output
- An input of the graph is an input of one of the graph's nodes
- An output of the graph is an output of one of the graph's nodes
- A graph is acyclic. This allows nodes to be sorted topologically and be executed according to that order.
   
The following picture gives a simple example of a graph composed of 4 nodes.

 In this example, the inputs of the graph are the inputs of more than one node and the output of the `sub` node is not used.
 - a node output may be unused.  
- 
<p align="center">
<img src="./imgs/graph.png" width="200" />
</p>

*Here is a textual export of same model using `onnx.helper.printable_graph(model.graph)`. Please note that the `sub` operator has been removed since it is bnot used by any other node or as an output of the graph. *
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
## Edges
- An **edge** represents a connection between 
  - the output of a node and the input of another node. 
  - the input of the graph and the input of a node
  - the output of a node and the output of the graph
  
## Node
- A **node** refers to a fully qualified and configured operator ONNX **operator** (version of the operator is defined, attributes of the operators are set) )
- A node has 
  - zero or more inputs and 
  - at least one output
- The inputs and outputs of the node corresponds to the inputs and outputs of the referenced operator.  
- The input of a node is either 
  - connected to the output of another node or
  - an input of the graph
- The output of a node is either 
  - connected to the input of another node or
  - an output of the graph or
  - not connected.

## Execution of a graph
- Executing a graph means evaluating the outputs of the graph
- Evaluating an output of the graph means evaluating the output of the node to which it is connected
- Evaluating an output of a node is achieved by executing the node
- Executing a node means computing the output of the node according to the operator's specification
- Executing a node can be done when all its inputs are defined
- The value of an input is 
  - the value the node output to which it is connected (internal connection) or 
  - the value of the graph input to which it is connected (external connection). 
- Initially, the values of all outputs are not defined. 

## Special nodes
ONNX provides some "special operators" that deserve a specific description:  
- nodes referring to ONNX **function operators**
- nodes referring to control flow operators  (e.g., `if`, `scan`, `loop`,...). 

### Functions nodes
- A `function` operator encapsulates a graph. 
- Executing a function operator means executing the embedded graph according to the graph execution semantics described before. 
- An embedded graph may itself use `function` nodes, in a hierarchical manner. 
- In ONNX, a `function` node is conceptually expanded ("inlined") at the place where it is used. This forbids any direct or indirect recursion (incl. infinite recursion). 


## Control-flow operators 
- ONNX provides a series of control flow operators such as `if`, `scan`, `loop`,...). 
- Those nodes take one (e.g, operators `for`, `loop`, `scan`,...) or two graphs (`if`) has attributes and execute those graph according to their specific semantics. 
- An `if` node, for instance, takes one boolean input and two attributes, one specifying the graph to be executed when the boolean input is true (the `then_branch`) and another graph when the boolean is false (the `else_branch`). 
  - Note that one of the graph is not executed. This seems to contradict the execution semantics of a graph bit ut is not since executing the `then_branch` or the `else_branch` concerns the semantics of the `if` node, not of the graph. From the grph's perspective, the only node that is visible is the `if`. 
  - The same applies for the other control flow nodes.  

## Remarks
According to the previous definitions, the following properties hold:
- A graph is a pure functional construct, i.e., the values of its outputs only depend on the values of its inputs (incl. attributes). This is true as long as all operators are also purely functional, which is the case in the SONNX profile. 
- A graph has no side effect, i.e., the only effects of a graph are via its outputs.
- A graph is deterministic, i.e., the same values of inputs give the same values for outputs. This is true as long as all operators are deterministic, which is the case in the SONNX profile. In particular, 
  - the values of the outputs do not depend on the order according to which the nodes are executed.
  - By construction, a graph makes it explicit the order according to which terms of expressions are computed. For instance, expression `a+b+c` is either represented by `(a+b)+c`or `(a+(B+c)`.  
