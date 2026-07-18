# Eric1
- I think that the concept of "heterogenous" is neither necessary nor clear. \
=> We should probably stick to an explicit list of types. Which is actually what you are doing.

In the signature of CONCAT:
- There is a problem with our convention for tags / tensors. Here, `T1` could be considered as a tensor, while it is a tag.
- Shouldn't $X_i$ be written `Xi` ? (this may be discussed, but we have to be consistent). \
=> To be discussed. The fact that the tags are not in "[]" is also a problem when we want to use them in formulae: the tag are not clearly visible...

Restrictions:
- "Attribute axis lower bound is restricted to 0." \
	=> This is convoluted (and unclear)! use "Attribute axis is positive".

- "dim(inputs)" \
=> what is "dim"? what is "inputs"? (I come back to this later) \
=> Insert line break line before "let a".


- "Let $a$ be the concatenation axis and $d_{k,a}$ `T5` the dimension of the $X_{k}$ input tensor $k$ along the axis $a$." \
=> As far as possible, avoir introducing aliases to inputs, output, etc. (may be useful here, but to be checked).\
=> "the dimension of input tensor $X_{k}$ along the axis $a$."
	
- "The formal specification is given in section Formal specification below."\
=> To be suppressed since this is part of the standard operator description structure.

"Y shape matches the input shapes, except along the axis dimension..."\
=> This is a constraint. Here, we should only see definitions. Constraints will be given later.

- $i_{0}$ and $i_{r-1}$ are the indices which access respectively the first and last dimensions of a tensor to uniquely identify an element. \
=> I don't think that this is necessary since is it clear in the formula. I thinks that it complicates the reading.

- The "prime" on $i_a$ seems to be misplaced (detail)

- In the formula, is it $\exists k$ or "for k such that"? Is it possible for k not to exist?

- Eventually, the picture should be done with drawio that allows using latex formulae.

- What is a "local tensor" in "local tensor X_k".  \
  => Simply use "X_k".

- I am not sure that it is useful to add tag on tensors (ex. tag T3 on k). \
=> In the guidelines for the formal spec, we may ask the names to be maintained between the informal and formal spec.

- Introduce the figure.

- "You can find more examples in tests folder."\
=> To be discussed (in order to uniformize the presentations of ops).

- "a variadic list of input tensors "\
=> This is not the list that is variadic, but the function. \
=> I would simply write "accepts a variable number of input tensors."\
=>  would remove the "e.g., X_0,..." that brings no new info.

"The operator concat is not commutative so the input tensors order impacts on the output tensor."\
=> This is part of the mathematical definition. I would not write this here (otherwise, we will have to make such comments everywhere).\
=> I would not use "heterogeneous" because it is very unclear. it could be interpreted that the different X_i could be of different types.

- C1 is not a really a "value range" (otherwise, every condition could be considered as a "value range"). \
=> I would be more explicit "Limit on argument number"?

- C2: \
=> Check the formula: the ith dimension of a tensor X is normally noted dXi. Here, we can't see the X.

- Add a constraint about the rank of tensors: it is not possible to concat tensors of rank 0 (scalars).

- Attribute "axis", constraint C1\
=> Define "dim(inputs)" using the $dX$ notation.
=> Separate the constraint of being positive (whihc is a restriction) fro the constraint relating the axis to the dimension of the tensors.

- Output, shape consistency\
=> There are two constraints: one about the consistency with the input tensor, and one that is not exactly a consistency constraint, but one of the result of the concatenation operation. I would call the second one "dimension of the concatenation axis" or something similar.




 





