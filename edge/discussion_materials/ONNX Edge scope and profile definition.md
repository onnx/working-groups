# ONNX Edge scope and profile definition
Author: Yedong Liu, Milan Oljaca, Saurabh Tangri, Ofer Rosenberg

Version: 0.1

## Motivation

The following document provides a description of terminology related to "edge" : what is the scope of "edge", what are the scenarios, example of devices which map into the edge, and more. The goal is to define elements that identify an edge profile, based on attributes.

The next step would be using these definitions to create a per profile document which contains: the definition of a profile, scenario/s which are relevant to this profile, scenario mapping to list of ONNX models (and hence derived ONNX operators).

## Scope of Edge

<p align="center">
	<img src="Scope of Edge.png" width="65%"/>
</p>

Broadly speaking, scope of edge can be defined as "not cloud". Edge computing is computing that’s done at or near the source of the data, without relying on the cloud computing resources in data centers. Edge computation is largely or completely performed on distributed edge devices. The consumer of edge computing is any application or general functionality needing to be closer to the source of the action where system can process and interact with the real world instantly.

## Edge scenario

Doing the computing at the edge may be due to various reasons - need for real-time, privacy, latency, connectivity and more. A few examples for edge usage scenarios there are: face recognition, smart assistant, smart city, intelligent traffic control, industrial IoT, video analysis and monitoring, autonomous cars and smart drones.

Edge computing requirements are highly scenario dependent.

In one of the scenarios, specifically for IoT devices, data comes in from the physical world via various sensors, and actions are taken to change physical state via various forms of output; by performing analytics and generating output directly at the site, communications bandwidth between edge and cloud is reduced. Edge computing takes advantage of proximity to the physical items of interest and also exploits the relationships those items may have to each other.

In another scenario which requires low latency like autonomous driving cars. A notable applications include online gaming. Game servers are running in the cloud and the rendered video is transferred to lightweight clients such as AR devices (mobile phone), VR glasses, etc. Conventional cloud games may suffer from high latency and insufficient bandwidth. As real-time games have strict constraints on latency, processing game simulation at the edge node is necessary for the immersive game plays.


## Edge device

An edge device is a device which has the capability to connect to the internet or to a private network/data-center/cloud or connected to other smart devices to share the workload of a certain scenario. Examples include routers, routing switches, terminals, mobile phones, IoT devices, autonomous cars, etc. In those cases, edge devices provide connections into carrier and internet service provider networks. An edge device doesn't need to be at connected state at all time, like mobile phones and smart cameras which can still work at offline state, but sharing of these data requires connectivity between those devices.

## ONNX Edge profiles

The ONNX Edge profile is described with the following:

1. Attributes / characteristics, such as power consumption, memory size, accuracy, latency, etc.

2. ONNX operations subset

3. Other ONNX related limitations 

Defining a strict subsets of the operators which apply to edge device profiles is important and relevant due to limitations imposed with computational complexity and device capabilities. Use-cases not applicable to the edge (e.g. large scale training scenarios) need to be excluded.

### Edge profile attributes

In computing, there are always compromises to be made, such as latency vs power or memory utilization. Computing at the edge is no exception. We can think of edge profile attributes as dimensions along which trade-offs are being made in edge scenarios.

<p align="center">
	<img src="Edge scenario radar chart.png" width="50%"/>
</p>

#### 1. Accuracy

The ONNX model zoo collects many wide-used neural network models, for use cases such as image classification, object detection, face recognition, image segmentation, etc. While the accuracy number varies, the top-5 accuracy seems acceptable in many cases; e.g. VGG, Resnet and MobileNet models all have top-5 accuracy above or close to 90%. Acceptable accuracy is very much use case or scenario dependent. Accuracy is critical for scenarios like smart city, face recognition and smart camera. Challenge in deploying these models on an edge device is to keep the accuracy still at acceptable level while employing various techniques to reduce model's computational complexity and size (e.g. via model compression or low-bit integer math computation).

#### 2. Size

Size here refers to both the neural network's on-disk storage size and the memory that the runtime reqiures to run the inference. In ONNX 1.4 release, support for large models (larger than 2GB) and store the data externally is added as a new feature. But in edge devices, such huge models are usually not practical due to memory resource constraints. There are ways to reduce size of neural network models while keeping the accuracy, like using quantized operators, model compression etc. 

#### 3. Latency

In many scenarios, fast processing speed and low latency are required. Optimizations are always encouraged, either through vendor-specific runtime optimizations or general neural network and operator optimizations. Optimizing processing speed overlaps with optimizations in data bandwidth, since a broader data bandwidth usually provide less latency thus improving overall processing speed.

#### 4. Power consumption

Power consumption is important and often critical for an edge device. In this context, inferences/second/watt metric is often used. There are ways to reduce the power consumption and extend the service time of edge device while maintaining the same level of performance, e.g.:

1. A larger battery which extend the servie time of an edge device.

2. A better chipset which utilized with more advanced algorithms and techniques yields lower power consumption.

3. New scheduling system to switch off some unused applications or hardware parts

4. Better more efficient cooling system 

5. etc. 


#### 5. Data locality

Data locality is tightly connected with data privacy and security aspects of a scenario. In some cases keeping data local on device is a must. It is also possible to have a local on edge device neural network and to send the data to the cloud for further processing or for storage. With faster cellular communication technology advancements, such as 5G, it is likely that future IoT devices will heavily depend on it. In such cases and depending on the application, in particular on the required data type and format, it is up to the developer to select the best data transmission technology.
Security attacks target connected sensor nodes and personal devices to collect privacy data, which could be used for analysis purposes or to profile users. In such cases, encryption techniques and cryptography may be needed in edge devices to improve data transmission security.
