<!--- SPDX-License-Identifier: Apache-2.0 -->

﻿# ONNX Edge Working Group SoW

## Purpose
As the use of ONNX become more pervasive, running ONNX-based models on a wider set of platforms is required. A growing class of these platforms is “edge devices”, which due to their nature may have some constraints. The Edge working group will explore the implications of these constraints on various ONNX aspects, and provide recommendations to the SIGs.

## Scope
Promote the usage of ONNX on edge devices by actively working with various ONNX SIGs, and working groups to ensure compatibility and introduce features relevant to execution in this domain, creating a complete end to end specification for edge devices in ONNX.

Identify the scenarios/use-cases which are applicable for edge devices, translated into definition of edge device profiles.

Promote ONNX compliance for edge devices via defining a subset of ONNX operations, data representation and accuracy metrics which applies to edge devices profiles. Selected ONNX operations will maintain the semantics across ONNX targets.
Suggest compliance tests covering edge profiles by validation of tested models using golden references and adequate comparisons.

Examine collaboration with [MLPerf organization](https://mlperf.org/) and their Edge inference WG on aligning terminology and defined ops subset / data representation / accuracy metrics, to streamline the use of ONNX models as MLPerf inputs to benchmarking. Consider collaboration with other performance-focused benchmarks/organizations (TPC, AIBench, others) for promoting ONNX as input models.

## Collaboration
The edge WG will collaborate with the following ONNX groups:
* Operators SIG (in context of quantization)
* Model Zoo SIG
* Architecture/Infrastructure SIG (in context of compliance)

The WG should avoid overlapping work with the mentioned WGs and SIGs.

## Organization
ONNX Edge is one of ONNX working groups.
The working group will gather requirements, deliver documentation and required material into the [edge directory under the working-group repository](https://github.com/onnx/working-groups/tree/master/edge).
The working group will use a dedicated [gitter room channel](https://gitter.im/onnx/edge).
In addition, it will hold periodic meetings which are open to any active contributor of ONNX. Notification of the meeting and agenda will be published on the gitter channel a few days prior to the meeting. Meetings will be recorded and published.
The organization and logistics information will be maintained in [edge working group README.md](https://github.com/onnx/working-groups/blob/master/edge/README.md).
Recommendations of the working group will be delivered to the relevant SIGs.

## Deliverables
### Documents
1. Definition of "Edge" scope, encompassing infrastructure edge, IoT devices, Mobile devices and more ( e.g. !Cloud ;-) )
2. Definition of a "edge profile":
   1. Attributes / characteristics: Power, Compute resources, Size, Connectivity, Security, …
   1. ONNX operations subset
   1. Other ONNX related limitations
3. Definition of specific profiles covered by the Edge working group: e.g. Mobile Profile, Smart-Device Profile, Infra-Edge profile, etc.
4. Collaborate with Quantization working group to define the following:
   1. Data types
   1. Representation of quantization parameters in the model
   1. Set of quantized operations
   1. Accuracy impact of quantization on set of defined models/use-cases
5. Collaborate with ModelZoo and Operator Standardization SIGs to define the following:
   1. Define compliance workflow
   1. Define content of test packages for Edge "profiles"

### Code
1. TBD. This is dependent on interaction with other WGs and SIGs. For example, possible code contribution to compliance suite for Edge profiles.

## Goals and Milestones
### 2019Q2
* SoW approved by steering committee.
* Documents 1. and 2. as described in Deliverables section.
### 2019Q3
* Document 3. as described in Deliverables section.
### 2019Q4
* Documents covered under items 4. and 5. as described in Deliverables section.

## Exit Criteria
1. Create a document describing an ONNX profile in terms of : what it covers, what it defines (ops set, data types), what are the differentiating criteria, etc.
2. Create a document which describes the profile/s covered by the edge working group, including the defined operation and data types subsets for each.
3. Create a document in collaboration with the quantization working group to define quantization on edge devices - supported types, how quantization is expressed in the model, expected accuracy difference from floating-point implementation.
4. Define a set of use cases (scenarios) which is applicable to the profiles defined by the working group.
5. For each use case, provide a defined test including a model, acceptable accuracy.
