# Copyright (C) 2023-2025 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
cmake_minimum_required(VERSION 3.18.1)

project(text2image_sample)
set(CMAKE_CXX_STANDARD 20)

if(USE_CXX)
  add_compile_definitions(USE_CXX)
endif()

if(POLICY CMP0135)
    cmake_policy(SET CMP0135 NEW)
endif()

find_package(genai_interfaces REQUIRED)
find_package(OpenVINOGenAI REQUIRED)

add_executable(text2image text2image.cpp imwrite.cpp)
target_include_directories(text2image PRIVATE genai_interfaces::genai_interfaces)
target_link_libraries(text2image PRIVATE openvino::genai genai_interfaces::genai_interfaces)
target_compile_definitions(text2image PRIVATE USE_OPENVINO_GENAI=1)
