# Recording and Transcript:

https://zoom.us/rec/share/eREfe2eWY-X81MownekfKAf0zz9i4K60oAHMKr4-m9vdQJuF6HjKUrxfck2zyfDk.57fMmZDObgZjyOT_

# Meeting Minutes:

## TensorScatter Operator for KV Cache Update

The primary topic was a Pull Request ([PR #7114](https://github.com/onnx/onnx/pull/7114)) by Yuan for a new operator, referred to as **`TensorScatter`**, designed to perform in-place updates to the KV cache.

* **Generic vs. Specific Design**: A major point of discussion, led by *Rama*, was whether the operator should be designed generically for any tensor update or specifically for the KV cache use case.
    * *Rama* suggested a more general and abstract operator. He reasoned that a generic tensor update/scatter operation could be useful in many other contexts. He suggested that making it too specific (e.g., hardcoding the update to the second-to-last axis) would limit its future utility. He proposed making it support N-dimensional tensors with a configurable `axis` attribute to specify the update dimension.
    * The group agreed that a generic operator with a generic name (like **`TensorScatter`** over `KvCacheUpdate`) was the preferable path to ensure future utility. *Yuan* will incorporate this feedback into the PR.

---

## Proposed Changes to the Attention Operator

The introduction of **`TensorScatter`** led to a discussion about necessary modifications to the existing **`Attention`** OP.

* **`kv_sequence_length` Input**: *Yuan* proposed adding a new optional input to the **`Attention`** OP called `kv_sequence_length`.
    * **Purpose**: Since the **`TensorScatter`** op passes a large buffer to **`Attention`**, this new input would be a 1D tensor (of size `batch_size`) that tells the operator how many tokens in the cache are actually valid for each sample. This allows for optimization by preventing the kernel from processing padded/invalid portions of the cache.
    * **Relationship to `attention_mask`**: The group discussed how this new input relates to the existing `attention_mask`. *Kunal Vaishnavi* noted that a similar approach in GQA (Grouped-Query Attention) initially removed the `attention_mask` but it had to be added back for flexibility. The consensus was that both `kv_sequence_length` and `attention_mask` should be supported as optional inputs, as they serve different purposes. `kv_sequence_length` is a compact way to handle simple causal masking, while `attention_mask` is required for more complex scenarios (e.g., speculative decoding, non-causal masks).

* **Composing `is_causal` and `attention_mask`**: *Rama* suggested that the `is_causal` attribute and the `attention_mask` input should not be mutually exclusive. He proposed that if both are provided, the final mask should be a composition of the two. This would simplify models exported from frameworks like PyTorch, which often generate large, explicit subgraphs to create a causal mask that is then combined with a user-provided mask.

* **Past/Present KV Inputs**: *Yuan* questioned whether the existing `past_kv` and `present_kv` inputs in the **`Attention`** OP should be removed now that **`TensorScatter`** provides an external mechanism for cache updates. *Rama* suggested that the **`TensorScatter`** logic could instead be integrated into the **`Attention`** op itself (making it a "bigger box"), which would maintain backward compatibility. The performance implications of splitting the logic into two ops versus keeping it as one were discussed but not resolved.

---

## Advanced KV Cache Management

*Yamini* raised the topic of more advanced cache management techniques, such as token eviction, where non-contiguous tokens might be removed from the cache to save space, and the remaining tokens are repacked.

* The group agreed that this introduces a level of state management that is likely outside the scope of the current **`Attention`** OP changes. It would require complex logic to decide which tokens to evict and could be handled by the runtime or with dedicated operators in the ONNX graph in the future.

---

## Timeline and Next Steps

*Yuan* noted that the proposed changes are substantial and that the upcoming opset 24 branch cut (in one week) is too soon to finalize the design and implementation. The group concluded that they would need to contact the release managers to make a case for extending the timeline to incorporate these features properly. The topics related to fusions in ONNX script and hosting GenAI interfaces code would be discussed in the next meeting.

---

## Action Items

* **Yuan**: Update the **`TensorScatter`** PR based on feedback to make the operator more generic.
* **Yuan**: Investigate updating the **`Attention`** op to allow the composition of the `is_causal` attribute and the `attention_mask` input.
* **Yuan/Rama/Yamini**: Contact *Andreas* to request an extension for the upcoming ONNX branch cut, as the current timeline is insufficient to finalize these changes.
* **All**: Continue the discussion on updating the **`Attention`** op definition to include the new optional `Kv_sequence_length` input.
* **All**: Follow up offline or continue the discussion to decide whether the **`TensorScatter`** logic should be integrated into the **`Attention`** op or remain a separate operator.
