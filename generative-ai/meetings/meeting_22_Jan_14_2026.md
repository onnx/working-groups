# Recording and Transcript:

https://zoom.us/rec/share/O77VTbYJPR6hObo4_dJgWXcfo-y6PZoGtxSHblrJdY2ZGGTLnbbjbX8NfQAVuQ5y.Slg75HZun6F9E458

# Meeting Minutes:

## Summary
The meeting focused on three primary technical areas: reviewing an open-source contribution for flex-attention, debating the long-term infrastructure for LLM model exports, and introducing a proposal for a standardized ternary storage format to optimize LLM inference.

## Key Discussion Points

### Flex-Attention Contribution
- A comprehensive open-source contribution for flex-attention was submitted via GitHub [PR link](https://github.com/onnx/onnx/pull/7534) with numerous test cases.
- WG members are requested to review the PR before the next meeting for further discussion.
- The team noted that the primary challenge moving forward will be the backend implementation. They plan to discuss how to include this in upcoming versions and its integration with the exporter.
  
### LLM Model Export Paths
- There is a discussion whether to focus on Optimum ONNX or Olive as the primary path for exporting Large Language Models (LLMs) at scale.
- Intel has been using Optimum Intel and is considering integrating their quantization tool (NNCF) into Optimum ONNX to provide a consistent experience for users. Since Olive contains Optimum pass, the same integration can be used via Olive.
- Rama explained that Microsoft’s main area of investment is the PyTorch-to-ONNX exporter. Exporter-related issues in Optimum-ONNX will be supported by the exporter team, though Olive remains Microsoft’s recommended solution.
- Freddy raised concerns about "model variation," suggesting the need for architectural guidelines to ensure exported models remain reusable and semantically equivalent across different tools.

### Ternary Storage Format Proposal
- Soumendu introduced a proposal for a standardized storage format for Ternary LLMs (weights represented as -1, 0, 1).
- By using a 2-bit (or 10:8) compression scheme, memory traffic between DRAM and on-chip SRAM can be reduced by approximately 20%. This significantly improves power efficiency and performance during the memory-bound decoding phase (token generation).
- A formal draft of this data-independent compression scheme will be shared for review before the next meeting.

## Action Items
- All:  Review the flex-attention GitHub [PR](https://github.com/onnx/onnx/pull/7534) and provide feedback.
- Yamini: Share the list of missing ORT classes from optimum-onnx in Slack for the ONNX exporter team to review.
- Soumendu: Share the draft proposal for the Ternary Storage Format
- Yamini & Rama: Finalize a new recurring meeting time (potentially 10:30 AM) to avoid conflicts.
- Justin: Provide updates on the RFC system for tracking proposals.

## Comparison between Auto and ORT model classes in Optimum (As of 1/23/2026):

| Task                                     | Auto Class                              | ORT Class                              |
| ---------------------------------------- | --------------------------------------- | -------------------------------------- |
| audio-classification                     | AutoModelForAudioClassification         | ORTModelForAudioClassification         |
| audio-frame-classification               | AutoModelForAudioFrameClassification    | ORTModelForAudioFrameClassification    |
| audio-xvector                            | AutoModelForAudioXVector                | ORTModelForAudioXVector                |
| automatic-speech-recognition             | AutoModelForSpeechSeq2Seq               | **Missing**                            |
| automatic-speech-recognition             | AutoModelForCTC                         | ORTModelForCTC                         |
| depth-estimation                         | AutoModelForDepthEstimation             | **Missing**                            |
| feature-extraction                       | AutoModel                               | ORTModel                               |
| feature-extraction / sentence-similarity | SentenceTransformer                     | **Missing**                            |
| fill-mask                                | AutoModelForMaskedLM                    | ORTModelForMaskedLM                    |
| image-classification                     | AutoModelForImageClassification         | ORTModelForImageClassification         |
| image-text-to-text                       | AutoModelForImageTextToText             | **Missing**                            |
| image-to-image                           | AutoModelForImageToImage                | ORTModelForImageToImage                |
| image-to-image                           | AutoPipelineForImage2Image              | ORTPipelineForImage2Image              |
| image-to-text                            | AutoModelForVision2Seq                  | ORTModelForVision2Seq                  |
| inpainting                               | AutoPipelineForInpainting               | ORTPipelineForInpainting               |
| masked-im                                | AutoModelForMaskedImageModeling         | **Missing**                            |
| multiple-choice                          | AutoModelForMultipleChoice              | ORTModelForMultipleChoice              |
| object-detection                         | AutoModelForObjectDetection             | **Missing**                            |
| question-answering                       | AutoModelForQuestionAnswering           | ORTModelForQuestionAnswering           |
| semantic-segmentation                    | AutoModelForSemanticSegmentation        | ORTModelForSemanticSegmentation        |
| text2text-generation                     | AutoModelForSeq2SeqLM                   | ORTModelForSeq2SeqLM                   |
| text-classification                      | AutoModelForSequenceClassification      | ORTModelForSequenceClassification      |
| text-generation                          | AutoModelForCausalLM                    | ORTModelForCausalLM                    |
| text-to-audio                            | AutoModelForTextToSpectrogram           | **Missing**                            |
| text-to-audio                            | AutoModelForTextToWaveform              | **Missing**                            |
| text-to-image                            | AutoPipelineForText2Image               | ORTPipelineForText2Image               |
| token-classification                     | AutoModelForTokenClassification         | ORTModelForTokenClassification         |
| visual-question-answering                | AutoModelForVisualQuestionAnswering     | **Missing**                            |
| zero-shot-image-classification           | AutoModelForZeroShotImageClassification | ORTModelForZeroShotImageClassification |
| zero-shot-object-detection               | AutoModelForZeroShotObjectDetection     | **Missing**                            |

