# Recording and Transcript:
https://zoom.us/rec/share/R8EEh_TkRb-C42zOE9wDwKcirNQ2TJzPc7fHKX3QQ9OlRMw9qZr0ZgAk6Yzncy1b.K_GY1Im8Bnq5l0lc

# Quick Recap:
The team discussed standardizing GenAI interfaces to enable seamless switching between different backend stacks using ONNX models, reviewing a proof-of-concept (POC) demo by Ryan and Kshitij. Key proposals were made to update the Attention operator specification. The group also addressed implementation concerns regarding the proposed graph attributes feature, ultimately deciding to prioritize the in-place KV cache update PR before the upcoming code freeze and defer the graph attributes discussion to the next release cycle.

# Meeting Notes:

## GenAI Interface Standardization & Demo:
The group discussed standardizing GenAI interfaces and APIs to allow developers to easily switch between different backend frameworks (e.g., ONNX Runtime GenAI, OpenVINO GenAI, TensorRT etc.) while maintaining application logic.
- Goal: Create a seamless developer experience with high-level pipeline APIs, similar to Hugging Face Transformers, to improve adoption and accelerate time-to-market. The long-term plan is to align with APIs from platforms like OpenAI for agentic workflows.
- POC: Ryan demonstrated a POC using GenAI interfaces. It showed how a text-to-text pipeline could be conditionally compiled to work with different frameworks with only minor changes to headers and compilation flags.
- Proposal: The group agreed to propose hosting these standardized interfaces under the ONNX umbrella and will seek guidance from the steering committee on the best path forward.

## Proposed Updates to the Attention Op Spec:
Two updates to the Attention operator specification were proposed by Rama to better reflect common usage.
 - Combined Masks: The spec will be updated to allow both a user-provided attention mask and the causal mask attribute to be used simultaneously. This reflects a common pattern where both are combined in an "AND" operation.
 - QK MatMul Output Attribute: A special value (e.g., -1) will be added to the QK matmul output attribute to explicitly indicate that this optional intermediate tensor is not needed.

## Graph Attributes Implementation Challenges:
The team discussed the implementation complexity of adding graph attributes to the Attention op.
- Core Concern: The proposal includes 6 subgraph attributes and this creates a combinatorial explosion of possible configurations, making it impractical for backends to implement comprehensively.
- Conclusion: Given the complexity, the team decided to defer this feature. To prepare for future work, Yuan will collect and enumerate the most common, high-priority use cases (e.g., specific cast and QDQ patterns) to guide a more focused implementation. While subgraph attributes may be postponed as we gather more feedback on usage scenarios, Rama suggested that we could target kv cache update for the upcoming release
- PRs: Yuan shared the below PRs that are currently open and requested feedback on:
- Attention subgraph attributes: https://github.com/onnx/onnx/pull/7090
- TensorScatter for in place kv update: https://github.com/onnx/onnx/pull/7114
- Follow up from Yuan: Yuan shared a list of common quantization/precision patterns for Attention to evaluate the use of subgraph attributes as a follow up in the GenAI operators slack. The tables on this page do a pretty good job summarizing it. The most important piece we are missing in Attention-23 would be the Q/DQ before BMM2

## Rotary Embedding & In-Place KV Cache:
The team confirmed that the planned in-place KV cache updates would not negatively impact the rotary embedding operation. For standard use cases, the op is compatible, and for more advanced scenarios, any required changes are considered manageable.

## Action Items:
- Ryan and Kshitij to host the GenAI interface examples publicly for feedback.
- Yamini to bring the GenAI interface proposal to the steering committee for guidance on where to host the interfaces.
- Yamini to discuss the GenAI interface demo with the ORT GenAI team.
- Yuan to update the attention op spec to allow both explicit mask input and causal mask attribute to be used simultaneously.
- Rama to add a special value (e.g., -1) to the QK_MATML_OUTPUT attribute in the attention op spec to indicate no output is required.
- Yuan to collect and enumerate common use cases for graph attributes in the attention op, focusing on cast and quantization scenarios - Done (see details above)
- Rama to review and address CI test failures in the inliner PR: https://github.com/onnx/onnx/pull/7112
- All to review PR for in-place KV cache updates: https://github.com/onnx/onnx/pull/7114
