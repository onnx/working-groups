# Recording and Transcript:

https://zoom.us/rec/share/Zp0h_Wni7ERIsa4ixCIUffc_H6Kh9vkgr4Heh9kvtXYAwHTx6uqhczZ-psWy3EU.Ihb-C-mKMKL8a0Vl

# Meeting Minutes:

- ONNX Release Timeline
  - Next release is more likely to be 1.19 rather than 2.0 to avoid breaking compatibility. A 2.0 discussion might occur at a community meetup. The potential timeframe for the next release (1.19) was mentioned as July-September.
  - Yuan is the release manager. We can potentially align some of the proposals from the GenAI group with the next release.
- KV Cache Operator Proposal (Document: Attention op proposal):
  - Separation from Attention: Yuan proposed separating KV cache updates into a new, distinct operator rather than being part of the main Attention operator.
    - Reasoning: Handling batched updates for KV cache (where new tokens are appended to the end of the actual valid data, considering padding) becomes too complex to express with primitive ops if integrated directly into the Attention op.
  - Functionality: The new KV Cache op would take past_kv, present_kv (new tokens), and past_sequence_length as inputs and output the updated present_k and present_v. It essentially performs a "scatter" or "in-place update" into a larger tensor representing the cache.
  - In-Place Updates:
    - The design supports in-place updates where past_k/v and present_k/v have the same shape (dimension being max_sequence_length).
    - It was clarified that the ONNX op itself remains functional; true in-place memory optimization is a backend/compiler responsibility. The op design facilitates this by ensuring shape compatibility and relying on backends to potentially use aliasing APIs or lifetime analysis to reuse buffers if the user provides the same buffer for input and output of the cache.
  - Circular Buffers:
    - An open question from Gaurav was how to handle circular buffer updates (when kv_sequence_length exceeds max_sequence_length).
    - If supported, the modulo logic for wrap-around indexing would need to be part of the op's specification.
    - max_sequence_length would likely be derived from the input tensor shapes rather than being an explicit attribute to the op, allowing a single model to work with varying sequence lengths.
- Attention Operator Updates (Related to KV Cache):
  - With a separate KV Cache op, the Attention op would take q, k, v (where k and v are outputs of the KV Cache op), attention_mask, and kv_sequence_length as inputs.
  - Quantization Subgraphs:
    - Yuan discussed incorporating attribute subgraphs for quantization/dequantization (Q/DQ) operations related to attention inputs/outputs.
    - Rama expressed reservations about adding these as attributes for prologue/epilogue Q/DQ ops, suggesting they could remain outside the Attention op. He was more open to it for operations within the attention mechanism. Yuan suggested that internalizing them could simplify fusion for backends. Rama planned to review this further.
    - The restrictiveness of these subgraphs (e.g., allowing only Q/DQ/Cast vs. more complex operations like score_mod for Flex Attention) was an open point.
- Flex Attention Representation:
  - Yamini raised the issue of how to represent Flex Attention models in ONNX, as current Pytorch exports result in a higher-order op, not standard ONNX ops.
  - Justin Chu suggested that submodules captured within the exported program could potentially be represented as ONNX functions. The main logic of the higher-order op could then leverage these functions (similar to how the ‘If’ operator works).
  - This approach requires further investigation into the Pytorch-side compilation and main logic. Performance optimizations for such a representation in ONNX would be crucial.
- Exporter Considerations:
  - The team acknowledged the need to examine how current model exporters (e.g., Optimum, torch.dynamo via Transformers Executorch) handle KV caching to ensure the new ops align with existing practices.
  - Yamini mentioned recent experience with Transformers Executorch integration using torch.dynamo with static cache.

## Action Items:
- Yuan: Continue developing the specifications for the new KV Cache operator and updates to the Attention operator.
- Rama: To review the attention proposal regarding attribute subgraphs for quantization in the Attention operator and provide feedback.
- Yamini: To post a link on Slack regarding the Transformers Executorch exporter with static cache and to experiment with more score_mod and mask_mod configurations for Flex Attention.
- Justin Chu: To take a deeper look into representing Flex Attention's exported program logic in ONNX, exploring the use of ONNX functions.
- All Attendees:
  - Review Yuan's proposed spec (Attention op proposal) updates for the KV Cache and Attention operators.
  - Contribute to the backend representations document shared by Yamini on Slack.
