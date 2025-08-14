# Recording and Transcript:

https://zoom.us/rec/share/1zMxy_nRfIiWr4N7mEu0lsgJ_d1HANXjngMUFrAd_WYWk8HCzIUal_bsoOsFNBY_.gviYqqrVmJtjCzYe

# Meeting Minutes:

## Paged Attention Support in ONNX 

The group discussed whether ONNX should provide explicit support for paged attention, a memory management technique for the KV cache popularized by frameworks like vLLM.

* **Core Question**: The group debated whether paged attention is an implementation detail best handled by backends or if it requires a new ONNX operator.

* **Technical Details**: Paged attention relates to KV cache management (using non-contiguous memory blocks) and is distinct from compute-focused optimizations like FlashAttention. The current ONNX approach involves passing the KV cache as a graph input/output, which can be updated in place using the new `TensorScatter` op.

* **Current State**: The consensus was that paged attention is a deployment-time optimization applied by engines like vLLM to PyTorch models. There are currently no known ONNX models that inherently use a paged attention operator. It was noted that this is similar to how tensor strides are handled—a backend implementation choice that doesn't require a change to the ONNX spec itself.

* **Next Steps**: The group will conduct further research into how paged attention is implemented in PyTorch and vLLM to determine if any standardization is needed within ONNX.

---

## Mixture of Experts (MoE) Operator 

A proposal was made to standardize a Mixture of Experts (MoE) operator in ONNX, noting its growing popularity (e.g., recent GPT models) and the benefits it would provide for tools like OpenVINO.

* **Problem**: While MoE logic can be constructed from existing ONNX operators, it results in large, complex, and repetitive subgraphs. A single MoE operator would greatly simplify the model graph.

* **Proposed Solution**: It was suggested that MoE be defined as a **function op**. This approach has a lower barrier to entry than a primitive operator and allows backends to either use the function's definition or provide their own highly optimized implementation.

* **Challenges**: MoE implementations vary significantly between models, which can cause challenges for exporters, often leading to data-dependent shape errors. Creating a single, unified op that covers all variants will be difficult.

* **Next Steps**: The group will explore creating an MoE function op, using the existing [contrib MoE op](https://github.com/microsoft/onnxruntime/blob/main/docs/ContribOperators.md#com.microsoft.MoE) in ONNX Runtime as a potential starting point.

---

## Opset 24 and Attention Updates 

An update was provided on the upcoming ONNX 1.19 release, which will include **Opset 24**.

* **Key Features**:
    * The `TensorScatter` op will be included for efficient KV cache management.
    * This enables native representation of **linear and circular buffer attention**.
    * [New documentation](https://github.com/onnx/onnx/blob/main/docs/docsgen/source/technical/kv_cache.md) detailing these features will be available.

* **Open Topic**: A standardized method for representing quantization within the attention operator is still under discussion and is not included in this release.

* **Outreach**: A suggestion was made to create a blog post or social media announcement to ensure the broader community is aware of these significant updates.

---

## Standardizing GenAI Pipelines 

An update was requested on the initiative to standardize end-to-end GenAI pipelines in ONNX.

* **Status Update**: The proof-of-concept (POC) for a **text-to-text pipeline** has been merged into the working group's GitHub repository ([link](https://github.com/onnx/working-groups/tree/main/generative-ai/genai-interfaces)). The initiative has received positive feedback from the working group.

* **Community Feedback**: To gather wider input, the group will create a short write-up and seek feedback from the community on Slack and other channels.
