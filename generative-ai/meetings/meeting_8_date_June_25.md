# Recording and Transcript:

https://zoom.us/rec/share/Gk8h1bZmiu0LPAwKcm_KOll91VeYDUi7sV6dPDwpuGivCENj5m4SV9anQEHjW-hi.38aTzMxigw1kJXaB

# Meeting Minutes Summary
This week’s meeting primarily focused on two key topics: the Attention OP proposal and the Backend Context function design.

## Attention OP Proposal
The discussion revolved around how to represent and implement the attention operator, particularly regarding precision and quantization.
- Flex Attention and Graph Attributes: Yamini raised a question about whether "flex attention" was discussed as part of the attention proposal. Rama clarified that while flex attention wasn't specifically focused on, Yuan's proposal of using graph attributes for general graph operations was discussed, which could apply to flex attention and other issues.
- Backend Implementation Implications: Rama expressed concerns about the backend implications of using graph attributes, specifically regarding implementation complexity. He highlighted that if a graph attribute represents a subgraph with operations like Cast or Quantize/Dequantize, backends would need to parse these subgraphs at load time, which is more cumbersome than simply checking an integer attribute (like Softmax precision).
- Alternatives to Graph Attributes: Rama presented an alternative: using specific dtype attributes and zero point/scale parameters for quantization, rather than complex graph attributes. He asked for feedback on which approach would be preferred by implementers.
- Offline vs. Just-In-Time (JIT) Compilation: Rajnish explained that offline compilers could handle subgraphs by inlining them or using function call injections for templated kernels. He noted that JIT frameworks would likely adopt similar function call mechanisms. Rama's primary concern was the Just-In-Time (JIT) inference scenario, where checking subgraph formats at load time could introduce overhead, though caching could mitigate this.
- Hybrid Approach: Rajnish shared that TensorRT is considering a hybrid approach, using direct API attributes for common scaling and precision needs (e.g., BMM scaling) for speed, while also optionally extending to subgraphs for greater generality to support future attention variants like "Sage Attention."
- KV Caching: Yuan also discussed the KV cache update. Rama suggested using the regular ScatterND operation, but Yuan raised the need for a specialized operator due to the complexity of specifying multiple indices (batch, head, sequence position) for each token, especially during the preview phase with many tokens.

## Backend Context Function Design
- Yamini presented an initial draft of a backend context function [link](https://docs.google.com/document/d/1rfXqd36HdIpxPrlYsyJMqxtHa1rR81bB3eTZKck_O20), inspired by the EP context design, aiming for a more generic ONNX standard.
- Retaining Original Subgraph: The core idea is to retain the original ONNX subgraph within the backend context node. This allows for fallback to the ONNX subgraph if the precompiled objects (blobs) fail due to driver incompatibility or other reasons.
- Multiple Backends in One ONNX Model: The proposed design envisions a single ONNX model acting as a container, holding pre-optimized blobs for multiple backends. Each backend might have different unsupported ops, leading to different backend context nodes within the overall model. These blobs would share the original weights.
- Discussion Points:
  - Multiple IHVs in one file: Yamini questioned whether the goal is to support multiple Independent Hardware Vendors (IHVs) within a single ONNX file (e.g., Intel CPU and Nvidia GPU in one model) or if it's targeted for a specific platform.
  - Dynamic Scheduling: Rama raised the point of supporting dynamic scheduling decisions at runtime, where different devices might be chosen based on current load, which would require a flexible representation.
  - Node Duplication and Weight Sharing: Rama speculated that node duplication might not be a significant concern if weights can be effectively shared across different backend representations. Yamini agreed that this would require backends to support weight-free compilation and weight sharing.

## Action Items (ARs)
- All Attendees: Provide feedback regarding the choice between graph attributes and direct D-type/quantization attributes for the Attention OP.
- Yuan and Rama: Discuss offline the export work needed for RMSNorm and Rope operations.
- All Attendees: Review the Backend Context proposal document [link](https://docs.google.com/document/d/1rfXqd36HdIpxPrlYsyJMqxtHa1rR81bB3eTZKck_O20) and provide comments or additions.
- All Attendees: Consider the question of whether node duplication is a significant concern if weights can be shared, in the context of the Backend Context design.
