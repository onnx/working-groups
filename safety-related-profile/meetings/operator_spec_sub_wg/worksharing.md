
### List of contributors

|Initial | Actual name |
|------|-------------|
| ej | Eric |
| mt | Mariem |
| jlf| Jean-Loup |
| sb | Sebastian | 
| tb | Thiziri |
| hb | Henri |
| nv | Nicolas |
| sml| Salomé |
| js | Jean |

### Definition of statuses

|Status | Meaning|
|-------|--------|
| DR    | Draft   |
| RLR-i    | Ready for local (*) review #i  |
| RGR-i    | Ready for general (**) review #i  |
| RER-i    | Ready for external review #i  |
| FI    | Finalized |

(*) A "local" review involves a limited set of people.
(**) A "general review" involves the complete working group.
(***) An  "external" review involves people outside of the working group. 

### Status of operators 

| Operator                     | Writers            | Local reviewers         | Status (WR, RW, FI)
|------------------------------|--------------------|-------------------|-------------------
| Abs                          |hb,                 |                   | DR
| Add                          |hb                  | sml               | DR
| Cast                         |                    |                   |
| Clip                         |                    |                   |
| Concat                       |sml                 |                   | RGR-1
| Constant                     |hb,                 |                   | DR
| ConstantOfShape              |                    |                   |
| Conv                         |ej,mt               |jlf,sb,tb,hb       | RGR-1
| ConvTranspose                |                    |                   |
| Dense                        |                    |                   |
| Div                          |hb,                 |                   | DR
| Equal                        |                    |                   |
| Erf                          |                    |                   |
| Exp                          |                    |                   |
| Expand                       |                    |                   |
| Flatten                      |                    |                   |
| FullyConnected               |                    |                   |
| Gather                       |                    |                   |
| Gemm                         |nv                  |                   | DR
| GlobalAveragePool            |                    |                   |
| GRU                          |                    |                   |
| HardSwish                    |                    |                   |
| Identity                     |                    |                   |
| LeakyRelu                    |                    |                   |
| Less                         |hb,                 |                   | DR
| Log                          |hb,                 |                   | DR
| LSTM                         |nv                  |                   | DR
| MatMul                       |nv                  |                   | DR
| Max                          |                    |                   |
| MaxPool                      |sml, js             |                   |
| Min                          |                    |                   |
| Mod                          |                    |                   |
| Mul                          |hb,                 |                   | DR
| Neg                          |hb,                 |                   | DR
| Not                          |                    |                   |
| Pad                          |                    |                   |
| Pow                          |hb,                 |                   | DR
| Range                        |                    |                   |
| ReduceMean                   |                    |                   |
| ReduceSum                    |                    |                   |
| Relu                         |sml, js             |                   |
| Reshape                      |                    |                   |
| Resize                       |sml                 |                   |
| ScatterND                    |                    |                   |
| Shape                        |                    |                   |
| Sigmoid                      |                    |                   | DR
| Slice                        |                    |                   |
| Softmax                      |                    |                   |
| SoftPlus                     |                    |                   |
| Split                        |                    |                   |
| Sqrt                         |hb,                 |                   | WR
| Squeeze                      |                    |                   |
| Sub                          |hb,                 |                   | WR
| Tanh                         |                    |                   | WR
| Transpose                    |                    |                   |
| ConvTransposeDeconvolution   |                    |                   |
| Unsqueeze                    |                    |                   |
| Where                        |hb,                 |                   | WR


