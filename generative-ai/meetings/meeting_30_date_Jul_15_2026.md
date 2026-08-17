# Recording and Transcript:

https://zoom.us/rec/share/fLbVGkpZUxeBp8qmYsSbO15_g4P8Xp4awfPt_JWNgScGWFBT56j8Zi4Uj9K3id79.W29VSQGOSrtcWWzc

# Meeting Minutes:

## ONNX Community Meetup Debrief

- Resources: Presentations and slides are being uploaded to the ONNX meetup website, with YouTube recordings [here](https://www.youtube.com/playlist?list=PLLIyVy1DXx5M).

## GQA ContribOp & KV Cache Layout Configuration

- Context & Issue: The standard ORT contrib op for Grouped-Query Attention (GQA) defaults to BNSH ([batch, num_heads, seq_len, head_size]). Some NPUs benefit from a BNHS format where sequence length is the innermost dimension.
- Proposal: Intel proposed adding an attribute to the GQA op to allow specifying alternate KV layouts (such as BNHS).
- Discussion Points:
  - Kunal clarified that BNSH was chosen for compatibility with Hugging Face Optimum and to avoid extra transposes during cache updates.
  - Rama raised concerns that exposing this via an attribute forces all backends to handle multiple layouts and can complicate global optimizations (potentially introducing unnecessary transposes).
  - Cem Pehlivan suggested exploring ORT's existing transpose-fusion and layout-optimization passes rather than modifying the op attribute.
- Action Item: Javier and Yamini to refine the proposal with concrete layout and optimization details before bringing it back to the group.
- Reference: [GQA Contrib Op Documentation](https://github.com/microsoft/onnxruntime/blob/main/docs/ContribOperators.md#com.microsoft.GroupQueryAttention)

## Grouped MatMul RFC & MoE Operator Representation

- Context: Motivated by Mixture-of-Experts (MoE), an RFC was opened to add a standalone GroupedMatMul operator.
- Discussion Points:
  - GroupedMatMul restricts computation to the top-selected experts instead of evaluating all experts, providing clear performance wins across backends. 
  - Rama cautioned against over-generalized "macro" fused MoE ops using graph-valued attributes for arbitrary activation functions (similar to issues observed with naive FlexAttention implementations).
  - The group agreed that primitive decompositions or backend-internal pattern-match fusions are preferable to monolithic ops for activations.
- Action Item: Community members to review and leave comments on the PR; target is to merge the RFC ahead of the next monthly meeting.
- Reference: [ONNX GroupedMatMul PR #8193](https://github.com/onnx/onnx/pull/8193)

## Backend Context & Ahead-of-Time (AOT) Compilation

- Status: Discussion around standardizing the backend context / AOT compilation workflow was deferred due to key stakeholder availability (notably European attendees from NVIDIA and others).
- Next Steps: Javier to coordinate an asynchronous discussion (via Slack/channel) and schedule a dedicated deep-dive session in 2–4 weeks.

## Proposed Topics for Next Meeting:

- Backend Context & ORT Package specification.
- General MoE strategy and aggressive fusion trade-offs.
- Paged Attention representation in ONNX.
- KV Cache Quantization (e.g., TurboQuant, QDQ-style representations).
