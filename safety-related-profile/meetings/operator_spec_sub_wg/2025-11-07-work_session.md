### Notations and other conventions to be added to the *guidelines*
- Change  the notation of variadic arguments from $X_i$ to $Xi$ .
- All elements are indexed from $0$ to $L$ , L being the index of the **L**ast element.
- In the spec of all operator, add an hyperlink to the ONNX operator  
- To designate a specific element of a tensor $T$, use $T[i,j,..]$, i.e., square bracket rather than parentheses.
- Comply with the ONNX naming conventions: $add$ becomes $Add$.
- Use ONNX type lists (without the "tensor()) 
- Provide a template of the informal spec that will serve as a basis for the writing of new operators (besides the *guidelines*)
- [ ] (all) Modify the already specified operators to ensure compliance with these new conventions.

### Review of the $\text{Slice}$ operator
- See replies to Ricardo and Jõao's questions in [joao-ricardo-doubts.md](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/sonnx/ops/spec/informal/slice/reviews/joao-ricardo-doubts.md)
- Those questions raised very interesting discussions about empty tensors
- [ ] (Eric) Create a side note about "empty tensors" (To be placed in "doc"). [project::[[SONNX]]] 
- Ensure that all existing operators (and pseudo-op such as $bc$) handles tensors with null  dimensions correctly. (To be added in the guidelines.)

### Review of the $\text{Clip}$ operator
- Jõao and Ricardo have questions about the handling of NaN.
	- The spec. should only refer to  $\min(M, \max(X[i],L))$  and define what $\min(x,NaN)$ and $\max(x,NaN)$ means.
	- Consider other special values (+Inf, -Inf, $0^+$ +, $0^-$ )
	- Check what the IEEE  says about min and max with these values. 
- [ ] (Mariem) Give R&J a pointer to Why3 where NaN are handled.
- [ ] (Mariem) Give R&J a feedback ont the formal spec (in particular: recall a few principles to be followed).

### Review of $\text{Max}$ and broadcasting
- See Eric's comments [here](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/sonnx/ops/spec/informal/max/reviews/max-ejn.md)
- [ ] (Jean-loup) Separate the spec broadcasting and the max operator 
	- Broadcasting is specified as $(Z1,Z2,ZL)=\text{bc}(X1,X2,...,XL)$  
	- The spec is to be placed in "common"
	- "Properties" will be useful to support the verification (formal, test) activities but they have to be removed from the informal spec.
    	- They should be specified in the most simple way so has to be traceable to some simple implementation using primitive operations (loops, simple mathematical operations). In particular, we should stick to two-step process : (i) construction of the broadcasted tensors and (ii) computation of the maxes on those tensors must be explicit.

### Other topics
- [ ] (Eric) Provide explanations about the new way to manage modifications (using Pull Requests).
- [ ] Check the display problem with LaTeX formulae in Markdown (see $\text{Add}$)
- [ ] (Eric) During next meeting ask participants if they know other issues similar to those raised by empty tensors.


