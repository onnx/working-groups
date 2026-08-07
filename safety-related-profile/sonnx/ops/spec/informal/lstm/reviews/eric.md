- Hyper-parameters
	- Are they "parameters" or "notations". It seems to me that they are *** notations *** used to designate "attributes" of the input tensors. Can we really call them "hyper-parameters"?.
		- nu_directions is a specific case since is is actuall "computed" by the algotithm. I would not introduce it...
	
	- Suppress "defines the" : 
	> `seq_length`: number of time steps for the LSTM cell
	- foward => forward 

- Signature

- Informal specification
	- Check title level
	- "Operator LSTM computes the Long Term Short Term Memory Cell forward, backward, or bidirectional." => "Operator LSTM computes the forward, backward, or bidirectional Long Term Short Term Memory Cell."
	- Shouldn't we add (somewhere) some reference to the academic paper?
	- "is described as follows" => "is the following"?
	- Where does the "direction" "parameter" come from?
	- I don't understand the role of "num_directions". is it an input or some output?
	- shouldn't we avoid the use of "..." in the specification?
	- Formula to be reformated.
	- The activation functions "act1" and "act2" and "act3" are not defined. Should they be attributes? 
	- Are you sure about Y[t-1]=h_t? (just check)
- Inputs and outputs 
	- "is intoduced" => "is introduced"
	- "considering the actual industrial use case" : discuss how to formulate this...
	- About the tensor sizes, we should probably clarifies / explain the notation (in particular "*" stands for usual multiplication whereas "\times" introduces a new tensor dimension.
	- "sequence_lens [...) T1" => "sequence_lens [...) T" 
		- Note that as we are in the real domain, we should probably replace "T" by "real"? => to be discussed
		- "It has shape batch size" => "Th shape of tensor `sequence_lens` is (batch_size). (to be corrected everywhere)
	- "optional initial value of the hidden" => "optional initial value of the hidden state"
		- "assumed to be ..." => is it really "assumed to be xxxx"? => "if not specified the initial value of h is set to 0" => to be discussed.
		- check the font for all notations (sometime `xxx`and sometimes xxx)
- Attributes 
	- We should not see "floats".
	- activation_alpha :  not necessarily a "scaling" value. For a Leaky ReLu, for instance, it corresponds to the leakiness factor.
	- "The value is a coma separated $3 \times STRINGS$ where 'act1, act2, act3' values can be taken in {`Relu`, `Tanh`, `Sigmoid`}." 
		- => "The value is a string of 3 comma separated values 'A1,A2,A3' where the $Ai \in {`Relu`, `Tanh`, `Sigmoid`}$.
	- "Defaults to" => "if not specified..."
	- be careful : "coma" => "comma" (with two "m"s.
	- if "direction is bidirectional" 
		=> add the first case "if direction is  not bidirectional" then... 
	- "hiden_size" 
		- I don't understand the sentence "shall be set to hidden_size". If it is an attribute, then it is the value provided by the user. There is no need to add this "hyper-parameter"...
	- input_forget
		- shouldn't this attribute paly a role in the algorithm?
	- layout
		- to be discussed. Seems to refer to Python implementation...
	- Explicit inputs and attributes 
		- We ahev called them "restrictions" => SONNX restrictions, to be discussed
	
	
		