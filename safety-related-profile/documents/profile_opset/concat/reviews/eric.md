- About R1
  - use $A_n$ instead of $A_N$ with the underline brace.
  - the explanation about $k$ is not that clear
  - definition of $k$ not necessary
  - indexing does not need to be defined
  - not clear what is the "simplification" here.
  - Clarify the condition "these input tensors..." and, if necessary, use a specific line for it. 

- Do we accept negative values for "axis"?

- About R2: simply state that broadcasting is forbidden. 
  - btw, the question is not necessarily determinism because the broadcasting process is surely deterministic. What we want is a traceable and controlled processing of tensors. 

- About R3: to be clarified. shape or type? There is a specific constraint on shape (all tensors must have the same shape except on the dimension on which concatenation must be done). Thi sis a constraint, not a restriction...

- In the signature, don't use underbrace...
- The fact that we start from 0 does make the upper bound strange, may be use $[1, 2^{31}-1[$, do not rephrase is using $n$...
-  "The concat operator compute the concatenation..." =>  "The concat operator concatenates..."
-  "Each tensor concatenated..." is not necessary => suppress. 
-  Une $n$ rather than $N$ because (i) this is rather usual and (ii) it prevent confusion with the $N$ of Natural numbers.
-  Do not repeat "Let concat_result"... 
-  "the number of dimensions for the ..." => "the number **of** dimensions of the ..."?
-  Its the word "rank" appropriate? For a matrix, the "rank" refers to the number of linearly independent rows/columns... use dimension only?
-  In the "mathematical formula", the notation is really pythonic... I would prefer a more standard way...
- The mathematical description is overly complicated with respect to what the operator actually does. I think that it would be more appropriate to first describe the operator in siple terms with a diagram and, then, provide a more detailed explanation. 
- In any case, I would not write "to simplify the formula...", but, instead, would simply remove the first part, keeping only the part where this "simplification" has been used. BTW, the simplification is not that obvious since the formulation is more of less the same (becasue we have to compute the sum of all indexes in any case...)à
- rather than "i", shoundn't we use the "axis" attribute?
- I don't know if introducing "d" is necessary... $i$ or $axis* should be sufficient.
- Item tagged "E6" should be a constraint on the input tensors.
- Same for tag "E7" whihc express a constraint on the output tensor.  
- Put the "examples" in a specific section (called "examples"?)
  
### Notation
Let $a$ be the concatenation axis. \
Let $d_{ij}$ be the dimension of input tensor $X_i$ for axis $j$. 

#### Constraint
All tensors must have the same shape except for the concatenation axis, i.e, 

  $\forall i, k$ and all $j ≠ a$:
    $d_{ij} = d_{kj}$

### Shape of the output tensor ``Y``

$shape(Y) = (d_0, d_1, ..., d_{r-1})$ where:\
$d_j$ = $\sum_{i=1}^n d_{ij}$ , if $j = a$ and\
$d_j = d_{1j}$,          otherwise

### Value of  of the output tensor

Let $s_k = \sum_{j=1}^{k-1}d_{j,a}$  be the cumulative offset along axis $a$ before input $X_k$.\
Then 
$Y[i_0,...,i_{r-1}]= X_k[i_0,..., i_a-s_k,..., i_{r-1}]$ if $s_k\leq i_a \lt s_k+d_{k,a}$   


- The examples shall *** first *** illustrate the operator works. 
- Use examples in which the values can be discriminated, e.g., 31,32,33 for tensor 3... 
- Except 1 or 2, other examples shall be given at the end of the description, after the inputs, outputs, attributes... and preferably in the test notebook.

- input tensor
  - C1: "The input number of tensors..." => "The number of input tensors must be..." (note that this means that we support variadic operators)
  - C2: "the shape of input tensors shall be the same except for dimension ``axis``. And see the more mathematical statement above. 
- output
  - C1: concept of "type  to be clarified (seems to cover both "datatype" (float, int, etc.) and shape). BTW, the shape of input tensors must not be the same for all dimensions. And the shape of the output tensor shall satisfy the relation state previous (see above).
  - As stated somewhere (?), we do not repeat constraints involving several inputs, outputs or attribyutes but provide a link to them. See operator ``conv``.  

- attributs "axis" : "Attribute axis determines how the concatenation should be operated (along which axis)." => "Attribute ``axis`` determines the axis along which concatenation should done."
- the restriction on positive value of ``axis`` shall be reflected tagged and reflected at the beginning of the file.
