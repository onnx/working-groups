# ONNX Edge scope and profile definition
Author: Yedong Liu, Milan Oljaca, Saurabh Tangri, Ofer Rosenberg

## Motivation

The following document provides a description of terminology related to "edge" : what is the scope of "edge", what are the scenarios, example to devices which map into the edge, and more. The goal is to define what is contained inside an edge profile , based on attributes.

The next step would be using these definitions to create a per profile document which contains: the definition of a profile, scenario/s which are relevant to this profile, scenario mapping to list of ONNX models (and hence derived ONNX operators).

## Scope of Edge

Broadly speaking, scope of edge can be defined as "not cloud". Edge computing is computing that’s done at or near the source of the data, without relying on the cloud computing resources in data centers. Edge computation is largely or completely performed on distributed edge devices. The consumer of edge computing is any application or general functionality needing to be closer to the source of the action where system can process and interact with the real world instantly.

## Edge scenario

Doing the computing at the edge may be due to various reasons - need for real-time, privacy, latency, connectivity and more. A few examples for edge usage scenarios there are: face recognition, smart assistant, smart city, intelligent traffic control, industrial IoT, video analysis and monitoring, border control, unattended shops, autonomous cars and smart drones.

Edge computing requirements are highly scenario dependent.

In one of the scenarios, specifically for IoT devices, data comes in from the physical world via various sensors, and actions are taken to change physical state via various forms of output; by performing analytics and generating output directly at the site, communications bandwidth between edge and cloud is reduced. Edge computing takes advantage of proximity to the physical items of interest and also exploits the relationships those items may have to each other.

In another scenario which requires low latency like auto pilot cars. A notable applications include online gaming. Game servers are running in the cloud and the rendered video is transferred to lightweight clients such as AR devices (mobile phone), VR glasses, etc. Conventional cloud games may suffer from high latency and insufficient bandwidth. As real-time games have strict constraints on latency, processing game simulation at the edge node is necessary for the immersive game plays.


## Edge device

An edge device is a device which has the capability to connect to the internet or to a private network/data-center/cloud or connected to other smart devices to share the workload of a certain scenario. Examples include routers, routing switches, terminals, mobile phones, IoT devices, autonomous cars, etc. In those cases, edge devices provide connections into carrier and internet service provider networks. An edge device doesn't need to be at connected state at all time, like mobile phones and smart cameras which can still work at offline state, but sharing of these data requires connectivity between those devices.

## ONNX Edge profiles

The ONNX Edge profile is described with the following:

1. Attributes / characteristics, such as power consumption, memory size, accuracy, latency, etc.

2. ONNX operations subset

3. Other ONNX related limitations 

Work to define strict subsets of the operator sets which apply to edge devices which avoid complex operations imposed by limitations on edge devices with high computational complexity. Exclude use-cases not applicable to the edge (e.g. large scale training scenarios)


### Edge profile attributes

In computing, there are always compromises to be made, such as latency vs power or memory utilization. Computing at the edge is no exception. We can think of edge profile attributes as dimensions along which trade-offs are being made in edge scenarios.

#### Accuracy

The ONNX model zoo collected many wide-used models for image classification, face recognition and image segmentation. While the accuracy number varies, the top-5 accuracy seems acceptable with VGG, resent and mobile net are all above or close to 90%. Accuracy is critical for scenarios like smart city, face recognition and smart monitoring. If put these models in edge device in actual use, primary work is to keep the accuracy still in a decent level while compressing the model and changing ops to low-bit version.

#### Size

Size here refers to both the model on-disk storage size and the memory that the runtime reqiures to run the inference. In ONNX 1.4 release, support for large models (larger than 2GB) and store the data externally is added as a new feature. But in edge device, we do not want such huge models running and consuming the precious memory. There are many ways to compress our models while keeping the accuracy like changing to quantized ops, model compression etc. 

#### Latency

In many scenarios, fast processing speed and low latency are required. Vendor-specific runtime optimization are encouraged while we should also keep our optimization work going. works on the speed over laps with some of the work on the bandwidth, since a broader bandwidth always provide less latency thus improving overall speed.

#### Power consumption

Power consumption is critical for an edge device. Methods are to be defined to reduce the power consumption/extend the service time of this edge device while maintaining the same level of performance:

1. A larger battery which extend the servie time of an edge device.

2. A better chipset which utilized with more advanced algorithms and technique to lower consumption in every clock time.

3. New scheduling system to switch off some unused applicatio or parts

4. Better cooling system that doesn't consume like the old fashioned fan

5. etc. 


#### Data locality

Data locality is tightly connected with data privacy and security aspects of a scenario. Depending on the application, in particular on the required data type and format, it is up to the developer to select the best transmission technology. Sometimes, it is possible to create a local network and to send the data to the cloud for further processing or for being stored. However, future IoT nodes will heavily depend on cellular communication, e.g. 5G technology.
Attacks can involve sensors nodes to collect privacy data from users, which could be used for analysis purposes or to profile users, or involve in auto pilot cars, healthcare devices (like smart watch) or literally every electrical item that will potentially be equipped with a network access. Thus cryptography is needed for edge devices to improve transmission security. This technique can (and should) be used for blocking the basic IP stealing attempts, and encrypting data for a better security.
