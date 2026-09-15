# Recording and Transcript:

https://zoom.us/rec/share/XxnVnxF-zBKENnRXFlZF0dlISQIrhJVXX-W98uyLuFN9oTmkEOJ-9hxrp2oMz8Fy.NzWKHjtQiBWjUs68

# Meeting Minutes:

- General Announcements & Release Management
  - The next ONNX release is planned in September.
  - Andreas noted that everything intended for the release needs to be merged beforehand; otherwise, it rolls over to the subsequent release (targeting a 3-month cadence).
  - The next release after September is planned for Q4 (around December). 

- Grouped Matrix Multiplication (Group MatMul) RFC
  - Status: Rama discussed about the Grouped MatMul [proposal](https://github.com/onnx/onnx/pull/8193) and discussed whether it can make the current release timeline.
  - Feedback:
    - Yamini checked internally with operators and NPU compiler teams and confirmed that it aligns with existing strategies.
    - A primary question was how Group MatMul will be exposed in ONNX models (e.g., pattern recognition/conversion via Torch ONNX export vs. model builder).
    - Rama clarified that supporting it via a model builder (like Mobius) is straightforward. While a torch exporter or ONNX script path is possible if there is broader interest, it is not currently prioritized.

- Grouped Query Attention (GQA) Operator
  - Javier gathered feedback regarding the GQA proposal from the ONNX Runtime (ORT) team.
  - A [PR](https://github.com/microsoft/onnxruntime/pull/32139) has been raised in ONNX Runtime to handle layout differences. If the preferred format swaps and (), a transpose is introduced to map back to the GQA definition.
  - The PR includes test cases to ensure the transpose is applied correctly without altering precision or accuracy. This is handled internally within ORT, requiring no changes to the ONNX spec. It also allows hardware execution providers (EPs) to identify the transpose and optimize it accordingly.

- Back-End Context / ORT Package Format Discussion 
  - Problem Statement Review: Javier revisited the problem statement framework, highlighting two primary use cases:
    - Just-In-Time (JIT) flow: Caching compiled models to mitigate long JIT compilation times.
    - Ahead-of-Time (AOT) flow: Applications shipping with pre-compiled caches, which requires target granularity descriptions and balancing performance against a proliferation of hardware permutations.
  - Weight Representation & Waitlist Compilation:
    - Discussed compiling models either with weights embedded or weightless (reusing original weights internally or externally).
    - Weightless compilation benefits include disk footprint reduction, smaller cache sizes, and sharing caches/weights across multiple hardware generations or vendor IPs.
  - Package Structure and Manifests:
    - The package format uses a directory structure with a manifest file to manage multiple model variants, model splits (e.g., pre-fill vs. decode for LLMs), and dependencies on original weights.
    - Compatibility Strings: Metadata generated during compilation that describes the target configuration. During local selection, execution providers query this string to validate and select the correct hardware variant to instantiate the inference session.
