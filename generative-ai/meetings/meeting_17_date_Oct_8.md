# Recording and Transcript:

https://zoom.us/rec/share/zwEQ42vW5FNRyEz23SK_zEPWbmxNRlHtozWcu7F7MWAVWg9qNLDBGsecQT9BoMRl.hsS8e3gRWsgl1RFX

# Meeting Minutes:

The primary topic is an RFC (https://github.com/onnx/onnx/issues/7301) introduced by Justin Chu regarding a proposal to represent equivalent or alternative graphs within a single ONNX model. This is related to the backend context discussion in the previous meetings.

- **Proposal Summary:** Justin explains the RFC's goal: to allow an ONNX model to store multiple, pre-compiled subgraph variations. This would enable different backends (like specific NPUs, GPUs, or CPUs) to select and execute the most efficient, pre-optimized version of a graph for their hardware. This proposal aims to solve the current problem where users must create and manage separate, non-standard ONNX files for each hardware target (e.g., an OpenVINO-optimized model, a TensorRT-optimized model, etc.). The new approach would allow for ahead-of-time (AOT) compilation while maintaining a single, portable, and standardized ONNX file.

- **Key Discussion Points:**
  - Rama clarified that the feature is for AOT optimization. A user could download a single model to a laptop, and the runtime could dynamically decide whether to use the pre-compiled NPU, GPU, or CPU graph based on the system's current load or power state.
  - The group debated how to specify which nodes to replace. Justin suggested a method of simply adding the new replacement node(s), rewiring the graph connections, and then running dead code elimination to remove the old, unused nodes.
  - Ti-Tai asked if this would slow down inference. Rama explained that the substitution logic would run during session creation (model load time), not during inference. This one-time setup cost is considered much cheaper than running full optimization passes every time the model is loaded.
  - Technical Challenges:
    - A potential issue was raised regarding the topological ordering of nodes. If an input to the new subgraph appears after an output in the original node list, the graph may need to be reordered, which Justin noted he hadn't fully considered.
    - Justin emphasized the need to keep the original graph unaltered and use namespacing so that backends that don't support this feature can still run the standard main graph.
  - Ti-Tai suggested a node-level approach where individual nodes could be flagged for specific backends. The group acknowledged this was also a possibility, likening it to "storing a diff" of multiple graphs within the file.
