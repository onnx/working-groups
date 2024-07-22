<!--- SPDX-License-Identifier: Apache-2.0 -->

# ONNX Safety-Related Profile Working Group (WG)

This repository is where ONNX Safety-Related Profile WG will capture various artifacts and deliverables. 

The purpose of this WG is to elaborate an ONNX profile dedicated to safety-related systems.

An ONNX model is the representation of an ML/AI model to be implemented. In other words, it is the specification for the implementation activity. 
The model may be either interpreted by a tool or translated into some lower level equivalent representation (e.g., some source code) by a tool or a human.  In both cases, to be able to interpret the model according to the intent of its designer, its syntax and semantics must be clear and non-ambiguous. 
This requirement is applicable to any system, but it is critical for systems for which a failure may have a critical business or safety impact.
This is for instance the case in the aeronautical domain for which evidences shall be provided to show that the model semantics is actually preserved throughout the implementation phase (see ARP 6983, "Process Standard for Development and Certification/Approval of Aeronautical Safety-related Products implementing AI").
We consider that the current ONNX standard does not fully satisfy these requirements and that there is a need (i) to clarify the industrial needs in that matter, (ii) to identify and address the weaknesses of the current standard in a systematic manner in order to produce an "safety-related ONNX profile" that would to fulfil these needs.
We also consider that these needs are specific and that the proposed changes and clarifications of the syntax, semantics, and documentation shall not prevent the use of ONNX in domains where constraints are relaxed. For instance, introducing restrictions on the parameters values for operators of the safety-related profile must not affect the usage of the same operators out of the profile. 

## Working Group Status
**ACTIVE**

# Slack channel
Please sign up at https://slack.lfai.foundation/ and join [onnx-srp](to be completed) channel.

# WG Lead(s)

* Eric JENN (IRT Saint-Exupery) and Jean SOUYRIS (Airbus) (July 22, 2024 - Current)

# Logistics

* WG leads will drive the meeting.
* Meeting annoucement will be posted in our Slack channel: https://lfaifoundation.slack.com/archives/C02AANGFBJB
* Feedbacks and topic request are welcome by all.
* Documents and artifacts: https://github.com/onnx/working-groups/tree/main/safety-related-profile

# WG Meeting Info

* Meeting (to be defined).
* TEAMS Meeting link: (to be defined)
* Meeting ID: (to be defined)

# Meeting notes

The meeting notes can be found [here](https://github.com/onnx/working-groups/tree/main/safety-related-profile/meetings)
