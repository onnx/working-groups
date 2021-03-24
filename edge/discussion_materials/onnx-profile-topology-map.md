<!--- SPDX-License-Identifier: Apache-2.0 -->

# ONNX Profile Topology Map
Author: Milan Oljaca, Ofer Rosenberg, Yedong Liu, Saurabh Tangri

Version: 0.1

## Introduction

This document defines a hierarchical classification of ONNX edge profiles, i.e. a profile topology map.
Intent with such profile breakdown is to establish categorization of edge profiles based on use cases and profile attributes identified in [onnx-edge-scope-and-profile-definition.md](https://github.com/onnx/working-groups/blob/master/edge/artifacts/onnx-edge-scope-and-profile-definition.md) document.

## Profile topology

Top level categories are identified as per [Scope of Edge.png](https://github.com/onnx/working-groups/blob/master/edge/artifacts/Scope%20of%20Edge.png).

### Edge Infrastructure
Considering edge infrastructure deployment aspects, e.g. stationary and wall-powered, the profile attributes of most relevance are accuracy and latency.

#### Basic 2D Image profile
Use cases: Computer Vison - Image Classification, Object Detection, Semantic Segmentation
Models: Mobilenet, MobilenetSSD, Enet?
Capability: Basic (e.g. meets top-5 accuracy, <= 15fps latency, input resolution <= 480p, ... )

#### Advanced 2D Image Profile
Use cases: Computer Vison - Image Classification, Object Detection, Semantic Segmentation
Models: ....
Capability: Advanced (e.g. meets top-1 accuracy, <= 30fps latency, input resolution >= 1080p, ... )


#### Basic Audio Profile
Use cases: ASR
Models: ....
Capability: Basic (e.g. .... )

#### Advanced Audio Profile
Use cases: NLP, Translation
Models: ....
Capability: Advanced (e.g.  .... )


### Edge Devices
Considering edge devices' deployment aspects, two sub-categoriese are considered:
* Mobile (battery powered): profile attributes of most relevance are power consumption and size.
* Stationary (wall-powered): profile attributes of most relevance are accuracy, latency and size.

#### Basic 2D Image profile
Use cases: Computer Vison - Image Classification, Object Detection, Semantic Segmentation
Models: ....
Capability: Basic (e.g. meets top-5 accuracy, <= ??fps latency, input resolution <= ??, ... )
Subtype: Data Locality: Yes or No

#### Advanced 2D Image Profile
Use cases: Computer Vison - Image Classification, Object Detection, Semantic Segmentation
Models: ....
Capability: Advanced (e.g. meets top-1 accuracy, <= 30fps latency, input resolution >= 1080p, ... )
Subtype: Data Locality: Yes or No

#### Basic Audio Profile
Use cases: ASR
Models: ....
Capability: Basic (e.g. )
Subtype: Data Locality: Yes or No

#### Advanced Audio Profile
Use cases: NLP, Translation
Models: ....
Capability: Advanced (e.g. )
Subtype: Data Locality: Yes or No


## NOTES
* Accuracy could be mAP based as per selected reference models in the profile.
  * E.g. Basic profiles will have simpler models but lower accuracy.

* Possible more formal profile naming convention to consider, more future proof. E.g.
  * 2D Image: Class A1 Profile ( = Advanced, data locality=yes)
  * 2D Image: Class A2 Profile ( = Advanced, data locality=no)
  * 2D Image: Class B1 Profile ( = Basic, data locality=yes)
  * 2D Image: Class B2 Profile ( = Basic, data locality=no)
  * 2D Image: Class B3 Profile ( = Basic, some future bounds go here: e.g. same as B1 but not more then 1% mAP drop )


