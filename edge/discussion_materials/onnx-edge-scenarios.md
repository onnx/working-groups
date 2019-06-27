# ONNX Edge Scenario Analysis Document
Author: Yedong Liu, Zhipeng Huang

## Introduction

Edge computing is coming. While we can benefit from the excellent interoperability of ONNX to be framework-agnostic, some issues critical for running ONNX model in an edge/mobile/IoT device still remains, therefore we gather here to discuss and try to solve these issues.

One part we want to include is the ONNX Runtime for Edge, we propose ONNX Runtime for Edge which is a runtime specific for the edge scenario. It leverages the moduler design of the ONNX Runtime and the ONNX Runtime for Edge will also be built upon the base of ONNX Runtime. More details will be discussed in the following section.

We are open to any discussion about ONNX edge, we will appreciate if you have any more issues/ideas or solutions. You can either edit in this doc or talk in the Gitter channel of Edge.


## Ultimate Goal

By definition, ONNX is an open specification that consists of the following components:

1. A definition of an extensible computation graph model.

2. Definitions of standard data types.

3. Definitions of built-in operators.

so, we should strive for complete support for ONNX model to run on edge device with:

1. The computation graph of ONNX model that is compatible with Edge device with relatively small size
Specific data types that used on edge device

2. Presumably low bits data types that define the input and output
Low-precision operators

3. The community seems no to be very interested in adding low-precision ops. Meanwhile it is more a vendor-specific problem than a consensus low-precision op set, custom low-precision op is another option for all the vendors

## Scenario Coverage

Right now most edge/mobile devices are doing the following things:

### Image processing

Face recognition, license plate recognition and gesture recognition technologies are widely used in a smart city scenario. Based on traditional image classification, Object detection and image segmentation models can we build the specific app to solve the problem. OCR for id card/ postcard or any card is also another way to use our image processing technology. We can leverage the ONNX model zoo, a collection of pre-trained state-of-the-art models in deep learning, available in the ONNX format, to help us build the app. Many powerful models like ResNet101, VGG-SSD are already collected in ONNX model zoo, but accuracy, size are the problems we must face against.

### Video Processing

Combining with the Image processing and video processing technology, traffic control, video analysis for security or other video processing scenario will be covered. Facility inspection is also a use case if we mount our edge device on a drone. The capability of multi-channel (HD) videos processing will be key to the performance of the edge device, while speed and latency are two problems that users concerned with.

### Natrual Language Processing

Modern NLP (Natural Language Processing) is an important domain in which deep learning is applied especially in Edge. NLP in ONNX: A Strategy Proposal [1] is already proposed to the ONNX community.


More other scenarios and use cases are welcomed here, feel free to add.

## Challenges

### Accuracy

The ONNX model zoo collected many wide-used models for image classification, face recognition and image segmentation. While the accuracy number varies, the top-5 accuracy seems acceptable with VGG, resent and mobile net are all above or close to 90%. If put these models in edge device in the future, how to keep the accuracy still in a decent level while compressing the model and changing ops to low-bit version? There are some discussion in the quantization Gitter  channel where further detailed work can be achieved cooperating with the quantization WG.

### Size

In ONNX 1.4 release, support for large models (larger than 2GB) and store the data externally is added as a new feature. But in edge device, obviously we do not want such huge models running and consuming the precious memory. The problem is that how should we compress our model while keeping the accuracy? There are some papers we can refer to: Universal Deep Neural Network Compression [2] (thanks to @Danilo Pau sharing the information) on resNet32, 47.36 compression factor and only 0.5% loss of accuracy. There are also plenty of papers that demonstrates that by carefully quantizing to ternary bit width a net keep accuracy with dramatic hw simplification, eg. Ternary Neural Networks for Resource-Efficient AI Applications [3], so it is our job to talk about the approach we should use and compress our model.

### Speed

In many scenarios, fast processing speed and low latency are required. Vendor-specific runtime optimization are encouraged while we should also keep our optimization work going.

### Power consumption

This is a field that we rarely talked about, but power consumption is critical for an edge device. MLPerf community is a broad ML benchmark suite for measuring performance of ML software frameworks, ML hardware accelerators, and ML cloud platforms. In MLPerf Edge Inference WG, power consumption is outlined as a metrics to be measured thus I suggest that our community can cooperate with MLPerf community to improve our power consumption performance. MLPerf Edge Inference Power/Energy [4] is the official document of MLPerf on how to handle the measurement and benchmarking for the power/ energy consumption. I suggest we look into the doc and cooperate with the MLPerf community to improve our power/ energy consumption performance based on the Spec mentioned.


## ONNX Runtime for Edge

The runtime for Edge devices differs from the runtime for data centers. In edge scenario, HW-related optimization (eg. quantization) is defined by vendors in the lower level, as a result, it is hard to unify while the graph optimization can be unified if there is a runtime specifically for Edge devices to run ONNX model. It also helps covering all scenarios with ONNX Runtime. 

We propose ONNX Runtime for Edge which is based on the ONNX Runtime. It is a moduler design where graph optimization (eg. constant folding) is separated from HW-related optimization (eg. quantization), see Huawei ONNX Runtime For Edge Proposal ( https://docs.google.com/presentation/d/1UZrEHY_7AQYUXXRs1q4_FTKsS1KRuGMXzg0Vq7P5uBc/edit?ts=5cb0051a#slide=id.g50dabc0fb2_0_107 ) for more details.

We are currently working on this proposal and collecting opinions from the community. In order to push this project forward, we plan to work together with Microsoft to work on the original ONNX Runtime including implementation of graph optimization, maintainance of individual EP etc. It is a long term effort from all contributors and vendors, and we are now open to your opinions.

## Deliverables

The deliverable consists two parts: documentation and code. The analysis document itself could be one of the deliverables alongside other possible docuementations. We could also expect some code implementation regarding ONNX Runtime For Edge proposal on edge configuration in correspoding to the scenario definition and analysis.

## Cooperation with other WG

Two of the three components in our design of the ONNX Edge are tightly connected with the work from the quantization WG. It is important for Edge WG to work together with the quantization WG

Three topics we’ve covered in quantization WG:
* Input/Output type specification update for quantize ops.
* Quantized data (weights) representation. (say, min/max or min/scale representation).
* Quantize OPs (including Quantize/Dequantize and other existing ONNX ops' quantization version)

In order to complete the ONNX Edge work, those topics should be more detailed and implemented based on the result. We’d like to see more suggestions in the quantization part and contribute to push the low-precision ops into the op list.

## References

[1]. NLP in ONNX: A Strategy Proposal: https://github.com/onnx/onnx/wiki/NLP-in-ONNX:-A-Strategy-Proposal

[2]. Universal Deep Neural Network Compression: https://arxiv.org/abs/1802.02271

[3]. Ternary Neural Networks for Resource-Efficient AI Applications: https://arxiv.org/abs/1609.00222 

[4]. MLPerf Edge Inference Power/Energy: https://docs.google.com/document/d/1XdX5-PHFuckeZYUJpEupvOgPmn_wmOHPY3JLP8-fjLs/edit#heading=h.7muvnvqgd1ss or https://docs.google.com/document/d/15BY2nYZYU2O-1sfppy544clwuT3dRJ6hxI0NdvkY8Lg/edit?usp=sharing in case you are not a member of the MLPerf community
