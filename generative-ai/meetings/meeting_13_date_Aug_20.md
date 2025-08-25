# Recording and Transcript:

https://zoom.us/rec/share/No2Z-ycx2-wbex9-W_B1A4jITcM6KX-FoZS_dXcqC7Wwq_YaqroVFz678bk8gB3C.K3CjXN6l2LOtAM27

# Meeting Minutes:

## Paged Attention
- The group discussed standardizing Paged Attention. Initially thought to be a backend-only optimization, it was clarified that Paged Attention fundamentally changes a model's input/output structure, requiring new inputs like block_tables. This makes it more than a simple implementation change.
- The current thinking in ONNX Runtime (ORT) is to create new ONNX models with a dedicated Paged Attention operator, as transforming existing models on the fly is complex. The discussion also touched on whether the block_table should be managed by the user or the backend.
- **Action Item:** The group will investigate this further. Kunal Vaishnavi shared a [draft pull request for paged attention models](https://github.com/microsoft/onnxruntime-genai/pull/1605) and links to the [operator's definition](https://github.com/microsoft/onnxruntime/blob/b0d4f005e6f94929f3d8a2a735768ae7d0977627/onnxruntime/core/graph/contrib_ops/bert_defs.cc#L1258) for reference

## Mixture of Experts (MOE)
- The team addressed the need for a standardized Mixture of Experts (MOE) function operator in ONNX. It was noted that many different MOE implementations exist across various models (e.g., Mixtral, Phi).
- The current ORT contrib op for MOE handles these variations by adding numerous attributes, which is not an ideal long-term solution. To illustrate this complexity, Kunal shared a link to an [ORT unit test file](https://github.com/microsoft/onnxruntime/blob/main/onnxruntime/test/python/transformers/test_moe_cuda.py) showing the different variations.
- The group considered creating a more flexible base op, possibly using subgraphs or functions similar to the proposed Flex Attention.
- **Action Item:** Kunal Vaishnavi will research the various implementations and propose a starting point for a base ONNX MOE operator.

## Community Feedback
Yamini Nimmagadda proposed creating a formal channel for broader community feedback on proposed changes to the ONNX standard. The group agreed that using GitHub Discussions within the ONNX repository would be a good platform to post topics and gather input, which can then be promoted through other channels like LinkedIn.

## Backend Context & Pre-compilation
- Yamini presented a proposal for embedding pre-compiled backend-specific objects ("blobs") into ONNX models to reduce compilation times for Large Language Models (LLMs).
- The key goals are to include these optimized blobs while retaining the original ONNX subgraph as a fallback and to support multiple backends (CPU, GPU, NPU) within a single model container.
- Two potential implementation options were discussed:
  - Function-based: A BackendContext function operator, similar to the existing EPContext.
  - Metadata-based: Using Scope annotations in the model's metadata to define which parts of the graph are targeted by specific backends.
- The discussion highlighted the complexity of handling multiple device configurations (e.g., CPU+NPU vs. CPU-only) and the trade-offs of weight sharing between different pre-compiled blobs.
-	Next Steps: The group will start by exploring simpler use cases. Yamini shared the [presentation link](https://docs.google.com/presentation/d/1oPgfK2qvuYsOa4_eT0bsiwV96eI66rsH) and Rama will gather more feedback from internal teams at Microsoft.
