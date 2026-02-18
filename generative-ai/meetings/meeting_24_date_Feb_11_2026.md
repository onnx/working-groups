# Recording and Transcript:

https://zoom.us/rec/share/12qRi-qJkMsAz4c37Gb-5Cxjit030JFNylsEhkEbp1AAsqTHormMY8jE5skXNVzk.DMaRIM-8Xs3GqhQ-

# Meeting Minutes:

## Ternary Storage Proposal

- Yamini opened the meeting by discussing the ternary storage proposal ([paper](https://drive.google.com/file/d/1oeHVpCygJ9XlWKChB5e1tCWVFil9j9gY/view?usp=drive_link), [presentation](https://drive.google.com/file/d/1ofjAkMWh0XEXm2WauN1CLSwNF49kpMwb/view?usp=drive_link)) from Soumendu.
- Rama emphasized following the same procedure used for 4-bit and 2-bit quantized types to ensure a standardized representation.
- Soumendu to convert the existing document into a Markdown RFC using the [official template](https://github.com/onnx/onnx/pull/7594) and submit it as a Pull Request (PR) in the proposals folder for community visibility.


## Optimum ONNX Analysis (Xavier Dupré)
- Xavier presented the challenges and future directions for exporting models to ONNX, specifically focusing on Large Language Models (LLMs) and the transition to the Dynamo Exporter ([Link](https://github.com/onnx/working-groups/blob/main/generative-ai/meetings/optimum-onnx-discussion.pdf) to the proposal).
- Key Challenges Identified:
  - Export Complexity: Hugging Face pipelines do not provide a direct forward method, making it difficult to guess inputs and dynamic shapes.
  - Cache Management: The nested structure of caches needs constant flattening and unflattening, which is prone to breaking as Transformers versions update.
  - Control Flow: The new Dynamo exporter is sensitive to control flows (if/else) that depend on shape or content, requiring significant code rewriting.
  - Maintenance: "Patching the patches" across multiple repositories (Transformers, Optimum, Optimum ONNX) is not sustainable.
- New approach with "Observers":
	Xavier introduced a new Observer-based approach to simplify the export process:
  - Mechanism: An observer stores inputs sent to the forward method during a typical run (e.g., calling a pipeline). It then automatically infers the largest set of inputs and dynamic shapes.
  - Benefits: This removes the need for manual dynamic axis declarations and heavy "ORT Model" wrapper classes.
  - Status: Xavier has a working PR for LLMs like Llama and Whisper.
- Future Strategy (Proposals)
	Xavier outlined three potential paths forward:
  - Proposal 1: Keep everything as-is and extend as needed (doable but inefficient)
  - Proposal 2: Keep Optimum ONNX API for backward compatibility but use the new "Observer" stack for new models (preferred as scalable solution)
  - Proposal 3: Move patches elsewhere (Olive, ONNX Runtime) and keep Optimum ONNX only for the old exporter (Misses out HF optimum developer ecosystem)

## Next Steps
- Hugging Face Collaboration: Yamini and Muthaiah will facilitate a connection between Xavier and the Hugging Face team to review the proposals and align on the new architecture.
- Technical Deep-Dive: Xavier shared the [link](https://github.com/pytorch/pytorch/blob/main/torch/onnx/_internal/exporter/_input_observer.py) to observers code for the team to review the implementation details.
- Ternary Storage: Yamini to follow up with Soumendu regarding the RFC conversion.
