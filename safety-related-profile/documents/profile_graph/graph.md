## Graph

- An ONNX graph is a set of  **nodes** connected by **edges** 
 
<p align="center">
<img src="./imgs/graph.png" width="200" />
</p>

*I don't really like mixing mathematical concepts (e.g. graph, nodes) with computer-science concepts (e.g., input, output). Talking about the "input of a graph" sounds pretty strange. This has to be clarified. We may write that an ONNX model is a specific node encapsulating a graph. See tentative below*

## Model
- A **model** is a node encapsulating a graph. 
- A model has zero or more inputs and at least one output
- A model input is connected to one or several inputs of the graph's nodes.
- A model output is connected to the output of one of the graph's nodes.

## Node
- A **node** refers to an ONNX operator. 
- A node has the inputs, outputs and attributes of the operator it represents.  

## Edges
- An **edge** represents a connection between the input of a node and the output of another node. 

## Constraints
- A graph is acyclic. This allows nodes to be sorted topologically and be executed according to that order.
- The input of a node is either 
  - connected to the output of another node or
  - connected to an input of the graph
- The output of a node is either 
  - connected to the input of another node or
  - connected to the output of the model or
  - not connected.

## Execution of a model
- Executing a model means evaluating all outputs of the model.
- Evaluating an output of the model means evaluating the output of the node to which its is connected 
- Evaluating an output of a node means executing the node
- An output of a node is evaluated (defined) by executing the node according its specification
- Executing a node can only be done if all its inputs are defined
- The value of an input is 
  - the value the node output to which it is connected (internal connection) or 
  - the value of the graph input to which it is connected (external connection). 
- Initially, the values of all outputs are undefined. 

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
