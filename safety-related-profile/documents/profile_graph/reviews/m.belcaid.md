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
					
	- "that can be bound" need to be replace by "must be bound to tensor" 
	(The node entries must be associated with a tensor, otherwise the calculation can't be performed)
	- Add an Example: A Graph with 2 Nodes and the bindings Tensors inputs/ouputs.

		[input_tensor]--+
			 	|--[Add]--[add_output_tensor]--[Relu]--[output_tensor]
		[const_tensor]--+



Remarks on Operators and Nodes [T03a] and [T03b] : 
	
	- Precise that in Node " describes the binding of its inputs and outputs " is defined by name and not parameter contrary to the Operator;
		-> "describes the binding of its inputs and outputs by named tensor"
	- Precise that "A Node can only bind only one Operator." 
	- Add an example with the same Operator used multiple times.
	
		Example:An Operator [Add] used twiced in this Graph.

		Input a ----+
			     |--[Add]--(Output c)---+
		Input b ----+                        |--[Add]--( Output e)
		Input d ----------------------------+
