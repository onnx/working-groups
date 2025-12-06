# Recording and Transcript:

https://zoom.us/rec/share/_9Hfc3qBUVm0RPLyop2UAVNwpVjiN_yeW3bV-gypAry4-3poZttL9o4zt7T-zVyo.pmYDduHKbNQhPYxr

# Meeting Minutes:

## FlexAttention Operator Contributions
- Issue: Yamini raised a [GitHub issue](https://github.com/onnx/onnx/issues/7494) seeking community contributions for FlexAttention in ONNX. No active responses have been received yet.
- Resolution: Yuan suggested cross posting the request to the general ONNX Slack channel (rather than just the GenAI channel) to increase visibility. Yamini agreed to this action.

## GenAI Interface Proposal
Freddy Chiu presented a [proposal](https://docs.google.com/presentation/d/1yPvLV5PzNv54M-oCRy6rWnRtA84EYKhT) as a follow-up to the previous ONNX GenAI interfaces proposal to address the fragmentation in GenAI deployment stacks
- Problem Statement: Developers currently face a steep learning curve and lack of interoperability when switching between different C++ stacks for GenAI.
- Proposed Solution: A standardized, framework-independent, and platform-independent API for GenAI.
  - Goal: Provide a consistent application interface (similar to how ONNX standardized inference) allowing developers to write business logic once while swapping hardware backends dynamically.
  - Current Status: [POCs](https://github.com/onnx/working-groups/tree/main/generative-ai/genai-interfaces) were created in August/September demonstrating end-to-end usage for text-to-text and text-to-image workflows.
- Proposed Roadmap:
  - Immediate: Formalize definitions into an "Alpha" release with samples to gather community feedback by Q1 2026.
  - Future: Move to Beta, with a targeted formal release in Q3 2026.
 
## Technical Feedback & Debate
Yuan provided feedback regarding the feasibility of a unified interface across divergent backends.
- Export vs. Builder Divergence: Yuan noted that ONNX Runtime (ORT) GenAI currently uses a "Model Builder" approach with custom ops, whereas other backends rely on standard ONNX export.
  - Response: Yamini clarified that the goal is to converge on a common export path directly from Transformers, enabling the use of a shared model format while allowing backends to implement pipeline-level optimizations (e.g., paged attention, continuous batching) under the hood.
- C++ vs. Python: Yuan pointed out that Data Center users overwhelmingly prefer Python/PyTorch and may resist a C++ interface. He noted that even TensorRT LLM is pivoting toward native PyTorch integration.
  - Response: Freddy acknowledged this but emphasized that the primary target for this proposal is the Client/Edge PC ecosystem. Unlike the Data Center, the client space has non-homogeneous hardware; a unified C++ API solves the complexity of deploying a single application across different NPU vendors.

## Actions from the community: 
- Check the [GitHub issue](https://github.com/onnx/onnx/issues/7494) on FlexAttention implementation and leave a comment if you would like to contribute
- Review the [proposal](https://docs.google.com/presentation/d/1yPvLV5PzNv54M-oCRy6rWnRtA84EYKh) on GenAI interfaces and share your feedback or let us know if you would like to contribute
