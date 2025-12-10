<!--- SPDX-License-Identifier: Apache-2.0 -->

# ONNX Generative AI Working Group (WG)

This repository is where the ONNX Generative AI (GenAI) WG will capture various artifacts and deliverables.

## Objective

As discussed in the ONNX steering committee meeting on 4/2/2025 ([meeting minutes](https://github.com/onnx/steering-committee/blob/main/meeting-notes/2025/20250402.md#growing-onnx-with-evolving-needs)), we are establishing this working group to address the evolving needs of ONNX to support Generative AI. The scope of this working group includes, but not limited to:

### ONNX Functions and Operators

- Propose new decomposable ONNX functions
- New Metadata required to describe device specific graphs or Function groupings.
- Reference implementations for the proposed ONNX functions
- Standardize popular GenAI operations in ONNX to reduce the usage of contrib ops
- Define methods/scripts for converting existing models to leverage newly defined ONNX operators and functions
- Ensure that the framework converters are updated to export the ONNX models with newly defined operators 

### Generative AI Pipelines

- Define GenAI pipelines for end-to-end execution of GenAI ONNX models
- Standardize high-level APIs that can be integrated into applications for usages like text generation, image generation
- Define interfaces for vendors to plug in their optimized implementations for GenAI pipelines
- Define pipeline constructs to enable seamless development of new pipelines
- Provide pipeline optimizations including decoding strategies, kv cache management, efficient parallelism and batching techniques 
- Explore constructs needed for building Agentic and reasoning workflows

## Working Group Status
**ACTIVE**

# Slack channel
https://lfaifoundation.slack.com/archives/C08MERYU84T

# WG Lead(s)

* Yamini Nimmagadda (Intel)
* Ramakrishna Sivakumar (AMD)

# Logistics

* WG leads will drive the meeting.
* Meeting annoucements will be posted in our Slack channel: https://lfaifoundation.slack.com/archives/C08MERYU84T
* Feedbacks and topic requests are welcome from everyone.
* Documents and artifacts: https://github.com/onnx/working-groups/tree/main/generative-ai 

# Meeting notes

The meeting notes can be found [here](https://github.com/onnx/working-groups/tree/main/generative-ai/meetings)
