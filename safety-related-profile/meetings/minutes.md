# 2025/08/26
## Participants
  *To be completed*
## Agenda
  - Actions [eric]
  - Status of [guidelines](../documents/profile_opset/guidelines.md) and application to [`conv`](../documents/profile_opset/conv/conv.md) and [`concat`](../documents/profile_opset/concat/concat.md)
  - Error / failure conditions; Eduardo's remarks on [discussion elements](../meetings/errror%20conditions/2025-07-30%20-%20Discussions.md) with Eduardo's comments. 
  - Code generation
  - Link with the DeepGreen project (see [slide](./slides/AIDGE.pptx))
  - Events (Mobilit'AI)
  - Presentation Alexandre Eichenberger on ONNX-MLIR on 08/10/2025
## Minutes
- Continuation of the discussion about [Failure modes / error conditions](../meetings/errror%20conditions/2025-07-30%20-%20Discussions.md) with Eduardo's comments.  on the basis of Edoardo's comments:
  - It seems that we converge on a baseline where we would simply indicate whether or not the operator may fail (due to a division by zero, wrap-around, etc.) and, if possible, in which conditions such situation may occur. 
    - If the conditions can be expressed on the inputs, this means that we could possibly add the condition in the specification (a conditions on the input domain)
    - If the condition cannot be expressed on (or "propagated to") the inputs, we express the condition at the appropriate level (for instance:
      > "When computing a matrix multiplication, the result of the accumulation may overflow and the result may "wraparound", leading to an incorrect result."
    - We may give a link to the location in the formula where this accumulation is done. 
    - Note that some smart implementation may avoid the problem. For instance, when accumulating 2 bits values on a 2 bits accumulator, "3+3-3-3" overflows while "3-3+3-3" does not.
    - So, the relevance of the warning (i.e., "When computing [...]") actually depends on the implementation, but we know that -- in principle -- there might be some cases where an overflow can occur. And this is due to the the very fact that the operation accumulates values. 
  - If no indication is given about occurrence of a "failure", this means that the specification is complete and defines what is the expected value for any input. 
  - In addition, we will also provide "recommendations" about the implementation. A typical example is the one of `SoftMax` where we could recommend the use of the `-max(Xi)` trick.  
- Concerning code generation from the Why3 spec.: Loïc has provided us with an example. We are currently analyzing it and will try to apply it on `conv` and `concat`.
## Actions
### New actions
- [X] (2708-1, Eric) Give short guidelines about error / failure conditions.
  - See minutes of 2025/08/27 meeting.
- [ ] (2708-2, Mariem) Put Loïc's contribution in the repo.
- [ ] (2708-3, Mariem, Salomé) Try to apply Loïc's approach to `conv` and `concat`
### Past actions
- [ ] (3007-1, Eric, All) Collect ideas exchanged on Error Conditions during the meeting. To be discussed during next meeting. 
  - Document is [here](../meetings/errror%20conditions/2025-07-30%20-%20Discussions.md) with Eduardo's comments. 
- [ ] (1607-1, Jean-Baptiste, Sergei (?)) Produce a synthesis of SONNX <=> ED 324 traceability 
- [ ] (1607-2, Eric, Jean) Check what is the actual need in terms of broadcasting (ask users, checks models, check operators providing this capability). What would be the effort to integrate broadcasting in the specification of our operators?
  - Introduce a specific "broadcast" operator to make the operation explicit in the spec. See 1607-3.
- [ ] (1806-3, Eric, Dumitru) Organize a presentation of Dumitru's approach to handle RNNs. (please complete [this document](./presentation_proposals.md))
- [ ] (1806-4, Eric) Organize a "physical" working session on the graph specification 
- [ ] (1806-5, Eric, Jean) Resend a "call for participation" to the mailing list (at least once we have a good template spec) 
- [ ] (0406-1, Franck) Specify numerical accuracy for the `conv` operator.
  - First trial on something simpler than the conv (matrix multiplication).
  - Done on the [matmul](../documents/profile_opset/matmul/matmul.md)
  - A prototype tool is currently being developed. Possibly available in October (this is **not** a commitment).   
- [-] (0904-5, Dumitru) Scrutinize the set of ONNX ops to see if there are other operator causing similar concerns as ``loop``.
  - Cancelled
### Long term actions
- [ ] (2003-3, Eric) Initiate discussion in WG about ONNX integration and propose possible solutions to ONNX (from [2023/03/19 meeting](./Other_meetings/2025-03-20-An-Er-Se-Je.md))
- [ ] (1205-6, Eric, Jean) See how to proceed with tool implementation
- [ ] (0412-6, Eric) Create a sub working group to analyze the existing standard in a systematic way...
  - Contribution of Anne-Sophie. But WG to be set. 
  - Take into account the new modality to manage and report issues to ONNX (from [2023/03/19 meeting](./Other_meetings/2025-03-20-An-Er-Se-Je.md))
  - [ ] Create a review form to support the analysis
  



# 2025/07/16
## Participants
  *To be completed*
## Agenda
  - Actions [eric]
  - A few words about the idea of a core set of operators
    - See note [here](./core_ops/core_ops.md) [eric]
  - Guidelines 
    - See [here](../documents/profile_opset/guidelines.md).
  - Status of MLIR presentation by Alexandre. (2025/10/08) [eric]
  - Status of work on formal spec [Mariem and Salomé]
    - Presentation of work on the formalization of Scalar and the first results about C code generation. 
  - Ideas on error condition spec [Franck]
  - Status of discussions about tests (Andreas, Justin, Christian, Eric, Jean) [eric+jean]
    - See [minutes](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/meetings/testing/2025-07-29-tests.md)
## Minutes
  - See above.
  - See Franck slides [here](./errror%20conditions/2025-07-30-SONNX_error.pdf)
  - See elements discussed about the errors conditions [here](./errror%20conditions/2025-07-30%20-%20Discussions.md)
## Actions
### New actions
- [ ] (3007-1, Eric, All) Collect ideas exchanged on Error Conditions during the meeting. To be discussed during next meeting. 
### Past actions
- [ ] (1607-1, Jean-Baptiste, Sergei (?)) Produce a synthesis of SONNX <=> ED 324 traceability 
- [ ] (1607-2, Eric, Jean) Check what is the actual need in terms of broadcasting (ask users, checks models, check operators providing this capability). What would be the effort to integrate broadcasting in the specification of our operators?
  - Introduce a specific "broadcast" operator to make the operation explicit in the spec. See 1607-3.
- [X] (1607-3, Dumitru) Write a few lines to explain the "mixed approach" to handle broadcasting.
  - Mail exchange collected in [here](./broadcasting/dumitru-2025-07-21.md) 
- [X] (1607-4, Franck) Write a few lines to explain the approach to handle errors: ask implementers to provide error conditions 
  - Description sent on 2025/07/16
- [X] (0207-1, Eric) Do a "synthesis" of the discussion about overflows, etc., discuss with the WG, find a consensus, add to the guidelines... 
    - First proposal in the [guidelines](../documents/profile_opset/guidelines.md). To be discussed (see Franck's pres.)
- [ ] (1806-3, Eric, Dumitru) Organize a presentation of Dumitru's approach to handle RNNs. (please complete [this document](./presentation_proposals.md))
- [ ] (1806-4, Eric) Organize a "physical" working session on the graph specification 
- [ ] (1806-5, Eric, Jean) Resend a "call for participation" to the mailing list (at least once we have a good template spec) 
- [ ] (0406-1, Franck) Specify numerical accuracy for the `conv` operator.
  - First trial on something simpler than the conv (matrix multiplication).
  - Done on the [matmul](../documents/profile_opset/matmul/matmul.md)
- [ ] (0904-5, Dumitru) Scrutinize the set of ONNX ops to see if there are other operator causing similar concerns as ``loop``.
### Long term actions
- [ ] (2003-3, Eric) Initiate discussion in WG about ONNX integration and propose possible solutions to ONNX (from [2023/03/19 meeting](./Other_meetings/2025-03-20-An-Er-Se-Je.md))
- [ ] (1205-6, Eric, Jean) See how to proceed with tool implementation
- [ ] (0412-6, Eric) Create a sub working group to analyze the existing standard in a systematic way...
  - Contribution of Anne-Sophie. But WG to be set. 
  - Take into account the new modality to manage and report issues to ONNX (from [2023/03/19 meeting](./Other_meetings/2025-03-20-An-Er-Se-Je.md))
  - [ ] Create a review form to support the analysis
  


# 2025/07/16
## Participants
  Salomé, Jean, Tomé, Cong, Jean-Baptiste, Franck, Eric, Dumitru, ...
## Agenda
  - Actions
  - A few words about shape inference and broadcasting
  - A few words about the "minimal corpus of operators"
  - A few words about runtime errors
  - Feedback on presentation to WG114 (see [slides](./Other_meetings/SONNX%20-%20WG114.pdf))
    - ED324 = ARP 6983
  - Feedback on meeting with DeepGreen
  - Meeting with ONNX infra about testing
  - Opportunities for presentation of our work:
    - Mobilit'AI.
  - Stragegy for next period
## Minutes
  - A few words about shape inference and broadcasting
    - Forbidding broadcasting may reveal extremely penalizing because making it "explicit" boils down to creating actual tensors whereas broadcasting is essentially a manipulation of indexes done at operation level.
    - We have to check if this restriction is necessary, sensible, and applicable.
    - See actions (1607-2) and (1607-3)
  - A few words about the "minimal corpus of operators"
    - Some operators can be described on the basis of simpler, "atomic" operators. For instance, a `softmax` can be described as the composition of `Exp` and `ReduceSum`. It may also be described as $s(z_i) = {e^{z_i} \over \sum_{j=1}^K e^{z_j}}$. A `Relu` can also be described as a combination of operators, etc.  
      - Do we want to apply this modular approach? 
      - What would be the "minimal corpus of operators"? 
      - Could we have a "non-modular" informal specification (that describes the operation using a mathematical formula) and a modular formal specification? 
  - A few words about runtime errors
    - See this [document](./errror%20conditions/error_conditions_2.md)
    - The question is to define a strategy to specify the error condition that may occur during the execution of an operator.
    - In the FP domain, we agree that no exception is considered but that we use the IEEE special values Inf, NaN to propagate the errors up to the operator's output. <off-meeting : note that this implicitly means that the implementation complies with IEEE. It shall be noticed that not all processors fully comply with IEEE (some do not support Nan, Inf) and software implementations may also behave slightly differently from IEEE /> 
    - We have to do a systematic analysis of the error conditions and indicate what are the possible error conditions (e.g., in the case of the SoftMax : overflow). The specification may still indicate that no error shall occur (i.e., no NaNs) because we know (as it is the case for SoftMax) that there is a means to avoid it (e.g., in the case of SoftMax : substract the max value). This means that all implementations will have to apply this means (or something equivalent). Otherwise, the specificaton of the operator shall indicate in the "Error conditions" section what errors can happen (e.g., an overflow) with a NaN as a result. 
    - Franck proposes an approach in which the implmeter would provide the description of error behaviour (see 1607-4)
    - For integer operations, we will provide the **exact spec** of the operations. For signed ops, the specification will show the 2's complement description of the operation, see [here](./errror%20conditions/error_conditions_2.md))
  - Feedback on presentation to WG114 (see [slides](./Other_meetings/SONNX%20-%20WG114.pdf))
    - Presentation was appreciated.
    - One slide or two on ED 324 <=> SONNX traceability must be done (see 1607-1)
  - Feedback on meeting with DeepGreen
    - SONNX will be used to specify (and partically provide code) for a C-code backend 
  - Meeting with ONNX infra about testing
    - Meeting planned on July 29th with people from the infra WG (Andreas, Justin, Christian).
  - Opportunities for presentation of our work:
    - Mobilit'AI.
      - We will probably present a poster à that occasion.
  - Stragegy for next period
    - For the informal specification 
      - Phase 1: Clean-up and ensure consistency between the guidelines and the 3 cononical examples (CONV2D, CONCAT, and aanother simple operator)
      - Phase 2: mailing to the potential contributor to ask for condibution on the basis of the guidelines and existing examples
      <off-meeting> - Phase 3: meeting to present the approach and share work </off-meeting>
    - The same approach shall be followed for the formal specification.  
  - Presentation of the `Add` operator by Salomé. 
## Actions
### New actions
- [ ] (1607-1) Jean-Baptiste, Sergei (?)) Produce a synthesis of SONNX <=> ED 324 tracaibility 
- [ ] (1607-2, Eric, Jean) Check what is the actual need in terms of broadcasting (ask users, checks models, check operators providing this capability). What would be the effort to integrate broadcasting in the specification of our operators?
- [ ] (1607-3, Dumitru) Write a few lines to explain the "mixed approach" to handle broadcasting.
- [ ] (1607-4, Franck) Write a few lines to explain the approach to handle errors: ask implementers to provide error conditions 
- [X] (1607-6, Tomé) Provide the description of the 2 interships.
  - Description sent on 2025/07/16
### Past actions
- [ ] (0207-1, Eric) Do a "synthesis" of the discussion about overflows, etc., discuss with the WG, find a consensus, add to the guidelines... 
- [ ] (1806-3, Eric, Dumitru) Organize a presentation of Dumitru's approach to handle RNNs. (please complete [this document](./presentation_proposals.md))
- [ ] (1806-4, Eric) Organize a "physical" working session on the graph specification 
- [ ] (1806-5, Eric, Jean) Resend a "call for participation" to the mailing list (at least once we have a good template spec) 
- [X] (1806-6, Eric) Initiate the specification of matrix multiplication 
- [ ] (0406-1, Franck) Specify numerical accuracy for the `conv` operator.
  - First trial on something simpler than the conv (matrix multiplication).
  - Done on the [matmul](../documents/profile_opset/matmul/matmul.md)
- [ ] (0904-5, Dumitru) Scrutinize the set of ONNX ops to see if there are other operator causing similar concerns as ``loop``.
### Long term actions
- [ ] (2003-3, Eric) Initiate discussion in WG about ONNX integration and propose possible solutions to ONNX (from [2023/03/19 meeting](./Other_meetings/2025-03-20-An-Er-Se-Je.md))
- [ ] (1205-6, Eric, Jean) See how to proceed with tool implementation
- [ ] (0412-6, Eric) Create a sub working group to analyze the existing standard in a systematic way...
  - Contribution of Anne-Sophie. But WG to be set. 
  - Take into account the new modality to manage and report issues to ONNX (from [2023/03/19 meeting](./Other_meetings/2025-03-20-An-Er-Se-Je.md))
  - [ ] Create a review form to support the analysis
  
# 2025/07/02
## Participants
-  Salomé, Alexandre, Jean, Sebastian, Cong, Mariem, Jean-Baptiste, Eric,...
## Agenda
- Status of actions
- Misc news:  
  - Feedback on June 20th workshop on formal specification and verification (Eric, Mariem, Jean)
  - Structure of repo for Why3 formal specifications (Mariem)  - A question about model readability (Eric)
  - Slides for WG114 (see [here](./Other_meetings/SONNX%20-%20WG114.pdf) (draft), Eric)
  - Issues [see [here](https://github.com/onnx/onnx/issues/3651)]
    - Back to action 0412-6...
  - Two questions
    - What shall we "say" about inner overflows, division par zeros, etc.?
    - *Do we need the model to be human-readable?*
  - For information: SIONNX (see [here](https://github.com/alibaba/sionnx))
      - Description of the algorithm (python). Example for [conv](https://github.com/alibaba/sionnx/blob/master/include/conv.algorithm)
      - Description of the signature. Example for [cov](https://github.com/alibaba/sionnx/blob/master/include/onnx_conv.td)
## Minutes
- Long discussion about overflows etc. See action (0207-1).
## Actions
### New actions
- [ ] (0207-1, Eric) Do a "synthesis" of the discussion about overflows, etc., discuss with the WG, find a consensus, add to the guidelines... 
### Past actions
- [X] (1806-1, Eric) Provide a complete (simple) spec example for 1 op that can be reproduced on the other ops...
  - See [matmul](../documents/profile_opset/matmul/matmul.md)
- [X] (1806-2, Mariem) Provide Franck with the C code of the conv2d operator.
  - Done. The code is [here](./attachments/conv2d.c).
- [ ] (1806-3, Eric, Dumitru) Organize a presentation of Dumitru's approach to handle RNNs. (please complete [this document](./presentation_proposals.md))
- [ ] (1806-4, Eric) Organize a "physical" working session on the graph specification 
- [ ] (1806-5, Eric, Jean) Resend a "call for participation" to the mailing list (at least once we have a good template spec) 
- [ ] (1806-6, Eric) Initiate the specification of matrix multiplication 
- [X] (1806-7, Jean-Baptiste) Provide Eric with ARP/SONNX analysis material 
- [ ] (0406-1, Franck) Specify numerical accuracy for the `conv` operator.
  - First trial on something simpler than the conv (matrix multiplication).
  - Done on the [matmul](../documents/profile_opset/matmul/matmul.md)
- [ ] (0904-5, Dumitru) Scrutinize the set of ONNX ops to see if there are other operator causing similar concerns as ``loop``.
### Long term actions
- [ ] (2003-3, Eric) Initiate discussion in WG about ONNX integration and propose possible solutions to ONNX (from [2023/03/19 meeting](./Other_meetings/2025-03-20-An-Er-Se-Je.md))
- [ ] (1205-6, Eric, Jean) See how to proceed with tool implementation
- [ ] (0412-6, Eric) Create a sub working group to analyze the existing standard in a systematic way...
  - Contribution of Anne-Sophie. But WG to be set. 
  - Take into account the new modality to manage and report issues to ONNX (from [2023/03/19 meeting](./Other_meetings/2025-03-20-An-Er-Se-Je.md))
  - [ ] Create a review form to support the analysis
  

# 2025/06/18
## Participants
-  Eric, Mariem, Salomé, Alex, Henri, Dumitru, Jean-Baptiste, Mohammed, Franck, Jean-Loup, Jean
## Agenda
- Status of actions.
- Misc news:  
  - Presentation to ONNX meetup (["video"](./general/2025-06-09%20-%20MEET-UP/SONNX%20-%20Meetup%202025.7z))
  - Review and update of ops...
    - The existing specifications must be updated to comply with the [specification guidelines](../documents/profile_opset/guidelines.md). A first pass has been done on [`abs`](../documents/profile_opset/abs/abs.md).
  - Request for participation to work on the graph execution
    - Jean and Jean-Loup are OK to help. Eric to organize a working session.  (See action 1806-4)
  - Eric to present SONNX to the WG114. One slide about the ARP/SONNX mapping could be useful. (see action 1806-7)
- Numerical accuracy
  - Franck is preparing some elements to be put in the guidelines.
  - Franck is also working on the analysis of the matrix multiplication. It could be wise to specify this operator in order to have a complete example including numerical accuracy analysis (see action 1806-6). 
  - He needs some C code for the conv2D. (see action 1806-2) 
  - Numerical analysis verification will be computed by executing the C++ code. The C code of the operators (generated using Why3) will be integrated as is. The tool leverage's C++ operator overloading capability. 
- The number of participants to the bi-weekly meetings is decreasing steadily... 
  - Give a "good" example of spec and invite people in the mailing list to contribute...
  - Organize new presentations (see action 1806-3) 
- Discussion about June 20th second workshop on formal methods (off-main meeting).
  - This workshop concerns those that have been involved in the first workshop (other may join, please contact me). It will take place at IRT. A link will be provided. 
  - On the basis of what has been done on conv2D, concat, and graph, clarify/complete the method, obtain guidelines to carry out proofs, obtain material to support self-training, obtain guidelines to generate C code, etc. 

## Actions
### New actions
- [ ] (1806-1, Eric) Provide a complete (simple) spec example for 1 op that can be reproduced on the other ops...
- [X] (1806-2, Mariem) Provide Franck with the C code of the conv2d operator.
  - Done. The code is [here](./attachments/conv2d.c).
- [ ] (1806-3, Eric, Dumitru) Organize a presentation of Dumitru's approach to handle RNNs. (please complete [this document](./presentation_proposals.md))
- [ ] (1806-4, Eric) Organize a "physical" working session on the graph specification 
- [ ] (1806-5, Eric, Jean) Resend a "call for participation" to the mailing list (at least once we have a good template spec) 
- [ ] (1806-6, Eric) Initiate the specification of matrix multiplication 
- [ ] (1806-7, Jean-Baptiste) Provide Eric with ARP/SONNX analysis material 

### Past actions
- [ ] (0406-1, Franck) Specify numerical accuracy for the `conv` operator.
  - First trial on something simpler than the conv (matrix multiplication).
- [ ] (0904-5, Dumitru) Scrutinize the set of ONNX ops to see if there are other operator causing similar concerns as ``loop``.
### Long term actions
- [ ] (2003-3, Eric) Initiate discussion in WG about ONNX integration and propose possible solutions to ONNX (from [2023/03/19 meeting](./Other_meetings/2025-03-20-An-Er-Se-Je.md))
- [ ] (1205-6, Eric, Jean) See how to proceed with tool implementation
- [ ] (0412-6, Eric) Create a sub working group to analyze the existing standard in a systematic way...
  - Contribution of Anne-Sophie. But WG to be set. 
  - Take into account the new modality to manage and report issues to ONNX (from [2023/03/19 meeting](./Other_meetings/2025-03-20-An-Er-Se-Je.md))
  - [ ] Create a review form
  
# 2025/06/04
## Participants
- Nicolas, Salomé, Sebastian, Henri, Jean-Loup, Jean, Eric, Jean-Baptiste, Frédéric, Eduardo,...
## Agenda
- Status of actions.
- Misc news: 
  - ONNX meetup on June 9th: a ["video"](./general/2025-06-09%20-%20MEET-UP/SONNX%20-%20Meetup%202025.7z) has been prepared.
  - The abstract of our [paper on SONNX](../documents/publications/ERTS2026/2025-06-02%20SONNX%20-%20ERTS%202026%20abstract%20-%20final.pdf) has been submitted to [ERTS 2026](https://conference-erts.org/).
  - Salomé has updated the informal and formal specification of the ``concat`` operator. Will be pushed soon.
  - Frédéric has presented his first attempt to specify errors for operators using floating point values. 
    - As a proof of concept, it has been applied to the [``abs``](https://github.com/ericjenn/working-groups/blob/spec-with-numerical-accuracy-info/safety-related-profile/documents/profile_opset/add/abs.md) and [``add``](https://github.com/ericjenn/working-groups/blob/spec-with-numerical-accuracy-info/safety-related-profile/documents/profile_opset/add/add.md) operators.
    - The specification gives the properties that an implementation shall satisfy considering the errors due to the floating point arithmetic. Methods errors are not considered. The properties are "conservative" in the sense that they consider any floating point values. Tighter bounds could be obtained for smaller domains.
    - A C++ implementation to compute the errors is provided (not fully implemented for the moment...). 
    - This implementation evaluates (will eventually evaluate) the error **symbolically**.
    - Verification of the assertion will also be done symbolically.
    - The next step would be to address the ``conv`` operator. 
## Actions
### New actions
- [ ] (0406-1, Franck) Specify numerical accuracy for the `conv` operator.
### Past actions
- [X] (2105-1, Salomé) Provide answers (OK,KO, TBdiscussed) to [Eric's comments](../documents/profile_opset/concat/reviews/eric.md) for the `concat` operator. 
- [X] (0904-2, Jean-Baptiste) Complete the analysis of the ARP+Concept papers to collect potential reqs for SONNX 
- [ ] (0904-5, Dumitru) Scrutinize the set of ONNX ops to see if there are other operator causing similar concerns as ``loop``.
- [ ] (2003-3, Eric) Initiate discussion in WG about ONNX integration and propose possible solutions to ONNX (from [2023/03/19 meeting](./Other_meetings/2025-03-20-An-Er-Se-Je.md))
- [X] (1203-5, Eric, Jean and Andreas) Organize a meeting with ONNX to present our first results (in order for them to have an idea of the expected end-result) and discuss what could be the integration modalities.
  - Will be done during next ONNX team up
- [ ] (1205-6, Eric, Jean) See how to proceed with tool implementation
- [ ] (0412-6, Eric) Create a sub working group to analyze the existing standard in a systematic way...
  - Contribution of Anne-Sophie. But WG to be set. 
  - Take into account the new modality to manage and report issues to ONNX (from [2023/03/19 meeting](./Other_meetings/2025-03-20-An-Er-Se-Je.md))
  - [ ] Create a review form

# 2025/05/21
## Participants
- At least: Salomé, Sabastian, Dumitru, Sergei, Jean, Eric, Mariem, Mohammed, Nicolas, ...
## Agenda
- Status of actions.
- Misc news: 
  - next workshop on formal specification + proof...
  - discussion with WG114 and presentation to WG114 
- Presentation of the `concat` operator by Salomé
- Brief presentation of the informal and formal specification of a `graph` by Eric
  - Review of the `graph` informal specification by Mohammed.
- Overview of the [Specification guidelines](../documents/profile_opset/guidelines.md)
- Status of operator specification
## Actions
### New actions
- [ ] (2105-1, Salomé) Provide answers (OK,KO, TBdiscussed) to [Eric's comments](../documents/profile_opset/concat/reviews/eric.md) for the `concat` operator. 
- [X] (2105-2, Mohammed) Upload graph review form 
### Past actions
- [X] (2304-1, Eric+Jean) Plan presentation of SONNX to Christophe R.
  - Done on May 13th.
- [X] (2304-2, Mohamed) Review of the informal spec of the [graph semantics](../documents/profile_graph/graph.md). *Please place the review in the "review" directory.*
  - Done and to be presented during the meeting.
- [X] (0904-1, Sebastian, Edoardo) Review the [graph spec](../documents/profile_graph/graph.md)
  - [Review by Edoardo](../documents/profile_graph/reviews/edoardo.md)
- [ ] (0904-2, Jean-Baptiste) Complete the analysis of the ARP+Concept papers to collect potential reqs for SONNX 
- [X] (0904-3, Salomé) Specification (informal and formal) of the ``concat`` operator.
  - Work in progress. Fist review by Eric. 
  - Done, to be presented during the meeting
- [X] (0904-4, Joao) Investigate internship to support SONNX
- [ ] (0904-5, Dumitru) Scrutinize the set of ONNX ops to see if there are other operator causing similar concerns as ``loop``.
- [X] (2603-3, all) Think about our expectation concerning numerical precision (add req)
  - See minutes of [meeting with Franck ](../meetings/numerical%20accuracy/2025-04-11_Meeting_with_Franck.md)
- [C] (2003-1, Andreas) Create a "sonnx" label and a group with the appropriate rights to tag issues. (from [2023/03/19 meeting](./Other_meetings/2025-03-20-An-Er-Se-Je.md))
  - [X] Tag created. 
  - [C] Determine who can apply this tag? 
  - Cancelled. 
- [ ] (2003-3, Eric) Initiate discussion in WG about ONNX integration and propose possible solutions to ONNX (from [2023/03/19 meeting](./Other_meetings/2025-03-20-An-Er-Se-Je.md))
- [ ] (1203-5, Eric, Jean and Andreas) Organize a meeting with ONNX to present our first results (in order for them to have an idea of the expected end-result) and discuss what could be the integration modalities.
  - Will be done during next ONNX team up
- [ ] (1205-6, Eric, Jean) See how to proceed with tool implementation
- [ ] (0412-6, Eric) Create a sub working group to analyze the existing standard in a systematic way...
  - Contribution of Anne-Sophie. But WG to be set. 
  - Take into account the new modality to manage and report issues to ONNX (from [2023/03/19 meeting](./Other_meetings/2025-03-20-An-Er-Se-Je.md))
  - [ ] Create a review form

# 2025/05/07
## Participants
TBC
## Agenda
- Presentation Alex: "[About quantization and ONNX in Airbus' context"](./slides/2025-05-07-Alex-DIGONNET-SONNX%20quantization%20representation%20formats.pdf)"
- Certification referential (RMT) by Jean-Baptiste 
- Presentation of SONNX to ALTERA and ANSYS
## Actions
### New actions
No new action.
### Past actions
- [ ] (2304-1, Eric+Jean) Plan presentation of SONNX to Christophe R.
- [ ] (2304-2, Mohamed) Review of the informal spec of the [graph semantics](../documents/profile_graph/graph.md). *Please place the review in the "review" directory.*
- [ ] (0904-1, Sebastian, Edoardo) Review the [graph spec](../documents/profile_graph/graph.md)
  - [Review by Edoardo](../documents/profile_graph/reviews/edoardo.md)
- [ ] (0904-2, Jean-Baptiste) Complete the analysis of the ARP+Concept papers to collect potential reqs for SONNX (to be done for next meeting) 
- [ ] (0904-3, Salomé) Specification (informal and formal) of the ``concat`` operator.
  - Work in progress. Fist review by Eric. 
- [X] (0904-4, Joao) Investigate internship to support SONNX
- [ ] (0904-5, Dumitru) Scrutinize the set of ONNX ops to see if there are other operator causing similar concerns as ``loop``.
- [ ] (2603-3, all) Think about our expectation concerning numerical precision (add req)
  - See minutes of meeting with Franck: 
- [ ] (2003-1, Andreas) Create a "sonnx" label and a group with the appropriate rights to tag issues. (from [2023/03/19 meeting](./Other_meetings/2025-03-20-An-Er-Se-Je.md))
  - [X] Tag created. 
  - [ ] Determine who can apply this tag?
- [ ] (2003-3, Eric) Initiate discussion in WG about ONNX integration and propose possible solutions to ONNX (from [2023/03/19 meeting](./Other_meetings/2025-03-20-An-Er-Se-Je.md))
- [ ] (1203-5, Eric, Jean and Andreas) Organize a meeting with ONNX to present our first results (in order for them to have an idea of the expected end-result) and discuss what could be the integration modalities.
  - Will be done during next ONNX team up
- [ ] (1205-6, Eric, Jean) See how to proceed with tool implementation
- [X] (1202-3, All) Review new operators processed by Henri 
  - Reminder : place your comment in a dedicated file `<name>.md` in the "review" directory of the relevant operator
  - [X] Eric: review and modification of operator [`Div`](../documents/profile_opset/div/div.md)
- [C] (1501-1, Sebastian) Specify some operators...
  - Sebastian is working on `reshape`and other ops... 
  - Cancelled
- [C] (1501-2, Eric & Jean) Find a way to involve more people in the specification work...
  - Cancelled
- [C] (1812-6, All) Check legal aspects of contributing to the SONNX effort ("clearance")
  - Cancelled
- [] (0412-6, Eric) Create a sub working group to analyze the existing standard in a systematic way...
  - Contribution of Anne-Sophie. But WG to be set. 
  - Take into account the new modality to manage and report issues to ONNX (from [2023/03/19 meeting](./Other_meetings/2025-03-20-An-Er-Se-Je.md))
  - [ ] Create a review form

# 2025/04/23
## Participants
TBC
## Agenda
- Feedback on meeting with Franck (CEA) about error estimation.
- ERTS 2026 paper (see [here](https://share-is.pf.irt-saintexupery.com/s/ipMLHmEZ8adgBDY), read access)
## Minutes
- Review of actions
- Feedback on meeting with Franck.
- Welcome to Christophe Ratajczak from [EM Microelectronics](https://www.emmicroelectronic.com/welcome)
- Salomé has made some significant progress on the informal and formal specification of the [``concat``](https://onnx.ai/onnx/operators/onnx__Concat.html) operator. Work to be pushed to the repo by the end of the week. Presentation to be done in a future meeting. 
## Actions
### New actions
- [ ] (2304-1, Eric+Jean) Plan presentation of SONNX to Christophe R.
- [ ] (2304-2, Mohamed) Review of the informal spec of the [graph semantics](../documents/profile_graph/graph.md). *Please place the review in the "review" directory.*
### Past actions
- [ ] (0904-1, Sebastian, Edoardo) Review the [graph spec](../documents/profile_graph/graph.md)
- [ ] (0904-2, Jean-Baptiste) Complete the analysis of the ARP+Concept papers to collect potential reqs for SONNX (to be done for next meeting) 
- [ ] (0904-3, Salomé) Specification (informal and formal) of the ``concat`` operator.
- [ ] (0904-4, Joao) Investigate internship to support SONNX
- [ ] (0904-5, Dumitru) Scrutinize the set of ONNX ops to see if there are other operator causing similar concerns as ``loop``.
- [X] (0904-6, Eric) Clarify the concept and req of [numerical stability](https://en.wikipedia.org/wiki/Numerical_stability) in our context.
  > Numerical stability in numerical analysis refers to how errors are propagated by an algorithm during computation. These errors can come from several sources, like round-off errors due to finite precision (e.g., floating-point arithmetic), truncation errors from approximating infinite processes (like Taylor series), input errors (e.g., measurement uncertainty). A numerically stable algorithm is one in which small changes in input or small intermediate errors do not grow significantly and affect the final output too much. In contrast, an unstable algorithm may amplify these small errors, leading to wildly incorrect results. See [this page](./numerical%20accuracy/numerical_stability.md).\
  **=> The algorithm given in the profile specifies the result. It does not specify how to *compute* the result. So the algorithm may be naïve and unstable. Thi sis true for the specification in $\mathbb{R}$.\
  => What about specifications in other domains (floats,integers)?**  
- [ ] (2603-3, all) Think about our expectations concerning numerical precision (add req)
  - See minutes of meeting with Franck: 
- [ ] (2003-1, Andreas) Create a "sonnx" label and a group with the appropriate rights to tag issues. (from [2023/03/19 meeting](./Other_meetings/2025-03-20-An-Er-Se-Je.md))
  - [X] Tag created. 
  - [ ] Determine who can apply this tag?
- [ ] (2003-3, Eric) Initiate discussion in WG about ONNX integration and propose possible solutions to ONNX (from [2023/03/19 meeting](./Other_meetings/2025-03-20-An-Er-Se-Je.md))
- [ ] (1203-5, Eric, Jean and Andreas) Organize a meeting with ONNX to present our first results (in order for them to have an idea of the expected end-result) and discuss what could be the integration modalities.
- [ ] (1205-6, Eric, Jean) See how to proceed with tool implementation
- [ ] (1202-3, All) Review new operators processed by Henri 
  - Reminder : place your comment in a dedicated file `<name>.md` in the "review" directory of the relevant operator
  - [X] Eric: review and modification of operator [`Div`](../documents/profile_opset/div/div.md)
- [ ] (1501-1, Sebastian) Specify some operators...
  - Sebastian is working on `reshape`and other ops... 
- [ ] (1501-2, Eric & Jean) Find a way to involve more people in the specification work...
- [ ] (1812-6, All) Check legal aspects of contributing to the SONNX effort ("clearance")
- [ ] (0412-6, Eric) Create a sub working group to analyze the existing standard in a systematic way...
  - Contribution of Anne-Sophie. But WG to be set. 
  - Take into account the new modality to manage and report issues to ONNX (from [2023/03/19 meeting](./Other_meetings/2025-03-20-An-Er-Se-Je.md))
    - [ ] Create a review form
# 2025/04/09
## Participants
- Eric, Jean, Salomé, Sergei, Dumitru, Cong, Andreas, Sebastian, Mohammed, Jean-Baptiste, Joao, Edoardo, Henri, Jean-Loup, Alexandre 
## Agenda
- Presentation of ONNX MLIR by Alexandre Eichenberger 
- Discussion about the "hierarchical/modular" way to specify operator, use of `onnxscript` (with Nicolas and Dumitru)
- Status of reviews
  - LSTM
  - Graph
  - Requirements
- Feedback on discussions with WG 114 and what to do next.
## Minutes
- Newcomers.
- Alexandre was not able to do the presentation today. To be (re-)rescheduled...
- Very long discussion on the specification of operators... 
  - Our objective is (i) to keep the informal specification as simple and readable as possible and (ii) to avoid multiplying formalisms.
  - To make a long story short, and since we have already decided to use Why3 as our formal language... we have concluded that 
    - the informal specification will continue using a simple, informal, possibly mathematical representation (see e.g., [``lstm``](../documents/profile_opset/lstm/lstm.md)), 
    - other representations may be provided as "examples"
    - the formal specification (in Why3) must adopt some "modular" hierarchical approach where, when applicable, an operator shall be specified using some "primitive" operators (e.g., ``lstm`` is specified using ``scan``).   
  - Review of the informal [graph spec](../documents/profile_graph/graph.md): done by Jean-Loup (thanks!). To be completed to cover e.g., ``loop`` operator. To be reviewed again by Edoardo and Sebastian (action 0904-1)
  - [Requirements](../deliverables/reqs/reqs.md): reviewed by Edorardo (thanks). Comments have been taken into account and discussed with Edoardo.
    - Discussions about requirements about 
      - "determinism of resource usage and execution times" 
        - Remove the req about memory 
        - Concerning execution times, there is at least the ``loop`` operator that can (possibly) raise some problem: we have to ensure that the number of iterations is bounded. Dumitru will checks if there are other operators whose execution time or resource may not be bounded statically. (See action 0904-5)
      - "traceability to training model and environment"
        - To be removed because (i) it'll be too complicated if we were to specify the exact training environment, (ii) traceability can be ensured by conf mngt, etc. We simply have to give the capability to embed meta-data in the model (there is already a req about that).
      - "numerical stability"
        - We were not able to remember where this req comes from. The concept of [numerical stability](https://en.wikipedia.org/wiki/Numerical_stability) was discussed and various definitions/interpretations were given, none of them being really convincing. The main questions are: (i) what do we actually require? and (ii) why do we require it? (See action 0904-6 )
- Feedback to WG 114
  - The main point concerned the concepts "exact" and "approximate" replications. After many discussions, we agreed to remove these concepts from the core of the document and put it in an Annex. Those concepts where not at the "same level": "exact" replication expresses a relation between output or intermediate tensor values while "approximate" replication expresses a relation between performances. FurthermoreIn addition, the practical usage of these concepts was not that clear, especially for the "approximate replication" that basically state that the implemented model must comply with its spec...
  - We have to complete the analysis of the ARP+concept paper in order to ensure that we are not missing reqs. See action 0904-2.
- Shouldn't we do the same type of analysis for other domains (e.g., ISO 8800 in the automotive domain)... 
- Formal specification
  - We shall start from [Loïc's proposal](../meetings/formal_methods/code/) in which he specifies the ``where`` operator. Salomé will do the specification work on ``concat`` (action 0904-3). This will need some additional work due to the use of lists of tensors as inputs.
- Other contributions
  - Joao is investigating starting an internship to support SONNX activities by the end of Q2. 
## Actions
### New actions
- [ ] (0904-1, Sebastian, Edoardo) Review the [graph spec](../documents/profile_graph/graph.md)
- [ ] (0904-2, Jean-Baptiste) Complete the analysis of the ARP+Concept papers to collect potential reqs for SONNX (to be done for next meeting) 
- [ ] (0904-3, Salomé) Specification (informal and formal) of the ``concat`` operator.
- [ ] (0904-4, Joao) Investigate intership to support SONNX
- [ ] (0904-5, Dumitru) Scrutinize the set of ONNX ops to see if there are other operator causing similar concerns as ``loop``.
- [ ] (0904-6, Eric) Clarify the concept and req of [numerical stability](https://en.wikipedia.org/wiki/Numerical_stability) in our context.
  - > > (From Wikipedia: The usual definition of numerical stability uses a more general concept, called mixed stability, which combines the forward error and the backward error. An algorithm is stable in this sense if it solves a nearby problem approximately, i.e., if there exists a Δx such that both Δx is small and f (x + Δx) − y* is small. Hence, a backward stable algorithm is always stable.
### Past actions
- [X] (2603-1, Eric, Nicolas,Jean-Loup) Analysis of all remarks about operator [lstm](../documents/profile_opset/lstm/lstm.md)
- [X] (2603-2, Eric, Edoardo) Review of the [requirements](../deliverables/reqs/reqs.md) in order to produce a clean version (possibly incomplete).
  - Done on 2025/04/08
- [ ] (2603-3, all) Think about our expectation concerning numerical precision (add req)
- [ ] (2003-1, Andreas) Create a "sonnx" label and a group with the appropriate rights to tag issues. (from [2023/03/19 meeting](./Other_meetings/2025-03-20-An-Er-Se-Je.md))
  - [X] Tag created. 
  - [ ] Determine who can apply this tag?
- [ ] (2003-3, Eric) Initiate discussion in WG about ONNX integration and propose possible solutions to ONNX (from [2023/03/19 meeting](./Other_meetings/2025-03-20-An-Er-Se-Je.md))
- [X] (1203-2, Dumitru) Propose an draft spec of LSTM where the operator would be specified using SCAN.
  - First version presented during the 26/03 meeting.
  - To be completed for next meeting (Dumitru and Nicolas)
  - Discussed during the 2025/04/09 meeting.
- [X] (1203-4, Nicolas) The relation between the directions and the dimension of the tensors shall be expressed by a constraint, not the assignment of a variable. The attributes must be presented before the description of the operator. Check that any activation function can be used for atc1 to act3. For the backward LSTM, check if the output needs to be reverted. Create a jupyter note (in collab) to illustrate the use of the operator (in the same way as for the DIV operator).
- [ ] (1203-5, Eric, Jean and Andreas) Organize a meeting with ONNX to present our first results (in order for them to have an idea of the expected end-result) and discuss what could be the integration modalities.
- [ ] (1205-6, Eric, Jean) See how to proceed with tool implementation
- [ ] (1202-3, All) Review new operators processed by Henri 
  - Reminder : place your comment in a dedicated file `<name>.md` in the "review" directory of the relevant operator
  - [X] Eric: review and modification of operator [`Div`](../documents/profile_opset/div/div.md)
- [ ] (1501-1, Sebastian) Specify some operators...
  - Sebastian is working on `reshape`and other ops... 
- [ ] (1501-2, Eric & Jean) Find a way to involve more people in the specification work...
- [X] (1501-5, Anne-Sophie) Move issues to the "graph" part when they concern the graph (and not a specific operator)
  - Cancelled.
- [ ] (1812-6, All) Check legal aspects of contributing to the SONNX effort ("clearance")
- [ ] (0412-6, Eric) Create a sub working group to analyze the existing standard in a systematic way...
  - Contribution of Anne-Sophie. But WG to be set. 
  - Take into account the new modality to manage and report issues to ONNX (from [2023/03/19 meeting](./Other_meetings/2025-03-20-An-Er-Se-Je.md))
    - [ ] Create a review form
# 2025/03/26
## Participants
- E. Jenn, J. Souyris, H. Belfy, M. Turki, J.L. Farges, E. Manino, D. Potop Butucaru, M. Belcaid, N. Valot et Duy Khoi Vo.
## Agenda
  - Operators
    - [Current list](../documents/profile_opset/):  abs, add, constant, conv, div, gemm, less, log, lstm, matmul, mul, net, pow, sigmoid, sqrt, sub, tanh, where
      - We have to have at least 1 reference example (considered consensually "perfect"). 
      - Then we have to write / review the other operators against it. Which operator?
    - [LSTM operator](../documents/profile_opset/lstm/lstm.md). [Review by Jean-Loup](../documents/profile_opset/lstm/reviews/jean-loup.md)
  - [Graph semantics](../documents/profile_graph/graph.md)
  - Feedback on [2025/03/18 workshop on formal specification and verification](./formal_methods/minutes.md)
  - Review and finalization of the [specification](../deliverables/reqs/reqs.md). Who want's to join?
  - Status on ARP
    - Discussion on March 14th : 
    > 1. The exact replication is the only option to preserve the properties demonstrated during the design phase. It means the “bit accurate” replication of the semantics of the designed model (expressed by the MLMD) in the target environment.
    > 2. The approximative replication means that the properties (performance, generalization, stability and robustness) of the designed model (expressed by the MLMD) are re-assessed in the target environment and that the results are within an acceptable epsilon from the results obtained in the design environment. The epsilon should be specified by the applicant in the MLC requirements.
  - Review of ONNX IR. Who?
  - Work on formal spec. 
  - Traceability to certification constraints
    - *What do we do next?*
  - Mail to the troop? [here](../documents/Attic/call.md)
  
## Minutes
  - Discussion about the need to have a few set of "informal specifications" to be used as references for the writing and the review of the operators. 
    - As of today, none of the operators are completely satisfying. "conv", "where" and "lstm" are good candidate for they cover different aspects, issues. We may add "div" for it handles INF and NaNs and possible "sigmoid" since it raises problems wrt overflow / underflow (see below)
  - Presentation of the latest version of the [LSTM operator](../documents/profile_opset/lstm/lstm.md) by Nicolas and discussion of [Jean-Loup's review](../documents/profile_opset/lstm/reviews/jean-loup.md). 
    - Several comments fro Jean-Loup were discussed. A specific meeting with Nicolas, Jean-Loup and Eric has to be organized to complete the review process. 
    - Dumitru proposes to build the informal specification of "lstm" on more primitive operators (e.g., "scan"). A first version was presented that defines "lstm" in a hierarchical way using more primitive operators. This first version will be completed by Dumitru (see action (1203-2, Dumitru)) and we will take a decision about the most appropriate way afterwards. 
  - Presentation of the [sigmoid operator](../documents/profile_opset/sigmoid/sigmoid.md) by Nicolas.
    - For the float version of the operator, the specification proposes an "algorithm" that discriminates two cases: $X \gt 0$ and $X \leq 0$. This discrimination is aimed at providing the best output (prevent over/under flow) for the largest input domain. 
    - In some sense, it could be considered as a "guideline", a "recommendations". We need at least to give the very reason for discriminating the two cases (some hints are given in the spec).
    - Note that this design may also be justified with respect to the symmetry of the function.
    - Another possibility could be to define the `sigmoid` using `tanh` that is a standard IEEE 754 operator ($\sigma(x)=​{1+tanh(2x​)\over 2}$). 
    - This discussion raises, again, our problem with the specification of numerical properties... (For the record, see [this document](../meetings/numerical%20accuracy/01_what_is_the_issue.pdf) presented in a previous meeting)
## Actions
### New actions
- [ ] (2603-1, Eric, Nicolas,Jean-Loup) Analysis of all remarks about operator [lstm](../documents/profile_opset/lstm/lstm.md)
- [ ] (2603-2, Eric, Edoardo) Review of the [requirements](../deliverables/reqs/reqs.md) in order to produce a clean version (possibly incomplete).
- [ ] (2603-3, all) Think about our expectation concerning numerical precision (add req)
### Past actions
- [ ] (2003-1, Andreas) Create a "sonnx" label and a group with the appropriate rights to tag issues. (from [2023/03/19 meeting](./Other_meetings/2025-03-20-An-Er-Se-Je.md))
  - [X] Tag created. 
  - [ ] Determine who can apply this tag?
- [X] (2003-2, Eric) Update SONNX landing page to point to interesting material... (from [2023/03/19 meeting](./Other_meetings/2025-03-20-An-Er-Se-Je.md))
  - Added a "contents" section in the [SONNX main page](../README.md). (Not yet pulled to the main branch)
- [ ] (2003-3, Eric) Initiate discussion in WG about ONNX integration and propose possible solutions to ONNX (from [2023/03/19 meeting](./Other_meetings/2025-03-20-An-Er-Se-Je.md))
- [X] (2003-4, Eric) Give an example of the two categories of restrictions (from [2023/03/19 meeting](./Other_meetings/2025-03-20-An-Er-Se-Je.md))
  - See proposal for the [`conv` operator](../documents/profile_opset/conv/conv.md)
- [X] (1203-1, Eric) Propose a first specification of the graph execution semantics on the basis of Dumitru's slide and ONNX doc.
  - See [here](../documents/profile_graph/graph.md)
- [ ] (1203-2, Dumitru) Propose an draft spec of LSTM where the operator would be specified using SCAN.
  - First version presented during the 26/03 meeting.
  - To be completed for next meeting (Dumitru and Nicolas)
- [X] (1203-3, Jean-loup) Do a review of the LSTM operator
  - Review is [here](../documents/profile_opset/lstm/reviews/jean-loup.md)
- [ ] (1203-4, Nicolas) The relation between the directions and the dimension of the tensors shall be expressed by a constraint, not the assignment of a variable. The attributes must be presented before the description of the operator. Check that any activation function can be used for atc1 to act3. For the backward LSTM, check if the output needs to be reverted. Create a jupyter note (in collab) to illustrate the use of the operator (in the same way as for the DIV operator).
- [ ] (1203-5, Eric, Jean and Andreas) Organize a meeting with ONNX to present our first results (in order for them to have an idea of the expected end-result) and discuss what could be the integration modalities.
- [ ] (1205-6, Eric, Jean) See how to proceed with tool implementation
- [X] (1202-2, Eric) Discussion to be initiated with ONNX about the integration of our work...
  - Moved to action (2003-3)
- [ ] (1202-3, All) Review new operators processed by Henri 
  - Reminder : place your comment in a dedicated file `<name>.md` in the "review" directory of the relevant operator
  - [X] Eric: review and modification of operator [`Div`](../documents/profile_opset/div/div.md)
- [X] (1202-5, All) Define appropriate rules to handle multiples types without multiplying the specifications. 
  - See example of operator [`Div`](../documents/profile_opset/div/div.md))
- [cancelled)] (2901-4, Dumitru) Contact Nicolas to lend a hand on LSTM. 
- [X] (2901-5, Dumitru) Prepare a short presentation  on the graph's semantics. Planned for March 12th.
- [X] (2901-8, Henri) Consider Eric's [remarks](../documents/profile_opset/where/reviews/eric.md) on operator `where`.
- [ ] (1501-1, Sebastian) Specify some operators...
  - Sebastian is working on `reshape`and other ops... 
- [ ] (1501-2, Eric & Jean) Find a way to involve more people in the specification work...
- [ ] (1501-5, Anne-Sophie) Move issues to the "graph" part when they concern the graph (and not a specific operator)
- [X] (1812-3, Mariem) Complete the formal specification of `conv` with the help of FM experts (Augustin, Christophe, Cong, Eduardo, Loïc, etc.)
  - Moved to the general activity on formal spec. 
- [ ] (1812-6, All) Check legal aspects of contributing to the SONNX effort ("clearance")
- [ ] (0412-6, Eric) Create a sub working group to analyze the existing standard in a systematic way...
  - Contribution of Anne-Sophie. But WG to be set. 
  - Take into account the new modality to manage and report issues to ONNX (from [2023/03/19 meeting](./Other_meetings/2025-03-20-An-Er-Se-Je.md))
    - [ ] Create a review form

# 2025/03/12
## Participants
  - Nicolas, Cong, Dumitru, Anne-Sophie, Eric, Jean-Baptiste, Henri, Jean-Loup, Andreas (partially) (at least).
  - As usual, the meeting has been recorded. See [here]
## Agenda
  - Problem with meeting invitations (?)
  - Review of actions
  - Presentation of ONNX graph semantics (Dumitru)
  - Status on ARP
    - First set of answers received. Will be completed by Friday 14th
  - Review of newly described operators (see [DIV](../documents/profile_opset/div/div.md), [LSTM](../documents/profile_opset/lstm/lstm.md), other?)
  - Subjects raised by Andreas and Sebastian and further discussed with Nicolas (see [minutes](../documents/profile_opset/lstm/reviews/meeting_mom.md)):
    - Relations with ONNX
      - Compliance with ONNX spec
        - Nicolas:
          > I propose that for each operator .md file, we specify the full compliance with ONNX spec and we add a bottom section SONNX in the operator page, where we express the restrictions like : this input XXX shall be static, the B bias shall be explicitly defined, Broadcast not supported (reshape shall be prepended when required)...
          > This will show our specification work (math expressions, illustrations) mainstream to all the ONNX community from the ONNX documentation entry point, and also the SONNX 'value' for curious/interested people at the bottom of each operator page.
      - Visibility 
        - Sebastian/Nicolas:
          > For visibility and adoption, we shall avoid having a SONNX documentation entry point different from mainstream ONNX.
        - Andreas 
          > 1.  One if not the central meeting at Onnx is the SIG Operators meeting. It takes place every month.  
          > I think we should actively bring our points there to\
          > a. Get a discussion about our thoughts, from the experts who know operators, know how the way would be to implement them.\
          > b) We could also draw more attention to our initiative there.
          > 2. The next Onnx Community Meetup will probably take place in June 2025. (https://github.com/onnx/steering-committee/blob/main/meeting-notes/2025/20250305.md)\
          There we will have the opportunity to present what we are doing and what we have achieved.
          > 3. I think we need to create a lot more issues at https://github.com/onnx/onnx in order to work out the concerns more clearly,or to be able to discuss them even more with the community there, or to be able to refer to them in the Operators Meeting.
          > 4) As there are certainly already issues concerning SONNX at the moment, I could well imagine a new label “sonnx” for this, so that we can filter even better according to the topics. => you could ping me "andife" directly at the github issue and I add that specific label
    - Tooling
      - ONNX to SONNX converter
      - Model checker
      - *How to fund those developments?*
    - Other 
      - Graph semantics... Who?
## Minutes
- [Presentation of the ONNX graph semantics by Dumitru](./slides/2025-03-12-Dumitru%20on%20ONNX-graph-semantics.pdf)
  - The semantics is pretty simple (as far as I [eric] understand
    - considering a Directed Graph composed of nodes and edges, where 
      - a node is an operator
      - a edge connects a node output to a node input 
      - the graph is acyclic
    - considering that an edge carries either no value of a value(ii) the graph contains no cycle, 
    - considering that all edges carry no value initially
    - considering that an edge gets a value when the node whose output is associated with is executed
    - considering that a node can ony be executed when all edges associated with its inputs have a value 
    - executing a graph means executing every node until all nodes have been executed.
  - The graph is stateless, so if the computation requires a state, this state shall be managed outside of the graph. Such question are (very) relevant when dealing with reactive systems, but they do not concern the SONNX spec. 
  - Pipelining or other implementation concerns (e.g., scheduling of nodes execution) are not relevant to the specification
  - Questions were raised about 
    - operators implementing a random behaviour 
      - a deterministic behavior can be achieved by providing seeds to each and every random op. 
    - batch norm
      - batch norm is replaced by a constant at inference time
  - Brief presentation of the DIV operator that shows of implementation of the same operator for Real, Float and Int number can be specified. 
  - Presentation of the LSTM operator 
    -  A few verifications and corrections needs to be done, see action [1203-4].
 - Discussion about the presentation of our work to ONNX
   - Eric: I would prefer to present our results once we are completely happy with a first subset of operators. This will hopefully be the case in for the Meetup in June. In the meantime, we have to figure out with ONNX people who our work needs to be "integrated" with theirs. See action [1203-5]
 - Discussion about the tooling
   - We have identified two tools: one to check a model with respect to SONNX, and one to convert a model from standard ONNX to SONNX.
     - With respect to certification, the second one may not be a "good idea" <off-meeting (eric): it may still be useful during the first debugging phases>. see acton [1205-6].
 - The last point about "issues" has not been discussed.
## New actions
- [ ] (1203-1, Eric) Propose a first specification of the graph execution semantics on the basis of Dumitru's slied and ONNX doc.
- [ ] (1203-2, Dumitru) Propose an draft spec of LSTM where the operator would be specified using SCAN.
- [ ] (1203-3, Jean-loup) Do a review of the LSTM operator
- [ ] (1203-4, Nicolas) The relation between the directions and the dimension of the tensors shall be expressed by a constraint, not the assignment of a variable. The attributes must be presented before the description of the operator. Check that any activation function can be used for atc1 to act3. For the backward LSTM, check if the output needs to be reverted. Create a jupyter note (in collab) to illustrate the use of the operator (in the same way as for the DIV operator).
- [ ] (1203-5, Eric, Jean and Andreas) Organize a meeting with ONNX to present our first results (in order for them to have an idea of the expected end-result) and discuss what could be the integration modalities.
- [ ] (1205-6, Eric, Jean) See how to proceed with tool implementation
## Past actions
- [X] (1202-1, Eric) Reschedule Alexandre presentation
  - Presentation planned on April 9th. 
- [ ] (1202-2, Eric) Discussion to be initiated with ONNX about the integration of our work...
- [ ] (1202-3, All) Review new operators processed by Henri 
  - Reminder : place your comment in a dedicated file `<name>.md` in the "review" directory of the relevant operator
  - [X] Eric: review and modification of operator [`Div`](../documents/profile_opset/div/div.md)
- [ ] (1202-4, All) Define the appropriate way to specify the behaviour of operators for value out of range. Apply the approach on the `div` operator, for parameters in $\mathcal R$ and, `double`and `int`.
  - [X] Eric: See operator [`Div`](../documents/profile_opset/div/div.md)
- [ ] (1202-5, All) Define appropriate rules to handle multiples types without multiplying the specifications. 
  - See example of operator [`Div`](../documents/profile_opset/div/div.md))
- [X] (2901-1, Eric) Check how to express constraints about SparseTensor at operator level.
  - Only tensors of class "Tensors" are supported (SparseTensor are not supported). Such restriction applies to all operators. They are placed in document [General restrictions](../documents/profile_opset/general_restrictions.md) 
- [X] (2901-2, Anne-Sophie) Put back the issues (in the appropriate section) and add the answers given by Sebastian.
- [X] (2901-3, Eric) Provide a Jupyter notebook for the `conv` operator (see [here](../documents/profile_opset/conv/tests/conv_onnx.ipynb)).
  - Done for operator `Div`.
- [ ] (2901-4, Dumitru) Contact Nicolas to lend a hand on LSTM. 
- [ ] (2901-5, Dumitru) Prepare a short presentation  on the graph's semantics. Planned for March 12th.
- [X] (2901-6, Edoardo) Check how to involve students in the specification work.
  - On 12/02 : Edoardo has done some internal advertisement... waiting...
- [X] (2901-7, Jean-Baptiste) Analysis of EASA's Concept Paper.
- [ ] (2901-8, Henri) Consider Eric's [remarks](../documents/profile_opset/where/reviews/eric.md) on operator `where`.
- [ ] (1501-1, Sebastian) Specify some operators...
  - Sebastian is working on `reshape`and other ops. 
- [ ] (1501-2, Eric & Jean) Find a way to involve more people in the specification work...
  - *Thinking...*
- [ ] (1501-5, Anne-Sophie) Move issues to the "graph" part when they concern the graph (and not a specific operator)
- [X] (1501-6, All) Review issues reported by Anne-Sophie in file [issues.md](../documents/issues.md). Put your remarks in the [reviews](../deliverables/issues/reviews/) directory (in file `<you_name>.md`) or send them to me.
- [ ] (1812-3, Mariem) Complete the formal specification of `conv` with the help of FM experts (Augustin, Christophe, Cong, Eduardo, Loïc, etc.)
  - Discussion on-going with Loïc on the formal specification strategy...
  - Meeting planned to reach a final consensus...
  - Meeting done. See [minutes](../meetings/formal_methods/minutes.md).
- [ ] (1812-5, All) Indicate on which operator one can contribute (writer/reviewer). Put your id in this [table](./operator_spec_sub_wg/worksharing.md) The list of operators with their "complexity" and links to the ONNX doc are in this [Excel sheet](./operator_spec_sub_wg/SONNX_Operator_List.xlsx)
- [ ] (1812-6, All) Check legal aspects of contributing to the SONNX effort ("clearance")
- [ ] (0412-6, Eric) Create a sub working group to analyze the existing standard in a systematic way...
  - Contribution of Anne-Sophie. But WG to be set. 

# 2025/02/26
*Canceled.*

# 2025/02/12
## Agenda
- Presentation of ONNX MLIR (Alexandre Eichenberger) [postponed]
- Review of actions
- Some questions from Sebastian
  > I'm still not 100% clear, what we want to achieve with our operator specifications. 

  > **Is it intended that they appear in the official ONNX documentation and then the restrictions for SONNX may be below in the same text?** 
  > Otherwise, they will probably not be very visible to the public... <span style="color:blue"> See action (1202-0)  </span>

  > And is it clear that the norms you have to fulfill will require these formal specifications?
  
  > We work in very safety-critical projects and so far, it seems that a formal verification of numerical correctness compared to the original trained model is enough for most customers on our side (...]

  > For me the most critical operators are those that can create overflow or division by zero and there are a lot of them: Div, Exp, Log, Pow, Softmax, SoftPlus, Sqrt <span style="color:blue"> See action (1202-3) </span>
- "Review" of Henri's work
- Review of Jean-Baptiste work (<span style="color:blue"> See action (1202-2) </span>)
- Reply from the WG114 on our questions

## Attendees
(???)

## Minutes
- Presentation of ONNX MLIR (Alexandre Eichenberger) to be rescheduled. (<span style="color:blue"> See action (1202-1) </span>)
- "Review" of Henri's work
  - <span style="color:blue"> See action (1202-3) </span>
  - See new operators [here](../documents/profile_opset/) 
  - Question about error conditions: *How do we specify as the expected behaviour of an operator when a parameter is out of range (e.g., denominator of `div` is 0?)*
    - In the `div`spec, for instance, Henri has proposed to return `inf` (when the numerator is different from zero, otherwise a NaN shall be returned).
    - We have proposed a [first set of rules](./errors/error_specification.md). Basically, the behaviour of the operator is not defined when we cannot guarantee that its parameter are in range. However:
      - This raises a problem because more often than not, we cannot guarantee that the error condition (e.g., $x<=0$ for operator `log`) will not occur.
      - This would mean that any output value would be suspicious while we could actually be able to handle appropriately some singular values (such as /0)...
      - *This is clearly not satisfying.* We have to propose a better way to handle these cases. We may get some inspiration from the C standard: our interpretation would be determined according to the semantics of ISO C.  
    - Note that we have to discriminate cases where the operation is mathematically undefined (e.g. /0) from cases where the implementation of the operator may go wrong (e.g., overflow). Considering the `div` operator, if we are in $\mathcal R$ >, there is no `inf` value to be returned: the operation is simply undefined.
    - <span style="color:blue"> See action (1202-4) </span>
  - Question about types
    - The first batch of operators are specified in $\mathcal R$, so there should be no reference to types. In a second phase, we will have to specify the operators with actual types. When an operator has multiple parameters, we should either require all parameters to have a specific type, or the same types, etc. This may lead to many specifications...  
    - <span style="color:blue"> See action (1202-5) </span>
- Discussion about the integration of our work in ONNX (see Sebastian's question above). 
  - Our work must be part of the official ONNX documentation
  - Our spec could be added to the existing doc as a link to "SONNX".
  - A process shall be defined in order to ensure the consistent evolution of ONNX and SONNX.
    - We propose to wait until we have fully covered a few operators (incl. with their implementation types)
  - <span style="color:blue"> See action (1202-6) </span>
- Presentation of Jean-Baptiste's work
  - <span style="color:blue"> See action (1202-2) </span>
  - This work makes a mapping between the EASA's concept paper and the ARP. it also identifies the EASA's objectives that are relevant to SONNX. Note that Mohamed and Jean-oup have done a similar work (yet more focused) in the context of the DeepGreen project.
  - First draft to be validated at Airbus and with people from WG114.
- About the management of operators and reviews:
  - /!\ Don't forget to indicate on which operator you are working (in this [table](./operator_spec_sub_wg/worksharing.md)) in order to prevent overlaps... /!\
  - Please use the gconf to do your review. And when taking account of reviews, authors shall indicate in the review form what has been taken into account (KO/OK/TBD).

## New actions
- [X] (1202-1, Eric) Reschedule Alexandre presentation
- [ ] (1202-2, Eric) Discussion to be initiated with ONNX about the integration of our work...
- [ ] (1202-3, All) Review new operators processed by Henri 
  - Reminder : place your comment in a dedicated file `<name>.md` in the "review" directory of the relevant operator
- [ ] (1202-4, All) Define the appropriate way to specify the behaviour of operators for value out of range. Apply the approach on the `div` operator, for parameters in $\mathcal R$ and, `double`and `int`.
- [ ] (1202-5, All) Define appropriate rule to handle multiples types without multiplying the specifications. 
- [ ] (1202-6, Eric) Check with ONNX how to integrate our work.
## Past actions

- [ ] (2901-1, Eric) Check how to express constraints about SparseTensor at operator level.
- [ ] (2901-2, Anne-Sophie) Put back the issues (in the appropriate section) and add the answers given by Seb.
- [ ] (2901-3, Eric) Provide a Jupyter notebook for the `conv` operator (see [here](../documents/profile_opset/conv/tests/conv_onnx.ipynb)).
- [ ] (2901-4, Dumitru) Contact Nicolas to lend a hand on LSTM. 
- [ ] (2901-5, Dumitru) Prepare a short presentation  on the graph's semantics. Planned for March 12th.
- [ ] (2901-6, Edoardo) Check how to involve students in the specification work.
- [ ] (2901-7, Jean-Baptiste) Analysis of EASA's Concept Paper.
- [ ] (2901-8, Henri) Consider Eric's [remarks](../documents/profile_opset/where/reviews/eric.md) on operator `where`.
- [ ] (1501-1, Sebastian) Specify some operators...
  - Sebastian is working on `reshape`and other ops. 
- [ ] (1501-2, Eric & Jean) Find a way to involve more people in the specification work...
  - *Thinking...*
- [ ] (1501-5, Anne-Sophie) Move issues to the "graph" part when they concern the graph (and not a specific operator)
- [ ] (1501-6, All) Review issues reported by Anne-Sophie in file [issues.md](../documents/issues.md). Put your remarks in the [reviews](../deliverables/issues/reviews/) directory (in file `<you_name>.md`) or send them to me.
- [ ] (1812-3, Mariem) Complete the formal specification of `conv` with the help of FM experts (Augustin, Christophe, Cong, Eduardo, Loïc, etc.)
  - Discussion on-going with Loïc on the formal specification strategy...
  - Meeting planned to reach a final consensus...
  - Meeting done. See [minutes](../meetings/formal_methods/minutes.md).
- [ ] (1812-5, All) Indicate on which operator one can contribute (writer/reviewer). Put your id in this [table](./operator_spec_sub_wg/worksharing.md) The list of operators with their "complexity" and links to the ONNX doc are in this [Excel sheet](./operator_spec_sub_wg/SONNX_Operator_List.xlsx)
- [ ] (1812-6, All) Check legal aspects of contributing to the SONNX effort ("clearance")
- [ ] (0412-6, Eric) Create a sub working group to analyze the existing standard in a systematic way...
  - Contribution of Anne-Sophie. But WG to be set. 


# 2025/01/29
## Agenda
- Review of actions
- Other news
  - Contact with Altera.
- Operator specifications
  - Overview of the [`matmul`](../documents/profile_opset/matmul/matmul.md) and [`where`](../documents/profile_opset/matmul/where.md) operators
  - Current status of the [operators](./operator_spec_sub_wg/SONNX_Operator_List.xlsx) and [contributors](./operator_spec_sub_wg/worksharing.md) list.
- Formal specification
  - Feedback on [last meeting](./formal_methods/minutes.md).
- Other topics: 
  - Verification tool
  - talks in 2025
## Attendees
Jean, Julien, Eric, Mariem, Dumitru, Jean-Loup, Andreas, Sebastian, Jean-Baptiste, Tomé, João, Augustin, Anne-Sophie
<div class="off"> (Zoom does not give me a list of participants and I have not noted who was there...so the list if incomplete, sorry about that. Please add your name... </div>

## Minutes
- ONNX model verification tool
  - This tool will implement the constraints and restrictions identified at operator and graph level
  - The tool shall be part of the ONNX distribution
  - Using (e.g.) DeepGreen's ONNX parser could make sense but (i) we have to be sure that we can distribute it as part of ONNX, (ii) it will bring with it part of the AIDGE framework (iii) it may be overkill with respect to the level of parsing that we actually need.
  - Developing our own parser (possibly from something already available...) could also be a way to specify formally the file format (i.e., a correct ONNX file is a file that can be parsed successfully by our parser).
- Review of the comments on the [`where`](../documents/profile_opset/matmul/where.md) operator
  - Sparse tensors have to be forbidden. This can be checked at the file level by looking for the usage of the SparseTensorProto class. 
    - In the specification of operators, we should state that such tensors cannot be used. This should be part of the operators' signatures. To be elaborated, see action [2901-1]
  - Henri has given an example in Python. Should we generalize this?
    - We propose to add a few example in a  Jupyter Notebook for each operator. 
    - The examples must use ONNX. 
    - Those examples are not a test suite. They allow the user to get acquainted  / play with of the operator. 
    - The behaviour of the operator in the Jupytrer notebook may be different from the one of reference implementation. 
      - In the Jupyter notebook, we have to be clear that the example is given for documentation only. 
    - See action [2901-3].
- Specification work
  - Nicolas has added LSTM to the operator's list. Dumitru proposes to help. See action [2901-4].
  - It could be useful to start thinking about the graph semantics... See action [2901-5].
  - The work moves slowly...
    - We lack volunteers to do the hard work... 
    - We may become more visible and reach out a larger community (and hopefully, have more volunteers) once we have a first set of specification, completed documents. 
    - Edoardo proposes to use students to help us on the specification activity. (Jean will have one student to work on this topic) See action [2901-6].
  <div class="off"> Note that the initial list of interested people was pretty large... we may ask if some of them are still interested to contribute... </div> 
- List of issues
  - Anne-Sophie has removed some entries from [issues.md](../deliverables/issues/issues.md) since some of the ambiguities have been solved thanks to Sebastian.
  - However, it make sense to keep them in the list since part of our job is to prevent such ambiguities... See action [2901-2].
- On the specification of behavior in case of errors
  - At operator level
    - Whenever a value is out of the operator's domain, its behavior is "undefined" (e.g. xi<=0 in x for operator log(x)). In that case, the specification shall (i) indicate the domain constraint and (ii) state that the behaviour of the operator is undefined should the constraint be violated.
    - For some operators, some inputs will generally be static, even though the ONNX does not enforce this. In that case, we may add a restriction to ensure that the tensor's value will be known before runtime, and add a constraints on its value to prevent runtime error. 
  - At graph level
    - In some cases, the structure of the graph can ensure that the inputs values of an operator will always be in domain even though, they may be not in the general case. 
    - We may also propagate the domain constraints backward up to the inputs, and provide the user with these constraint (which would restrict the graph input domain). This could be interesting, but goes further than a verification.  
    - Whenever we cannot guarantee the absence of runtime error, the model wil be considered "unsafe".
- Compliance with regulatory docs.
  - It would be useful to identify the constraints/reqs in the EASA's concept paper that are relevant to our work. See action [2901-7]
- Formal methods.
  - See [minutes](../meetings/formal_methods/minutes.md) of FM sub-group on Feb. 28th.
  - Main conclusion: We will be using Why3 as the specification language. Work will start with a training session (being planned mid-march) done by Loïc. 
## New actions
- [ ] (2901-1, Eric) Check how to express constraints about SparseTensor at operator level.
- [ ] (2901-2, Anne-Sophie) Put back the issues (in the appropriate section) and add the answer given by Seb.
- [ ] (2901-3, Eric) Provide a Jupyter notebook for the `conv` operator (see [here](../documents/profile_opset/conv/tests/conv_onnx.ipynb)).
- [ ] (2901-4, Dumitru) Contact Nicolas to lend a hand on LSTM. 
- [ ] (2901-5, Dumitru) Prepare a short presentation  on the graph's semantics. Planned for March 12th.
- [ ] (2901-6, Edoardo) Check how to involve students in the specification work.
- [ ] (2901-7, Jean-Baptiste) Analysis of EASA's Concept Paper.
- [ ] (2901-8, Henri) Consider Eric's [remarks](../documents/profile_opset/where/reviews/eric.md) on operator `where`.
## Past actions
- [ ] (1501-1, Sebastian) Specify some operators...
  - Sebastian is working on `reshape`and other ops. 
- [ ] (1501-2, Eric & Jean) Find a way to involve more people in the specification work...
  - *Thinking...*
- [X] (1501-4, All) Review the specification of the [`where` operator](../documents/profile_opset/where/where.md). Put your remarks in the [reviews](../documents/profile_opset/where/reviews/) directory (in file `<your_name>.md`) or send them to me (eric).
  - See Eric's [remarks](../documents/profile_opset/where/reviews/eric.md).
- [ ] (1501-5, Anne-Sophie) Move issues to the "graph" part when they concern the graph (and not a specific operator)
- [ ] (1501-6, All) Review issues reported by Anne-Sophie in file [issues.md](../documents/issues.md). Put your remarks in the [reviews](../deliverables/issues/reviews/) directory (in file `<you_name>.md`) or send them to me.
- [X] (1501-7, Eric) Check how to communicate with ONNX to sort out ambiguities...
    - The best solution is probably to use the [ONNX] test suite, which covers operators and graph. "Just in case", I have also contacted RAM at ONNX.
    - After a discussion with Ram : We can use the LFx slack channel (Operator SIG). Two contacts : G. Ramalingam and Justin Chu
- [X] (1508-1, Eric) Send the list of questions to the WG 114 leader.
  - List of questions sent to the WG114 chairwoman on Jan. 16th.
  - They'll analyze them and come back to us.
- [X] (1812-2, Eric) Complete the discussion about numerical accuracy and error management.
  - See mail dated 19/12.
  - See [new version of the document](./errors/error_specification.md)
- [ ] (1812-3, Mariem) Complete the formal specification of `conv` with the help of FM experts (Augustin, Christophe, Cong, Eduardo, Loïc, etc.)
  - Discussion on-going with Loïc on the formal specification strategy...
  - Meeting planned to reach a final consensus...
  - Meeting done. See [minutes](../meetings/formal_methods/minutes.md).
- [ ] (1812-5, All) Indicate on which operator one can contribute (writer/reviewer). Put your id in this [table](./operator_spec_sub_wg/worksharing.md) The list of operators with their "complexity" and links to the ONNX doc are in this [Excel sheet](./operator_spec_sub_wg/SONNX_Operator_List.xlsx)
- [ ] (1812-6, All) Check legal aspects of contributing to the SONNX effort ("clearance")
- [X] (0412-4, Thiziri, Nicolas, Jean, Sebastian, Jean-Loup) Review of the [updated version of CONV2D](../documents/conv_specification_example/README.md)
    - Review from Thiziri to be received on 2024/12/20.
    - *No answer => Closed*
- [ ] (0412-6, Eric) Create a sub working group to analyze the existing standard in a systematic way...
  - Contribution of Anne-Sophie. But WG to be set. 


# 2025/01/15
## Agenda
- Edoardo's presentation about the "Evaluation and improvement of SW verifiers on FP Neural Networks"
- Recall of the workplan, current status of the WG achievements
- Review of actions
- Status on [questions about the ARP ](../documents/analysis_of_standards/clarification_replication,.md)
- Status of CONV operator, review of Henri's `WHERE`operator
- Brief review of issues identified by Anne-Sophie, see [Issues](../documents/issues.md)
- Status on formal methods
- Discussion on the behavior in the presence of errors (see action 1812-2)

## Attendees
Edoardo, Eric, Jean, Mariem, Sebastian, Augustin, Dumitru, Henri, Nicolas, Cong, Jean-Loup [sorry, some names are probably missing ; I don't know how to obtain the list of attendees using LFAI...]

## Minutes 
- Edoardo's slides can be found [here](./slides/2025-01-15-Edoardo_Manino_SONNX_slides.pdf).
- Status of the current outoputs of our WG. We are a bit late with respect to the initial plan... 
  - Concerning the specification work, we can take `conv` as an example, even though it may be later modified thanks to the lessons learnt on other operators.
  - We have to find people to work on the specification. See action [1501-1] and [1501-2].
- Status of the work on formal methods. 
  - The strategy is not clear yet...
  - Mariem organizes a meeting to find a consensual formalization strategy. See action [1501-3].
- Discussion on Henri's specification of the `where` operator. 
  - It can be reviewed, see action [1501-4].
  - In order to enforce determinism, broadcasting should be forbidden. This is a general rule to be applied to all operators.
  - In a conservative manner, we may express restrictions in the first version of the operator and relax those restrictions later should they represent too strong a constrainst.
  - Discussion about the `if` operator which allows different subgraphs to be executed depending on a boolean value. Note that this operator does not violate the general rule about the execution condition of an operator: by construction, the `if` operator execute either one or another graph that are completely separated (they do not join).  
  - Discussion about `if`concern the specification of the graph execution semantics, which is an activity that has not yet started. 
-  Presentation of some of the issues identified by Anne-Sophie. 
   - Discussion about the interpretation of the tensor axis indexes. How do they relate to batch, channels, etc. Should we express this relation in the specification (ex. `split`operator). It actually depend on the operator: for some operators, this interpretation is necessary, and for other it is not. For instance, the `add` operator works can be used without giving any particular interpretation to the tensor's dimension (all axes play a symmetrical role). this is not the case for the convolution for instance. 
   -  Some issues actually concern the graph execution semantics. See action [1501-5].
   -  Remarks have to be reviewed (action [1501-6])in order to see if there reveal an actual issue and, if yes, how to address it. When there is an ambiguity, we may rely on an actual implementation of the ONNX specification to determine the actual semantics. But which implementation should be taken as a reference? OnnexRuntime, another? One solution may be to ask the ONNX committee in charge of the operators.  (see action [1501-7]).
- Concerning the question about the ARP, the list of question has been reviewed. Eric will send it to the WG114 in the name of the workgroup. See action [1501-8]. 
## New actions
- [ ] (1501-1, Sebastian) Specify some operators...
- [ ] (1501-2, Eric & Jean) Find a way to involve more people in the specification work...
- [X] (1501-3, all) Drop an e-mail to Mariem should you be interested in the work on formal methods
- [ ] (1501-4, All) Review the specification of the [`where` operator](../documents/profile_opset/where/where.md). Put your remarks in the [reviews](../documents/profile_opset/where/reviews/) directory (in file `<you_name>.md`) or send them to me.
- [ ] (1501-5, Anne-Sophie) Move issues to the "graph" part when they concern the graph (and not a specific operator)
- [ ] (1501-6, All) Review issues reported by Anne-Sophie in file [issues.md](../documents/issues.md). Put your remarks in the [reviews](../deliverables/issues/reviews/) directory (in file `<you_name>.md`) or send them to me.
- [ ] (1501-7, Eric) Check how to communicate with ONNX to sort out ambiguities...
- [ ] (1508-1, Eric) Send the list of questions to the WG 114 leader.
  - List of questions sent to the WG114 chairwoman on Jan. 16th.

## Past actions
- [X] (1812-1, Mariem et Eric) Process reviews of `conv`. 
  - Done. Spec moved [here](../documents/profile_opset/conv/)
- [ ] (1812-2, Eric) Complete the discussion about numerical accuracy and error management.
  - See mail dated 19/12.
- [ ] (1812-3, Mariem) Complete the formal specification of `conv` with the help of FM experts (Augustin, Christophe, Cong, Eduardo, Loïc, etc.)
  - Discussion on-going with Loïc on the formal specification strategy...
  - Meeting planned to reach a final consensus...
- [X] (1812-4, Eric) Provide a "complexity" estimation for each operator
    - Done, see [Excel sheet](./operator_spec_sub_wg/SONNX_Operator_List.xlsx)
- [ ] (1812-5, All) Indicate on which operator one can contribute (writer/reviewer). Put your id in this [table](./operator_spec_sub_wg/worksharing.md) The list of operators with their "complexity" and links to the ONNX doc are in this [Excel sheet](./operator_spec_sub_wg/SONNX_Operator_List.xlsx)
- [ ] (1812-6, All) Check legal aspects of contributing to the SONNX effort ("clearance")
- [ ] (0412-4, Thiziri, Nicolas, Jean, Sebastian, Jean-Loup) Review of the [updated version of CONV2D](../documents/conv_specification_example/README.md)
    - Review from Thiziri to be received on 2024/12/20.
- [ ] (0412-6, Eric) Create a sub working group to analyse the existing standard in a systematic way...
  - Contribution of Anne-Sophie. But WG to be set. 

# 2024/12/18
## Agenda
- Sebastian's presentation on Bosch's code generation tool.
- Review of actions
- Results of last review of ``conv2d``
- Overview of the first version of the [list of requirements](../documents/reqs.md)
- Discussion about the operators to integrate in the profile (see the [list of operators](./operator_spec_sub_wg/SONNX_Operator_List.xlsx))
- Call for contributors to reqs and description of ops. 
- Output from ``conv2d`` last review.
## Attendees
Andreas Fehlner, Christophe Garion, Cong Liu, Edoardo Manino,  Eric Jenn, Jean Souyris, Jean-Baptiste Rouffet, Jean-Loup Farges, Sebastian Boblest, Mohammed, Anne-Sophie Lalloyer, Andreas Dittberner, Benjamin Wagner, Duy Khoi Vo, Julien Vidalie, Thiziri Belkacem, Nicolas Valot, Henri Belfy
## Minutes
(The meeting has been recorded and is available [here](https://zoom.us/rec/play/Gp1BMRCA01sUw-m0lXeewLgfPIPRlluJ3Cfi_AakBAruDRvm5CSWSf_bj19PHA6Ky99dXm2mlASBkEKu.Ws8R97q6D_W-k0a_?canPlayFromShare=true&from=share_recording_detail&continueMode=true&componentName=rec-play&originRequestUrl=https%3A%2F%2Fzoom.us%2Frec%2Fshare%2FPTdcIxVJaVSPh1Ze39mu3zmVqjYJ0sB33oR76VOsWpsKlbnaGtQwa7r4bkp1OF3a.5BpTwCuQlXolU4uC) for those who have an LFX account. Note that there is also a full textual transcript of the meeting, which includes all the Mmmm, the hesitations, the globbish, etc. Nevertheless, this is extremely handy, you can even click on the text and the video will move at the appropriate place. If we were able to cut /paste the transcript in ChatGPT to generate a synthesis, that'll be perfect...)
- Sebastian's presentation on Bosch's Embedded Ai coder.
  - Two things (please refer to the video for the full contents):
    - Bosch is (in particular) targetting very small models (starting with a few hundrerds parameters) to be run on very small targets (microcontrollers).
    - One important expectation for Bosch: having a tool to check the (S)ONNX model... 
    - One important expectation for Bosch's customer: be able to reproduce results on a long time span. 
- Brief overview of the first version of the [requirement list](../documents/reqs.md). There has been quite a few comments on reqs 19 and 20 about errors. This issue will be addressed in a separate discussion (see action 1812-2) 
- Discussion about the list of operators and the way we have to "process them"
  - We have to share the work! Eric will add a "complexoity" evaluation to the current list of operators (1812-4), then every contributor can put his/her name in front of the operator on which he/she can contribute (as a writer, a reviewer). See action (1812-5). Note that we will start the work when the specification of the ``conv`` operator is completed (since it will be used as a template).
- Sebastian raised an important remark concerning the actual capability of people to contribute to the effort. Everyone has to check the legal aspects of contributing to the SONNX effort which, eventually, will be part of ONNX (exact modalities have to be addressed). See action (1812-6)
## New actions
- [ ] (1812-1, Mariem et Eric) Process reviews of `conv2D`. 
- [X] (1812-2, Eric) Complete the discussion about numerical accuracy and error management.
  - See mail dated 19/12.
- [ ] (1812-3, Mariem) Complete the formal specification of `conv2d` with the help of FM experts (Augustin, Christophe, Cong, Eduardo, Loïc, etc.)
- [X] (1812-4, Eric) Provide a "complexity" estimation for each operator
    - Done, see [Excel sheet](./operator_spec_sub_wg/SONNX_Operator_List.xlsx)
- [ ] (1812-5, All) Indicate on which operator one can contribute (writer/reviewer). Put your id in this [table](./operator_spec_sub_wg/worksharing.md) The list of operators with their "complexity" and links to the ONNX doc are in this [Excel sheet](./operator_spec_sub_wg/SONNX_Operator_List.xlsx)
- [ ] (1812-6, All) Check legal aspects of contributing to the SONNX effort ("clearance")
## Past actions
- [X] (0412-1, Eric) Integrate CS' use case in the [list of use cases](../documents/usecases.md)
- [X] (0412-2, Eric, Jean) Check Airbus's needs.
- [X] (0412-3, Eric) Integrate Henri's comments in the list of questions to WG114. Integrate questions raised by Jean-Baptiste presentation about hyperparameters (what are those hyperparameters, precisely), why do they need to carry this information in the MLMD, for what purpose?
- [ ] (0412-4, Thiziri, Nicolas, Jean, Sebastian, Jean-Loup) Review of the [updated version of CONV2D](../documents/conv_specification_example/README.md)
    - Reviews from Henri, Nicolas and Jean-Loup received and processed.
    - Review from Thiziri to be received on 2024/12/20.
- [X] (0412-5, Mariem) Replace the sentence that uses "shifted" by "the kernel is applied to data 2 units on right in the first spatial axis and to data 3 units down in the second spatial axis"
- [ ] (0412-6, Eric) Create a sub working group to analyse the existing standard in a systematic way...

# 2024/12/04
## Agenda
- Review of actions
- Feedback on meeting about formal methods (see minutes [here](../meetings/formal_methods/minutes.md))
- Review of [Airbus' needs](../documents/needs.md)
- Review of [Jean-Baptiste's analysis of the ARP6983](../documents/analysis_of_standards/SONNX_requirements_draft1.docx)
- Review of [questions about ARP6983](../documents/analysis_of_standards/clarification_replication.md)
- Review of [CONV2D updated version](../documents/conv_specification_example/README.md)
- Status about SONNX mailing list
- Discussion about new modalities for meetings

## Participants
Eric, Mariem, Edoardo, Pierre B., Jean-Loup, Pierre G., Mohammed, Jean-Baptiste, Thiziri, Henri, Jean, Julien, Eric B., Andreas F., Nicolas, Cong, Dittberner Andreas D.,  Sebastian

## Minutes
- CS case study.
  - Mohamed has provided a short description of CS' use case to be integrated in the [list of use cases](../documents/usecases.md). See action (0412-1).
- Review of Airbus' needs.
  - Current content is a raw integration of material provided by Sergei and discussed with Jean and Eric.
  - The needs have first to be checked by the authors in oder to remove redundancy, ensure that the needs are clear (see e.g., need about resource usage). See action (0412-2)
- Review of [Jean-Baptiste's analysis of the ARP6983](../documents/analysis_of_standards/SONNX_requirements_draft1.docx)\
  Several questions were raised during the presentation:
  - The standard requires the MLMD to carry the hyperparameters used during training...
    - What do they call "hyperparameters", exactly? According to some interpretation, the architecture of the model is itself described by "hyperparameters" (in the sense that when using AutoML, the architecture is also "learnt"). This has to be clarified. 
    - Why do they require this? To ensure the repeatability of the training process? But in that case, we need more that this. We need a complete description of the training environment, possibly the exact scheduling of the training operations, etc.  What is the exact intent of this requirement?
      - Pseudo Random Number Generators must be "controlled" in order to ensure repeatabilty of training. There is a discussion in ONNX "operators" SIG about this subject. See Andreas F.'s [note](https://gist.github.com/Craigacp/883f7e628ce91a370ce4bc3519c9cca0). See also [here](https://github.com/onnx/onnx/issues/6302) and [there](https://github.com/onnx/onnx/issues/6408). Other discussions on theat subject took place in the ONNX Operators SIG's slack channel. Those interested could joint the [SIG's meeting](https://zoom-lfx.platform.linuxfoundation.org/meeting/93845487316?password=87cf871b-389e-416b-ae73-60fbe608bc6b).
  - The standard is not very demanding concerning the relation between the model used during training and the MLMD (only "traceability" is required, not "conformity"). Is this really sufficient? If conformity is required, than this ** may ** require additional data to be put in the MLMD. 
- [Comments fromon the ARP6983](../documents/analysis_of_standards/clarification_replication.md)
  - Review of Henri's comments
    - Questions were raised about
      - the "inadequate or incorrect inputs detected during the ML Constituent architecture design process" (about what input are we talking? what does "inadequate" mean?).
    - the comparison of the characteristics of the training and target platform (the platform must be "similar". What does "similar" mean? What is the intent of this requirement?)
  - Jean-Loup's comments: not discussed.
  - Eric to integrate Henri's and Jean-Loup's comments, complete the list of questions, propose a mail to the WG114. The objective is to have a feedback fro them ASAP. See action (0412-3)
- CONV2D operator: Reviews from Jean-Loup and Sebastian have nee taken into account.See the [presentation of the modifications after review](./general/slides/2024-12-04-modifiedconv2Dinformalspec.pdf). A last review is necessary to obtain the "template" that will be used to do the work for the other operators. see action (0412-4).
  - Integrate Jean-Loup proposal to avoid the terms "moved", "shifted": ""the kernel is shifted by 2 units in the first spatial axis and 3 units in the second spatial axis" => "the kernel is applied to data 2 units on right in the first spatial axis and to data 3 units down in the second spatial axis". See action (0412-5)
- Formal methods:
  - A meeting took place about the use of formal methods to describe operators. See the [presentation](./formal_methods/slides-29-11.pdf) that was done at that occasion, and the [incremental minutes](./formal_methods/minutes.md). The main conclusion are that (i) a formal specification is useful, (ii) ACSL could be the most appropriate formalism. 
- Other subjects:
  - Sub-group on Reqs: no new contributors besides Sebastian's and Henri...  
  - Set-up a sub-group to analyse the ONNX standard to continue Nicolas' work which is collected in document [issues](../documents/issues.md). See action (0412-6)
## New actions
- [ ] (0412-1, Eric) Integrate Cs' use case in the [list of use cases](../documents/usecases.md)
- [ ] (0412-2, Eric, Jean) Check Airbus's needs.
- [ ] (0412-3, Eric) Integrate Henri's comments in the list of questions to WG114. Integrate questions raised by Jean-Baptiste presentation about (i) hyperparameters (what are those hyperparameters, precisely), why do they need to carry this information in the MLMD, for what purpose?
- [ ] (0412-4, Thiziri, Nicolas, Jean, Sebastian, Jean-Loup) Review of the [updated version of CONV2D](../documents/conv_specification_example/README.md)
- [ ] (0412-5, Mariem) Replace the sentence that uses "shifted" by "the kernel is applied to data 2 units on right in the first spatial axis and to data 3 units down in the second spatial axis"
- [ ] (0412-6, Eric) Create a sub working group to analyse the existing standard in a systematic way...
## Past actions
- [X] (2011-1 - Jean, Eric) Integrate Airbus' additional needs/reqs.
- [X] (2011-2 - Eric) Make a call for participation to the req core team. 
- [X] (0611-1 - Eric, Nicolas, Jean-Loup) Finish the discussion about "reproducibility"...
      - On going, see [this note](../documents/analysis_of_standards/2024-11-08%20-%20Replication%20criteria.md)
- [ ] (0611-2 - Eric) Prepare a followup to the discussion about computation errors: what is the impact on the MLMD?
- [X] (0611-5 - Eric, Mariem) Update conv2d spec from Sebastian's and Jean-Loup's reviews
  - To be done by next meeting.
- [ ] (231001 - All) Check Nicolas' classification proposal 
- [X] (231002 - Mohammed) Propose a use case for CS, [here](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/documents/usecases.md)
  - In progress. The case study is drone tracking. Transformers are used, but the model remains "simple"  enough to be embedded...
  - Done. The application is an object detection based on transformers. See [description](...)
- [ ] (231002 - Sebastian) Get in touch with other people in the automotive partners (e.g. ETAS).
- [ ] (231002 - Luis) Provide contact(s) with other industrial domains (medical,...)
    - On-going (see previous meeting)
- [ ] (A008 - leads) Plan SC meetings
- [ ] (A009 - Dumitru) Correct  / complete description of issue #2
      - Dumitru will check this...
profile/meetings/numerical_issues/01_what_is_the_issue.md}. Please add your ideas / remarks...
      - First discussion in the 11/06 WG meeting
- [ ] (A015) All : Complete description of use cases
      - On-going
- [ ] (A016) All : Complete description of needs
      - On-going
- [ ] (A002 - all) Add / remove your name for the [participant list ](https://github.com/ericjenn/working-groups/blob/da1fb275bcbfb32af95fd8ef54589cde0e14f927/safety-related-profile/meetings/team.md) and provide information about your possible contribution
- [ ] (A004 - all) Propose a short communication during the next WG meetings. The list is [here](https://github.com/ericjenn/working-groups/blob/da1fb275bcbfb32af95fd8ef54589cde0e14f927/safety-related-profile/meetings/presentation_proposals.md).
  - Alexandre Eichenberger (IBM),  on onnx-mlir (2025/??/??)
  - ??? on specification and verification of FP computations (2025/??/??)
  - Eduardo (Manchester U) on "Evaluation and improvement of SW verifiers on FP Neural Networks" (2025/??/??)
- [ ] (A006 - leads) Finalize the organization of the WG's repository. Define procedure to use it (inc. issues, wiki,...)
  - Meeting with Nathan and Andreas to be organized (use of [Linux Foundations' LFX](https://sso.linuxfoundation.org/)) 
  - Reply from Nathan on 11/05. Mailing list, etc. should be available by week 11/18
  - Meeting moved to 2024/11/21
- [X] (A007 - leads) Setup a mailing list
  - Meeting with Nathan and Andreas to be organized (use of [Linux Foundations' LFX](https://sso.linuxfoundation.org/)) 
  - Reply from Nathan on 11/05. Mailing list, etc. should be available by week 11/18
  - Meeting moved to 2024/11/21


# 2024/11/20

## Agenda
- Review of actions
- Status of deliverables
  - D1.a: Safety-related Profile Scope Definition
  - D1.b.<x>: End users' needs and requirements for domain <x>.
  - D1.c: Consolidated needs for all industrial domains
![image](https://github.com/user-attachments/assets/7b081310-cf71-4136-b796-e254faf72483)
- Discussion about modalities
## Participants
Marko, Sebastian, Julien, Jean, Henri, Augustin, Yohann, Mohammed, Eric B., Eric J.

## Minutes
- We are late: deliverable D1.1 was due Oct. 2024, and D1.2 was due Nov. 2024. We have very few needs / reqs, and all from the aero domain. Additional reqs will certainly come from Jean-Baptiste analysis of Aero standards (see action ). Airbus will propose material to complete the list of needs / reqs by the end of this week.
  - [ ] (Jean, Eric) Integrate Airbus' additional nededs / reqs.
- Providing a first list of needs/reqs will certainly clarify what is expected in D1.2...
- In order to accelerate the process, Jean proposes to set up a "core team" composed of representatives of the different industrial domains (or other interested people too). Those people will work specifically on "needs" and "requirements". They will meet in specific meetings... Sebastian and Henri will participate (thanks!). A local physical meeting with people from Airbus, Thales, ADS, TAS, IRT could also be organized in order to speed up the process.  
  - [ ] (Eric) Make a call for participation to the req core team.    
  
## New actions
- [ ] (2011-1 - Jean, Eric) Integrate Airbus' additional needs/reqs.
- [ ] (2011-2 - Eric) Make a call for participation to the req core team. 
## Previous actions
- [ ] (0611-1 - Eric, Nicolas, Jean-Loup) Finish the discussion about "reproducibility"...
      - On going, see [this note](../documents/analysis_of_standards/2024-11-08%20-%20Replication%20criteria.md)
- [ ] (0611-2 - Eric) Prepare a followup to the discussion about computation errors: what is the impact on the MLMD?
- [X] (0611-3 - Eric) Integrate paper in [document](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/meetings/numerical_issues/01_what_is_the_issue.md).
- [X] (0611-4 - Jean-Loup) Review the conv2d operator
      - Reviews are [here](../documents/conv_specification_example/reviews)
- [ ] (0611-5 - Eric, Mariem) Update conv2d spec from Sebastian's and Jean-Loup's reviews
  - To be done by next meeting.
- [ ] (231001 - All) Check Nicolas' classification proposal 
- [ ] (231002 - Mohammed) Propose a use case for CS, [here](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/documents/usecases.md)
      - In progress. The case study is drone tracking. Transformers are used, but the model remains "simple"  enough to be embedded...
      - To be done by next meeting.
- [X] (231002 - Jean-Baptiste) Provide a first analysis of the ARP 6983 / EASA concept paper
      - In progress. Under validation. 
      - First draft version to be delivered on next week. To be reviewed.
      - No document received as of 20/11/2024. Eric contacted Jean-Baptiste on 20/11/2024.
      - Document received on 2024/11/21, see [here](../documents/analysis_of_standards/SONNX_requirements_draft1.docx)
- [ ] (231002 - Sebastian) Get in touch with other people in the automotive partners (e.g. ETAS).
- [ ] (231002 - Luis) Provide contact(s) with other industrial domains (medical,...)
    - On-going (see previous meeting)
- [ ] (A008 - leads) Plan SC meetings
- [ ] (A009 - Dumitru) Correct  / complete description of issue #2
      - Dumitru will check this...
profile/meetings/numerical_issues/01_what_is_the_issue.md}. Please add your ideas / remarks...
      - First discussion in the 11/06 WG meeting
- [ ] (A015) All : Complete description of use cases
      - On-going
- [ ] (A016) All : Complete description of needs
      - On-going
- [ ] (A002 - all) Add / remove your name for the [participant list ](https://github.com/ericjenn/working-groups/blob/da1fb275bcbfb32af95fd8ef54589cde0e14f927/safety-related-profile/meetings/team.md) and provide information about your possible contribution
- [ ] (A004 - all) Propose a short communication during the next WG meetings. The list is [here](https://github.com/ericjenn/working-groups/blob/da1fb275bcbfb32af95fd8ef54589cde0e14f927/safety-related-profile/meetings/presentation_proposals.md).
  - [X] Sebastian Boblest (Bosch) on their tool (2024/12/18)
  - Alexandre Eichenberger (IBM),  on onnx-mlir (2025/??/??)
  - ??? on specification and verification of FP computations (2025/??/??)
  - Eduardo (Manchester U) on "Evaluation and improvement of SW verifiers on FP Neural Networks" (2025/??/??)
- [ ] (A006 - leads) Finalize the organization of the WG's repository. Define procedure to use it (inc. issues, wiki,...)
  - Meeting with Nathan and Andreas to be organized (use of [Linux Foundations' LFX](https://sso.linuxfoundation.org/)) 
  - Reply from Nathan on 11/05. Mailing list, etc. should be available by week 11/18
  - Meeting moved to 2024/11/21
- [ ] (A007 - leads) Setup a mailing list
  - Meeting with Nathan and Andreas to be organized (use of [Linux Foundations' LFX](https://sso.linuxfoundation.org/)) 
  - Reply from Nathan on 11/05. Mailing list, etc. should be available by week 11/18
  - Meeting moved to 2024/11/21


# 2024/11/06
## Agenda
- Review of actions
- Feedback on ``conv2d`` operator review (Sebastian)
- Computations accuracy
  - In the last meeting, we have identified that the precision (of computations) of computations are issue. This subject deserves a dedicated meeting and work. All material concerning this topics can be found [here](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/meetings/numerical_issues). A first list of questions and some "food for thought" are available [here](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/meetings/numerical_issues/01_what_is_the_issue.md)
- Other events
  - [ISCLP meeting](https://www.defense.gouv.fr/dga/evenements/ouverture-inscriptions-au-seminaire-futur-lembarque-critique-systemes-combat) at DGA-TA Toulouse
  - Collab. with [DeepGreen](https://deepgreen.ai/) project about reference implementation (followup to [10/25 meeting minutes](safety-related-profile/meetings/Other_meetings/2024-10-25-DeepGreen.md) )

## Participants
JENN Eric, Adrian Evans, Pierre Gaillard, Nicolas Valot , Edoardo Manino, Jean-Loup , Julien VIDALIE, COMBES Yohann, BELCAID Mohammed, Jean-Baptiste Rouffet, Jean Souyris , Cong Liu, Jean-Loup Farges, Claire Pagetti , Thiziri Belkacem Airbus Protect , Dumitru Potop, Sebastian Boblest , Sergei CHICHIN, Boblest Sebastian, Vo Duy Khoi

## Minutes
- Discussion about computation errors (see presentation in [markdown](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/meetings/numerical_issues/slides-06-11.md) and [pdf](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/meetings/numerical_issues/2024-11-06%20-%20Numerical%20issues.pdf))
  - **Slide 10: About weak and strong reproducibility**\
      - Statement is not clear.\
      The idea is that complying with the specification (the MLMD) does not ensure reproducibility: if the specification allows some error with respect to the true value, an implementation may compy with the specification without complying with reproducibility. Therefore, this is another property.  How compliance with the MLMD is ensured is another problem. We may use the "reference implementation" (RI), but it only moves the problem since we will have to demonstrate compliance of the RI to the MLMD... 
      - What does "all implementation" mean?\
        It refers to the set of all *potential* implementations that would comply to the MLMD, not the *actual* set of implementations (which is a subset of the former...). 
      - About the empirical evaluation of the effects of computation errors, see paper "[Causes and effects of unanticipated numerical deviations in neural networks inference frameworks](https://proceedings.neurips.cc/paper_files/paper/2023/file/af076c3bdbf935b81d808e37c5ede463-Paper-Conference.pdf)"
      - About non-determinism: here, we only care about inference, not training ; we only consider non-determinism due to numerical computations, not other sources such as random number generators...
      - Reproducibility is also a concern for audit activities (or "auditability").
      - [ ] (Eric, Nicolas, Jean-Loup) Finish the discussion about "reproducibility"...
      - [ ] (Eric) Integrate paper in [document](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/meetings/numerical_issues/01_what_is_the_issue.md). 
  - **Slide 12: importance of accuracy for ML**
      The effects of mathematical error may strongly depend on the type of application (e.g., regression *vs.* classification) 
  - **Slide 15: mathematical libraries**
    - There are version of ``libm`` that give explicitly accuracy requirements. See e.g., [sleef](https://github.com/shibatch/sleef/tree/master/docs/2-references/libm)
  - **Slide 17**
    - Over/under flow can be easily avoided using "accumulator" with a sufficient size. <off meeting: but overflow may occur in other situations>
    - **General** 
      - The slide are focus on the second part of the W cycle. Howver, as the MLMD is at he transition  between the two Vs, we also have to consider the relation between the ML model used during training and evaluation and the MLMD. In particular, what needs to be put in the MLMD to support the activities occuring in the ascending part of the first V (in order to ensure that the MLML delivered to the developper is correct)? 
      - In fact, what is (could be considered as) the actual reference is the model used for the training and evaluation that is executed using e.g., TensorFlow. Therefore, we shall provide all embed all the necessary information (metadata) in the MLMD to precisely designate this environment (framework, version of framework, machine, operating system,etc.). Note that the current version of ONNX aleady has this capability. <off meeting: another approach would be to consider that the evaluation of the model should be done using the reference implementation. This would really make the SONNX model THE specification.../>
  - [ ] (0611-2 - Eric) Prepare a followup to the discussion about computation errors: what is the impact on the MLMD?
  
- Review of Sebastian's remarks on the ``conv2d`` operator specification
  - Detailled remarks are in [Sebastian's branch](https://github.com/SebastianBoblest/working-groups/tree/lookAtConvSpec/safety-related-profile/documents/conv_specification_example). 
  - Major remarks:
    - Some restrictions (of the current version) prevent the description of some of the use models. For instance, the ``group`` attribute must support depthwise convolution with channel multiplier 1.
    - Many attributes of the ONNX spec are optional or "redundant" in the sense that their role can be played using other, more primitive attribnutes. For instance, the ``auto_pad`` attribute can be replaced by an explicit choice of padding. 
    - The SONNX profile shall provide a single solution without restricting capabilities ("There shall be a unique way to do things").
    - It also makes life of "customers" (aka "users") simpler.
    - The presentation is OK. The diagram must be kept, but corrected (see detailled comments)
    - [ ] (Jean-Loup) Review the conv2d operator
    - [ ] (Eric, Mariem) Update conv2d spec according to Sebastian's and Jean-Loup's reviews
  
## New actions
- [ ] (0611-1 - Eric, Nicolas, Jean-Loup) Finish the discussion about "reproducibility"...
- [ ] (0611-2 - Eric) Prepare a followup to the discussion about computation errors: what is the impact on the MLMD?
- [ ] (0611-3 - Eric) Integrate paper in [document](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/meetings/numerical_issues/01_what_is_the_issue.md).
- [ ] (0611-4 - Jean-Loup) Review the conv2d operator
- [ ] (0611-5 - Eric, Mariem) Update conv2d spec from Sebastian's and Jean-Loup's reviews
   
## Previous actions
- [ ] (231001 - All) Check Nicolas' classification proposal 
- [ ] (231002 - Mohammed) Propose a use case for CS, [here](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/documents/usecases.md)
      - In progress. The case study is drone tracking. Transformers are used, but the model remains "simple"  enough to be embedded...
- [ ] (231002 - Jean-Baptiste) Provide a first analysis of the ARP 6983 / EASA concept paper
      - In progress. Under validation. 
      - First draft version to be delivered on next week. To be reviewed.
- [ ] (231002 - Sebastian) Get in touch with other people in the automotive partners (e.g. ETAS).
- [X] (231002 - Sebastian and Luis) Review of the [Conv2d operator](https://github.com/ericjenn/working-groups/tree/ericjenn-srpwg-wg1/safety-related-profile/documents/conv_specification_example).
  - Done: to be discussed with Sebastian on 11/06
- [ ] (231002 - Luis) Provide contact(s) with other industrial domains (medical,...)
  - On-going:  
  > Regarding the invitation of experts to participate in the WG:
  > - Health sector: [METTLER]  the contacts were identified, the emails were sent, and we are waiting on their response.
  > - Railway sector: [ALSTOM] the contacts were identified.
  > Meanwhile do you think relevant to get more experts into the WG from the automotive industry (working in autonomous drive)?
  > I have good contacts in the H2020 project consortium Hi-Drive (www.hi-drive.eu [...]  Should I try to get some of them onboard?
- [X] (231002 - Eric) Provide one slide about SONNX.
  - Done: see [here](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/meetings/Other_meetings/2024-11%20-%20ISCLP%20meeting%20-%20SONNX.pptx)
- [ ] (A008 - leads) Plan SC meetings
  - No action.
- [ ] (A009 - Dumitru) Correct  / complete description of issue #2
      - Dumitru will check this...
- [X] (A012 - Nicolas) Review the the "issues" document
- [X] (A013 - leads) Organize a meeting on numerical computations (fp-sg)
      - Pending. Subject to be addressed durint the next meeting 2024/11/06. Draft material is available [here]{https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/meetings/numerical_issues/01_what_is_the_issue.md}. Please add your ideas / remarks...
      - First discussion in the 11/06 WG meeting
- [ ] (A015) All : Complete description of use cases
      - Pending
- [ ] (A016) All : Complete description of needs
      - Pending
- [ ] (A002 - all) Add / remove your name for the [participant list ](https://github.com/ericjenn/working-groups/blob/da1fb275bcbfb32af95fd8ef54589cde0e14f927/safety-related-profile/meetings/team.md) and provide information about your possible contribution
- [ ] (A004 - all) Propose a short communication during the next WG meetings. The list is [here](https://github.com/ericjenn/working-groups/blob/da1fb275bcbfb32af95fd8ef54589cde0e14f927/safety-related-profile/meetings/presentation_proposals.md).
  - Sebastian Boblest (Bosch), on their tool (to be planned)
  - Alexandre Eichenberger (IBM),  on onnx-mlir (to be planned)
  - ??? on specification and verification of FP computations
- [ ] (A006 - leads) Finalize the organization of the WG's repository. Define procedure to use it (inc. issues, wiki,...)
  - Meeting with Nathan and Andreas to be organized (use of [Linux Foundations' LFX](https://sso.linuxfoundation.org/)) 
  - Reply from Nathan on 11/05. Mailing list, etc. should be available by week 11/18
- [ ] (A007 - leads) Setup a mailing list
      - Meeting with Nathan and Andreas to be organized (use of [Linux Foundations' LFX](https://sso.linuxfoundation.org/)) 
  - Reply from Nathan on 11/05. Mailing list, etc. should be available by week 11/18

# 2024/10/23
## Agenda
- Review of actions
- Rapid review of current contents of Use Cases and Needs
- Work sharing and commitments (who can contribute to what?)
- Work on the PoC : review of the informal description, improvements
- Other events

## Participants

JENN Eric, TURKI Mariem, Filipo PEROTTO, Julien VIDALIE, Andreas Fehlner, JB Rouffet, BELCAID Mohammed, Nicolas Valot, BELFY Henri, Luís Conde, BONNAFOUS Eric, Jean-Loup Farges, Jean Souyris, Cong Liu, Dumitru Potop, Claire Pagetti, Edoardo Manino, Sebastian Boblest  

## Minutes
- Presentation of the Use Case document
  - Airbus Aircraft (target DAL C), Thales AVS (29-32 : not necessary, DAL : not yet defined, MobileNet and YoloV8 are necessary)
          - Dumitru would be interrested in having a presentation of the Use case? In particular what are the use cases using recurrent networks... (no action at this point)
          - Jean: there are significant differences between the operator sets. In fact, THAV has listed the operators from the standard models (e.g., Yolo) they plan to use.
  - Classification of operators
      - Nicolas proposes a tentative classification (see [here]([to be defined](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/documents/ONNX_Op_classification.xlsx))).
          - [ ] (All) Check Nicolas' classification proposal 
      - [ ] (Mohammed) Propose a use case for CS, [here](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/documents/usecases.md)
      - Jean-Loup proposes to add a classification criterion concerning certification in order to group operators raising similar issues. (Sebastian: e.g. operators potentially raising to numerical exceptions...)
      - [ ] (Jean-Baptiste) Provide a first analysis of the ARP 6983 / EASA concept paper
      - Sebastian: Customers often develop their model from scratch for they have very specific needs. They usually don't use models out of a zoo. For quantified model, they use TensorFlow lite. They are not using quantified ONNX quentified operators.
      - [ ] (Sebastian) Get in touch with other people in the automotive partners (e.g. ETAS).
- Review of the PoC specification
  - [ ] (Sebastian and Luis) Review of the [Conv2d operator](https://github.com/ericjenn/working-groups/tree/ericjenn-srpwg-wg1/safety-related-profile/documents/conv_specification_example).
  - [ ] (Luis) Provide contact(s) with medical and railway domains.
- Claire and Christophe to make a presentation to [ISCLP ](https://www.defense.gouv.fr/dga/evenements/ouverture-inscriptions-au-seminaire-futur-lembarque-critique-systemes-combat) about ARP, replication, etc.
- [ ] (Eric) Provide one slide about SONNX.
- Eric and Jean will discuss with people from the [DeepGreen](https://deepgreen.ai/) project in order to see how we coud share the effort / reference implementation
- **/!\PLEASE CONTRIBUTE TO THE DESCRIPTION OF [USE CASES](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/documents/usecases.md) AND [NEEDS/REQS](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/documents/needs.md) /!\\**
  - Concerning use cases, please provide links to the standard models (when applicable)

## New actions
- [ ] (231001 - All) Check Nicolas' classification proposal 
- [ ] (231002 - Mohammed) Propose a use case for CS, [here](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/documents/usecases.md)
- [ ] (231002 - Jean-Baptiste) Provide a first analysis of the ARP 6983 / EASA concept paper
- [ ] (231002 - Sebastian) Get in touch with other people in the automotive partners (e.g. ETAS).
- [ ] (231002 - Sebastian and Luis) Review of the [Conv2d operator](https://github.com/ericjenn/working-groups/tree/ericjenn-srpwg-wg1/safety-related-profile/documents/conv_specification_example).
  - Done: to be discussed with Sebastian on 11/06
- [ ] (231002 - Luis) Provide contact(s) with other industrial domains (medical,...)

## Previous actions
- [ ] (A008 - leads) Plan SC meetings
  - No action.
- [ ] (A009 - Dumitru) Correct  / complete description of issue #2
- [X] (A010 - leads) Create a “tools” area <closed on 03/10>
- [X] (A011 - Nicolas) Deposit his operator extraction tool in the repository. <closed on 03/10>
- [X] (A012 - Nicolas) Review the the "issues" document
- [ ] (A013 - leads) Organize a meeting on numerical computations (fp-sg)
      - Pending. Subject to be addressed durint the next meeting 2024/11/06. Draft material is available [here]{https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/meetings/numerical_issues/01_what_is_the_issue.md}. Please add your ideas / remarks...
      - First discussion in the WG on 11/06
- [X] (A014 - fp-sg) Provide a clear statement of the numerical computations issues.
      - See A013.
- [ ] (A015) All : Complete description of use cases
      - Pending
- [ ] (A016) All : Complete description of needs
      - Pending
- [ ] (A002 - all) Add / remove your name for the [participant list ](https://github.com/ericjenn/working-groups/blob/da1fb275bcbfb32af95fd8ef54589cde0e14f927/safety-related-profile/meetings/team.md) and provide information about your possible contribution
- [ ] (A004 - all) Propose a short communication during the next WG meetings. The list is [here](https://github.com/ericjenn/working-groups/blob/da1fb275bcbfb32af95fd8ef54589cde0e14f927/safety-related-profile/meetings/presentation_proposals.md).
  - Sebastian Boblest (Bosch), on their tool (to be planned)
  - Alexandre Eichenberger (IBM),  on onnx-mlir (to be planned)
  - ??? on specification and verification of FP computations
- [X] (A005 - leads) Organize sub-group on formal methods (fm-sg).
      => Meeting planned on 29/10
- [ ] (A006 - leads) Finalize the organization of the WG's repository. Define procedure to use it (inc. issues, wiki,...)
  - Meeting with Nathan and Andreas to be organized (use of [Linux Foundations' LFX](https://sso.linuxfoundation.org/)) 
  - Reply from Nathan on 11/05. Mailing list, etc. should be available by week 11/18
- [ ] (A007 - leads) Setup a mailing list
      - Meeting with Nathan and Andreas to be organized (use of [Linux Foundations' LFX](https://sso.linuxfoundation.org/)) 
  - Reply from Nathan on 11/05. Mailing list, etc. should be available by week 11/18

# 2024/10/02
## Agenda
- Presentation of "templates" to start of activies on
    - definition of [use cases, models, operators](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/documents/usecases.md)
    - elicitation of [needs](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/documents/needs.md)
    - identificaiton of [issues ](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/documents/issues.md)
- Discussion about the creation of a sub-group (who?)
    - on formal methods
    - on numerical issues (?)
- Status of integration with ONNX community
    - Brief presentation of the Linux Fundation support to our activities (=> Andreas, Friday, report during next meeting)
  
## Participants
(Was not able to retrieve the list from TEAMS)
## Minutes
- See agenda
  
### About the “Steering Committee”
- EMB will not be able to participate to our periodic meetings (every two weeks) but is nevertheless willing to contribute to our effort via a *Streeing Committe* (SC). The objective of the SC is to monitor important (”key”) moments in the progression of activities (“gates” , “phase transitions”, etc.).
- The SC shall be planned in advance. Basically: one SC every SC will be fine.
- [ ] (A008 - leads) Plan SC meetings

### About the templates
3 “template” document were presented (see link above)
- “Issues template”
    - Dumitru proposes to add a description / illustration of the effects of an issue. ⇒ to be added in the template
    - Concerning issue #2 (order of operations)
        - Dumitru (following a remark already done by Sebastian, a long time ago…)  emphasizes that there is not problem of non determinism / interpretation on the order of processing of operator: if one follows the topological ordering,  result of floating point computations are completely and unambiguoulsy determined. There may still be issues with random numbers.
        - [ ]  (A009 - Dumitru) Correct  / complete description of issue #2
- Use case / scope template
    - Nicolas : a description can simply refer to an existing model in the Hugging Face repository using a hypertext link.
    - Nicolas proposes a script to extract the list of operators. (To be placed in the “tools” area)...
    - [ ] (A010 - leads) Create a “tools” area
    - [ ] (A011 - Nicolas) Deposit his operator extraction tool in the repository
    - [ ] (A012 - Nicolas) Review the the "issues" document
  
### About sub-groups

- Floating point computation
    - [ ]  (A013 - leads) Organize a meeting on numerical computations (fp-sg)
    - [ ]  (A014 - fp-sg) Provide a clear statement of the numerical computations issues.

- Formal methods
    - The PoC must be completed, incl. aspect about formal methods
    - The value of a formal specification must be estimated (value in terms of communication, automation,…)
    - A formal language must be selected.
    - This is to be covered by the fm-sg, see action A005

Other (off-meeting) 
- [ ]  (Nicolas) See if we can involve the authors of the paper on ONNX conversion in order to identify Exploiter le papier / probblème
      
#### New actions
- [ ] (A008 - leads) Plan SC meetings
- [ ] (A009 - Dumitru) Correct  / complete description of issue #2
- [X] (A010 - leads) Create a “tools” area <closed on 03/10>
- [X] (A011 - Nicolas) Deposit his operator extraction tool in the repository. <closed on 03/10>
- [ ] (A012 - Nicolas) Review the the "issues" document
- [ ] (A013 - leads) Organize a meeting on numerical computations (fp-sg)
- [ ] (A014 - fp-sg) Provide a clear statement of the numerical computations issues.
- [ ] (A015) All : Complete description of use cases
- [ ] (A016) All : Complete description of needs

#### Previous actions
- [X] (A001 - Embraer) Clarify the role / organisation of the "Steering Committe". <closed on 02/10>
- [ ] (A002 - all) Add / remove your name for the [participant list ](https://github.com/ericjenn/working-groups/blob/da1fb275bcbfb32af95fd8ef54589cde0e14f927/safety-related-profile/meetings/team.md) and provide information about your possible contribution
- [X] (A003 - leads) Create templates to start feeding the list of **use cases**, **needs**, **requirements**, **issues**. <closed on 02/10>
- [ ] (A004 - all) Propose a short communication during the next WG meetings. The list is [here](https://github.com/ericjenn/working-groups/blob/da1fb275bcbfb32af95fd8ef54589cde0e14f927/safety-related-profile/meetings/presentation_proposals.md).
- [ ] (A005 - leads) Organize sub-group on formal methods (fm-sg).
- [ ] (A006 - leads) Finalize the organization of the WG's repository. Define procedure to use it (inc. issues, wiki,...)
- [ ] (A007 - leads) Setup a mailing list

#### Closed actions
(to be completed)

# SONNX meeting (04/09)

## Object
- ONNX Safety-related workgroup meeting

## Attendees
- Jean, Eric (ed.), Claire, Dumitru, Sergei, Henri, Nicolas,  Mariem
  
## Agenda
- Status of actions (see below)
  - [X]  <21/08> (Mariem) Convert the CONV operator specification to markdown. (see [here](https://github.com/ericjenn/working-groups/tree/ericjenn-srpwg-wg1/safety-related-profile/documents/conv_specification_example))
  - [X]  <21/08> (eric+Jean) Clarifies the use of github… => SeeMariem's presentation below.
  - [X]  (eric+jean) Propose an agenda for the KOM => see text below.
  - [X]  (all) Read the SOW and provide your feedback
  - [X]  <21/08> (Eric+Jean) In the SoW, Add to the SoW activities related to the validation of the WG results through its application to a practical use case

- KOM Agenda and organisation
  - Invitation text:
  >Dear Colleague,
  > On September 25th, 17:00-19:00, we organize the kick-off meeting of the Safety-Related Profile ONNX Working Group (WG).
  > The objective of this working group is to refine and clarify the semantics and syntax of the existing ONNX standard, ensuring unequivocal interpretation of models during the implementation phase.
  > This initiative was presented to the ONNX community during the ONNX MeetUp (June 26th, 2024) and the creation of the WG was accepted by the ONNX community on July 18th, 2024.
  > You will find the slides presented during this meeting here.  We will come back to this presentation and go into more details during the KOM. 
  > The agenda is available here. 
  > The "outlook invitation" will be sent in another mail. 
  > If you want to participate and have not received this invitation directly, please send a message to Eric (eric.jenn@irt-saintexupery.com) and Jean (jean.souyris@airbus.com).
  > Looking forward to meeting you on September 25th,
  > The co-chairs,
  > Eric JENN (IRT Saint-Exupéry) et Jean SOUYRIS (Airbus)

  - Proposed agenda
      1. **Introduction**: Presentation of the general objectives of the workgroup based on the slides shown during the meetup (Eric + Jean, 10 min)
      2. **Phase 1: Why?**
         1. Presentation of an example of regulatory requirements: the ARP. (Christophe, 15 min)
         2. Presentation of a few examples of issues posed by the current standard, choosing problems of various natures (Nicolas, 15 min)
      3. **Phase 2: What?**
         1. Presentation of an example of a set of requirements (???, to be prepared, 10 min)
         2. Presentation of an example of what the output of the work could be for the specification of an operator (Mariem + Eric, 15 min)
      4. **Phase 3: How?**
         1. Presentation of the work plan and the organization of the working group (Eric + Jean, 15 min)
         2. Brief presentation of the "hard points" that we have already identified (10 min)
      5. **Discussion** (All, 30 min)
      - Use of Github: See _Mariem presentation_
    
- Workplan (simplified)
    - See [here](https://extranet.irt-saintexupery.com/Extranet/Projets/SONNX/Work/_layouts/15/WopiFrame.aspx?sourcedoc=/Extranet/Projets/SONNX/Work/Documents%20partages/Admin/Workplan.xlsx&action=default)

## Minutes
- Discussion about the github structure and management.
    - Question was raised about the nature of the document we could put on the github:
      - The principle is that ANY document put on our repo is publicly accessible. So, **no document with restiction** shall be placed in the repo.
      - Concerning the possible publications of the workgroup, we will use a private Overleaf (e.g.) account to work in common. 
    - Mariem has reminded us the (usual) way to use github. See her [slides](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/documents/procedures/ModifGithubONNX.pdf)
    - This approach seems a bit complicated, especially if we are working in common on documents.It is necessary because the project is public and so requires some control before accepting modifications. Using a private project could be simpler. 
    - [X] (05/09) Henri to propose document edition / sharing modalities
      - See [proposal](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile/documents/procedures/collaborative_docs.md)
    - Currently, we are working on Eric's branch that is hosted in a private account (github.com/ericjenn/...). It may be cleaner to use a specific account for our workgroup (e.g., github.com/sonnx./...)

## Actions
  - [ ] (09/09) Eric to check if we could create a SONNX account in github
  - [ ] (05/09) Eric to check with Ram if there is any "rule"/ "contraint" imposed by ONNX on the use of github 
  - [X] (05/09) Henri to propose document edition / sharing modalities
    - See [proposal]()
  - [ ]  <21/08> (Mariem, eric, Loïc) Propose an first axiomatization of tensors (3D, 4D) and use it to specify the CONV operator.
  - [ ]  <21/08> (Mariem, Loïc, Eric, Augustin) Specify the CONV operator for int8 and (e.g., ) float16….
  - [ ]  <21/08> (Eric+Jean) In the SoW, avoid the use of the term “ambiguity”. Be more explicit about the different types of requirements. Introduce the concept of "replication" 
  - [ ]  <10/07>(eric+jean) Organize some meetings as “advisory boards”

# SONNX meeting (21/08)

## Object

- ONNX Safety-related workgroup meeting

## Attendees

- Mariem, Nicolas, Augustin, Eric

## Minutes

- Status of actions (see below)
- Brief recap of the work done on the CONV operator (Mariem)
    - The Why3 specification is now complete thanks to Loïc. A FrameC implementation is also available.
        
        
        - [ ]  <21/08> (Mariem) Convert the CONV operator specification to markdown.
    - After discussion with Loïc, the appropriate solution would be first to “axiomatize” tensors (in the same way it has already been done for matrices).
        
        
        - [ ]  <21/08> (Mariem, eric, Loïc) Propose an first axiomatization of tensors (3D, 4D) and use it to specify the CONV operator.
- Discussion of Nicolas’ comments on the SOW
    - Four points were discussed
        - We have introduced new terms (”TMD, TMDL) that are neither used in the ONNX community (where the term “ONNX IR” is used) nor in the ARP (where the term “MLMD” is used). We have either to stick to one of those — possibly ONNX’ — or at least explain the correspondence between them…
        - Nicolas mentioned that we have to “address the semantic of the model storage (ONNX IR for safety critical) […]”.
            - Yes, this should be covered by the activities concerning the semantics and the syntax of the model description language. Nicolas also raised the question about discriminating the model used during the design and the model used as the starting point of the implementation. *But it is not clear whether we really need to discriminate them: we are only concerned by the semantics of the model, whatever its used.* However, we will not consider operators used during training, so our profile will only be applicable during inference…
        - Nicolas what not happy with the remark about “ambiguous” models  (sentence  “[…] ambiguous if this ambiguity is acceptable or even necessary to leave some freedom to the implementer […]): *I do not see any reason for that. The model shall be unambiguous. If the implementer chooses to implement a surrogate model (optimized), then this model is the MLMD to be specified using ONNX. ARP6983 specifies that replication criteria shall be specified*.
            - This is an important point. The model shall actually be non ambiguous. The user may introduce derived requirements about implementation (e.g., the order in which operators have to be executed). This contingency is what was meant by the term “ambiguity”. We have to be more explicit in the SoW: the specification will not be ambiguous, but there will be some “flexibility” about the set of derived requirements applicable to a given model.
            
            - [ ]  <21/08> (Eric+Jeans) In the SoW, avoid the use of the term “ambiguity”. Be more explicit about the different types of requirements. Introduce the concept of “replication criteria” and clarify its relation to requirements.
        - Nicolas mentioned that “All the activities consist in paper work. Is there some room for POC for formal verification, extension of the definition of the format, tools to build, review, verify a SONNX MLMD ? Who are the users/recipients of the outputs ? (I would guess that some output are for us, some others for ONNX community...).”
            - Only the first part of the remark was discussed: we actually need some “practical” work in order to validate our proposal. We should introduce a “running example” (e.g., MobileNet) that will be specified using SONNX, implemented, compared with a reference implementation, etc.  Those “practical” implementation activities have to be described in the SoW too.
                
                
                - [ ]  <21/08> (Eric+Jeans) Add to the SoW activities related to the validation of the WG results through its application to a practical use case
- Discussion about polymorphic operators: *we have to provide a specific specification for every types supported by an operator,* i.e., there will be a specification of the CONV operator for int8, float16, etc. This is in particular necessary for ints for which saturation is necessary. We should do the exercise on the CONV operator.
    
    
    - [ ]  <21/08> (Mariem, Loïc, Eric, Augustin) Specify the CONV operator for int8 and (e.g., ) float16….
- We have to specify the broadcasting rules (see [https://github.com/onnx/onnx/blob/main/docs/Broadcasting.md](https://github.com/onnx/onnx/blob/main/docs/Broadcasting.md)).
- Logistics
    - All documents should be in the same place. At the moment, some documents are on the IRT’s sharepoint while some other at in the ONNX github. Office documents where placed in the Sharepoint for they were directly editable by some users. For other (e.g., Airbus), Sharepoint documents need to be downloaded first, which make Sharepoint pointless. 
    - [X]  <21/08> (Eric) Convert the SOW to markdown, move all documents to github
        - Documents have moved [here](https://github.com/ericjenn/working-groups/tree/ericjenn-srpwg-wg1/safety-related-profile/documents).
    - The Sharepoint has moved in order to match the new project name, which is “SONNX”. The URL is now : [https://extranet.irt-saintexupery.com/Extranet/Projets/SONNX/Pages/default.aspx](https://extranet.irt-saintexupery.com/Extranet/Projets/SONNX/Pages/default.aspx)
    - The github repository is accessible at  [https://github.com/ericjenn/working-groups/tree/ericjenn-srpwg-wg1/safety-related-profile](https://github.com/ericjenn/working-groups/tree/ericjenn-srpwg-wg1/safety-related-profile).
    
    - [ ]  <21/08> (eric+Jean) Clarifies the use of github…
    

## Actions

- [x]  (eric) Put the examples of mails (in French and English) to be used for dissemination purposes.

- [x]  (eric) Propose a poll for the project’s name, (all) answer the poll
    - (Updated 21/08) SONNX

- [ ]  (eric+jean) Propose an agenda for the KOM

- [ ]  (all) Read the SOW and provide your feedback )
- (Updated 21/08) Comments by Nicolas, see doc.

- [x]  (Nicolas) Collect the analysis done so far and put it in one document (on sharepoint or on the ONNX git, it’s up to you)
    - Done, the document is on the sharepoint ([https://extranet.irt-saintexupery.com/Extranet/Projets/SONNX/Work/_layouts/15/WopiFrame.aspx?sourcedoc=/Extranet/Projets/SONNX/Work/Documents partages/SoW/ONNX format comments v0.1.docx&action=default](https://extranet.irt-saintexupery.com/Extranet/Projets/SONNX/Work/_layouts/15/WopiFrame.aspx?sourcedoc=/Extranet/Projets/SONNX/Work/Documents%20partages/SoW/ONNX%20format%20comments%20v0.1.docx&action=default)”)

- [ ]  <10/07>(eric+jean) Organize some meetings as “advisory boards”
- [x]  <21/08> (Eric) Convert the SOW to markdown

<style> 
    .off{
        color:violet;
        font-style: italic;
        font-size: 10px
    }
</style>
