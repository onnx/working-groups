[ERIC] General remark: I have tried to simplify the expression as far as possible. 

Graph

[T01] A graph is defined by:

    A set of inputs and outputs parameters
        An input (resp. output) parameter is a free variable that can be bound to some tensor.
    A set of local (or "internal") tensors.
    A set of nodes


Remarks : 

	-Add a schema of the context of hierarchy of the Graph, with the notion of Node and Operator 
		Model
		 └── Graph
			  └── Node[ ]
					└── Operator (referenced by op_type)

{ERIC] OK, figure to be added.

	- "that can be bound" need to be replace by "must be bound to tensor" 

[ERIC] KO: There is a subtle distinction between a definition ("the free variable **can** be bound to a tensor") and the constraint ("the free variable **must** be bound to a tensor for the graph to be executable".). I keep the definition as is and I ensure that the operational constraint is actually stated somewhere.

	(The node entries must be associated with a tensor, otherwise the calculation can't be performed)
	- Add an Example: A Graph with 2 Nodes and the bindings Tensors inputs/ouputs.

		[input_tensor] --+
						|--[Add]--[add_output_tensor]--[Relu]--[output_tensor]
		[const_tensor]--+



Remarks on Operators and Nodes [T03a] and [T03b] : 
	
	- Precise that in Node " describes the binding of its inputs and outputs " is defined by name and not parameter contrary to the Operator;
		-> "describes the binding of its inputs and outputs by named tensor"
	
	
	- Precise that "A Node can only bind only one Operator." 

[ERIC] OK. 
	
	- Add an example with the same Operator used multiple times.
	
		Example:An Operator [Add] used twice in this Graph.

		Input a ----+
					 |--[Add]--(Output c)---+
		Input b ----+                        |--[Add]--( Output e)
		Input d ----------------------------+

[ERIC] OK, a complete example has been given.

