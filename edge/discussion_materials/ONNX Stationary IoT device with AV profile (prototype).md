# ONNX Stationary IoT device with AV profile (prototype)
Author: Ofer Rosenberg

Version: 0.1

## Introduction

*This document is a prototyping effort to describe a profile using the method and definitions provided in "ONNX Edge scope and profile definition"*

The profile described in this document is of a stationary IoT device with Audio/Video interface (input and output). 
The family of edge devices covered by this profile are devices which remain in the same location (fixed to a wall, lying on a table, etc), constantly connected to the web (wired ro wireless) and have audio and video interfaces - inputs, outputs or both.
The next section provides a few examples for devices which fit into this profile. 


## Profile Examples 
Here are a few examples for devices which fit this profile :

 1. IP Security Camera : This is an IoT device which is stationary, usually fixed to a wall or placed in some fixed location. It has a video input, which may range from low-resolution to 4K images, and possibly an audio input. It also has web connectivity, used to report on events and sometimes send video sections or still images. It is constantly connected to a power source. In terms of processing, it usually processes the AV information on the device, to ensure low latency of event detection.   
 2. Smart Speaker : This is an IoT device which usually located on some table of shelf, has audio inputs and outputs, and has web connectivity (wired or wireless). It may be connected to a power source or runs on batteries. In terms of processing, it usually uses a hybrid model, where some preliminary processing runs on the device, and the rest runs in the cloud. 
 3. Smart Display : Similar to a smart speaker, but has a video display and a camera. In terms of connectivity, power supply and processing model, similar to the smart speaker. 


## Profile attributes
This sections describes the attribute values for Stationary IoT device with AV profile, referred in this section in short as "the device" 

### 1. Accuracy

The ONNX model zoo collects many wide-used neural network models, for use cases such as image classification, object detection, face recognition, image segmentation, etc. While the accuracy number varies, the top-5 accuracy seems acceptable in many cases; e.g. VGG, Resnet and MobileNet models all have top-5 accuracy above or close to 90%. Acceptable accuracy is very much use case or scenario dependent. Accuracy is critical for scenarios like smart city, face recognition and smart camera. Challenge in deploying these models on an edge device is to keep the accuracy still at acceptable level while employing various techniques to reduce model's computational complexity and size (e.g. via model compression or low-bit integer math computation).

### 2. Size

 The device should have at least 2GB of DRAM memory, and free 8GB of Storage room (as flash drive or else)

### 3. Latency

In case of a Video input, the device should be able to process any of the defined classification networks in less than 33mSec (fitting 30FPS rate). 
In case of Audio input, the device should process the RNN based networks in less than 20mSec

### 4. Power consumption

The device would be limited to a power consumption of 5W. The expectation is to have 60% of the use cases consume 3W or less. 


### 5. Data locality
The following set of video classification models are required to be supported fully on device, due to latency & privacy requirements :

 - List TBD
 The following set of audio models are expected to run in hybrid mode, where only part of the model run on the device :
 
 - List TBD

## Required Networks
This section covers a list of networks required to be supported by the device

### Inception v3
TBD
### MobileNet v2
TBD

## ONNX Operations 
TBD