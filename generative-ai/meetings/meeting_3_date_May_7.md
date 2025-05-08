# Recording and Transcript:

https://zoom.us/rec/share/wWuUfGL8Jm_MMMt5MvDsHsFresKX9wOd92rOzMDl37JYurkBkEYuI69l60lnHr2R.zLi6dzeGKL1hZ7u3

# Meeting Minutes:

## Operators:
- The group discussed operators from the [sheet](https://docs.google.com/spreadsheets/d/1JIykwXJEPT8FTLzvb0_5p_odvTYS9zzZjPNN33ziEbQ/edit?gid=0#gid=0) and assigned a priority to the operators. The operators that appear when models are exported are assigned P1 and operators from other pipeline elements are assigned P2.
- Yuan noted that while the existing attention operator in ONNX can cover most cases, it lacks support for quantization, mixed precision, and in-place key-value (KV) caching. He shared a [proposal](https://docs.google.com/document/d/1H-tYkH0DlxEMFafk7dKolNMcEf6Lpk1HOeL33u0bMlY) with the team for feedback.
- The group also discussed flex attention operator. Sahar highlighted the need to support user-defined functions (e.g., for score_mod and mask_mod), which the current ONNX spec doesn't directly support.
- Yuan and Rama proposed using graph-valued attributes to embed such custom computations as they can encode flexible logic like score_mod as subgraphs. This makes the op more general and extensible but requires more backend complexity and thoughtful model export design.
- Need to check if both mask_mod and score_mod are needed. Mask_mod offers performance benefits by skipping certain computations. However, it can be implemented within score_mod, so having both may be redundant functionally but useful for optimization.
- Yamini confirmed that ONNX supports nested functions, which can also be potentially used for modular computation inside attention ops. The group to further explore torch.export for flex attention and analyze the ops exported in torch fx graph.

## Backend representation:
- The group discussed backend-specific representation following the EPContext design. Rama suggested to have an interpretable graph instead of a black box blob.
- Yamini did a simple POC and showed an ONNX model with a ‘BackendContext’ function that points to compiled blob in the node attribute and stores the original subgraph. This is a more interpretable backend representation using a subgraph function and can include detailed backend-specific metadata
- However, this becomes complicated if we need to store multiple backend representations in the same graph and different backends support different subgraphs.
- The group discussed handling different quantization types and backend-specific scopes without storing redundant weights, suggesting solutions like scoping within a shared graph.
- Yamini to start a draft for the backend context framework and share with others to collaborate on the proposal.

## Exporters:
- Kshitij is working on an ONNX Script fix to ensure the attention module exports as a single attention op instead of a decomposed subgraph.
- Shubham confirmed it can be done by adding a rewrite rule for scaled_dot_product_attention and will coordinate with Kshitij.

## Others:
- Max suggested a better handling of KV Cache by enabling partial writes to I/O tensors using indexing or interleaved formats, to preserve ONNX's functional semantics.
- Rama suggested adding top-level graph annotations to mark input/output aliasing, allowing backends to optimize without altering internal graph structures. Aliasing should be made explicit, not inferred by backends, to ensure correctness—especially with more complex attention patterns.
- Max to document the ideas and share them with the working group for further deliberation and feedback.
- Yamini suggested forming another breakout workgroup in the future to discuss GenAI pipelines and ideas like above that may not be captured by existing breakout groups.






