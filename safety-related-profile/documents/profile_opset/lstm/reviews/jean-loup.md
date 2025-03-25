"Operator LSTM computes forward, reverse, or bidirectional Long Term Short Term Memory Cell." <- "Operator LSTM computes the output of an architecture including one or several Long Term Short Term Memory cells. Cells are organized in a number of layers equal to the length of the input sequences. The organization can be forward, reverse or bi-directional."

"LSTM Bidirectional layer" <- "The following figure presents the use of a LSTM cell in a bidirectional architecture presenting three layers. Note that the sum of outputs is performed outside of the architecture defined by the operator."

"LSTM Cell internal diagram" <- "LSTM Cell internal diagram for input, memory and output gates controlled by sigmoïds and flow activated by hyperbolic tangent"

I don't understand the presence of "batch_size" in an inference context. Add a constraint "batch_size =  1"?


