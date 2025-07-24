# Recording and Transcript:

https://zoom.us/rec/share/zVDPlDe9YNy4yeFFs5zJvTLedkhHpFXR8Glo1gTaKTn84sNZbAaL8r0VaicsN94G.xa1NagznolIvXUSv

# Meeting Minutes:

## ONNX 1.19 Release & Operator Updates

### ONNX 1.19 Release Planning

The team discussed pending Pull Requests (PRs) for the upcoming ONNX 1.19 release.  
**Branch cut is scheduled for next Thursday.**

### TensorScatter Operator

**Status:** TensorScatter PR from Yuan is currently under review.


#### Motivation
Yuan explained the need for a specialized `TensorScatter` operator versus reusing existing scatter ops:
- **Simplified indices input**: Reduces index dimensions (e.g., only batch indices), avoiding verbose per-head/token indices.
- **Optimization signal**: Clearly communicates intent for **in-place KV cache updates**, enabling I/O tensor aliasing and backend optimization.

#### Next Steps
- Yuan will address **review comments** from Christian.
- The operator’s **description will be enhanced** for clarity.
- For the reference implementation, **readability will be prioritized** over vectorization.

**PR Link:** [Add TensorScatter operator](https://github.com/onnx/onnx/pull/5677)

### Attention Operator Update

After the TensorScatter PR is merged, Yuan will submit a **follow-up PR** to:
- Add an **optional `kv_sequence_length` input** to the Attention OP.
- This will enable models to **specify the number of valid tokens** in each sample of the KV cache buffer—important for kernel optimization.

**Note:** The current concat-based cache logic in Attention will remain to **keep the update minimal** for this release.

### Fusion Support: RMSNormalization & RotaryEmbedding

#### Overview
- Infrastructure is now available in **onnxscript** to detect and fuse common subgraphs into:
  - `RMSNormalization`
  - `RotaryEmbedding`

#### Fusion Details
- These fusions apply **automatically** when exporting with **opset ≥ 23**.
- Prevents large graph expansions during export (e.g., with Hugging Face models).
- Fusions currently only work on ONNX graphs **exported via TorchDynamo**.

#### PR Links:  
- [RMSNorm Fusion PR](https://github.com/microsoft/onnxscript/pull/1156)  
- [RotaryEmbedding Fusion PR](https://github.com/microsoft/onnxscript/pull/1157)

### Hosting for Generative AI Interfaces Code

- The ONNX Steering Committee has **approved hosting preview code** in the [`onnx/working-groups`](https://github.com/onnx/working-groups) repository.
- This allows for **iterative feedback** and code maturity.
- Once stable, the code may move to a **dedicated ONNX repo**.
- Yamini has created a **[draft PR](https://github.com/onnx/working-groups/pull/206)** to add the initial interface code.

## Action Items

| Owner     | Action                                                                                             |
|-----------|----------------------------------------------------------------------------------------------------|
| **Yuan**  | Address review comments on [TensorScatter PR](https://github.com/onnx/onnx/pull/5677). Submit follow-up PR for Attention OP `kv_sequence_length`. |
| **All**   | Test fusions for [RMSNormalization](https://github.com/microsoft/onnxscript/pull/1156) and [RotaryEmbedding](https://github.com/microsoft/onnxscript/pull/1157). Report any cases where fusion does not trigger correctly. |

