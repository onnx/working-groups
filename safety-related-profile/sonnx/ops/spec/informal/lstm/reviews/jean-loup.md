"Operator LSTM computes forward, reverse, or bidirectional Long Term Short Term Memory Cell." <- "Operator LSTM computes the output of an architecture including one or several Long Term Short Term Memory cells. Cells are organized in a number of layers equal to the length of the input sequences. The organization can be forward, reverse or bi-directional."

"LSTM Bidirectional layer" <- "The following figure presents the use of a LSTM cell in a bidirectional architecture presenting three layers. Note that the sum of outputs is performed outside of the architecture defined by the operator."

"LSTM Cell internal diagram" <- "LSTM Cell internal diagram for input, memory and output gates controlled by sigmoïds and flow activated by hyperbolic tangent"

"seq_length" : Number of layers in the archirecture. The same LSTM cell, with the same parameters is repeated at each layer of the architecture for each direction. I.e. when there are two directions there are only two sets of parameters. For forward architectures each layer corresponds to a time step of the simulation of the dynamic behavior of a single LSTM cell with delayed feedbacks of the state cell $c_{t-1} \gets c_t$ and the hidden layer $h_{t-1} \gets h_t$.

I don't understand the presence of "batch_size" in an inference context. Make the constraint "batch_size =  1" unconditional in SONNX restrictions?

"hidden_size" also defines tensor shapes.

I don't understand "for example (f, g, h) in LSTM" . I know that's in the ONNX documentation but "for exemple in LSTM" makes no sense because we are specifying LSTM. I think f, g, h are respectively what is called latter act1, act2 and act3. I think we should write, "act1, act2 and act3 as defined in Section Mathematical definition of LSTM_Forward".

"clip" should be in bold characters.

"input_forget" : -> 

$$
 c_t = (1 - act1(i_t)) \odot c_{t-1} + act1(i_t) \odot act2(g_t)
$$

and $W_f$, $R_f$, $B_{wf}$ and $B_{rf}$ not relevent.

It is strange that for  "direction is reverse" there is no "revert", i.e. "Y = revert( LSTM_Forward  (revert(X),...))"

If peepholes are authorized we should write:

$$
\begin{bmatrix}
     i_t \\
     o_t \\
     f_t \\
     g_t 
     \end{bmatrix}
     =
     \begin{bmatrix}
     W_{i} & R_{i} & 0     & P_{i} \\
     W_{o} & R_{o} & P_{o} & 0     \\
     W_{f} & R_{f} & 0     & P_{f}\\
     W_{g} & R_{g} & 0     & 0
     \end{bmatrix}
     \times
     \begin{bmatrix}
     x_t \\
     h_{t-1} \\
     c_t \\
     c_{t-1}
     \end{bmatrix}
     +
     \begin{bmatrix}
     B_{wi} + B_{ri} \\
     B_{wo} + B_{ro} \\
     B_{wf} + B_{rf} \\
     B_{wg} + B_{rg}
     \end{bmatrix}
$$

Indicating that $P_i$, $P_o$ and $P_f$ are diagonal matrices.
