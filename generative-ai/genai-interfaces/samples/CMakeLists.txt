cmake_minimum_required(VERSION 3.18.1)

project(genai_chat_sample)
set(CMAKE_CXX_STANDARD 20)

if(USE_CXX)
  add_compile_definitions(USE_CXX)
endif()



if( OVGENAI )
   message("building for OpenVINO GenAI")

   find_package(genai_interfaces REQUIRED)
   find_package(OpenVINOGenAI REQUIRED)

   add_executable(chat_sample chat_sample.cpp)

   target_link_libraries(chat_sample PUBLIC openvino::genai genai_interfaces::genai_interfaces)

   target_compile_definitions(chat_sample PRIVATE USE_OPENVINO_GENAI=1)

else()
    message("building for ORT GenAI")
    set(ORT_GENAI_LIB_DIR ${CMAKE_SOURCE_DIR}/ort_genai/lib)

	if(WIN32)
	  set(ONNXRUNTIME_GENAI_LIB "onnxruntime-genai.dll")
	  set(ONNXRUNTIME_GENAI_DEPENDENCY "*.dll")
	elseif(APPLE)
	  set(ONNXRUNTIME_GENAI_LIB "libonnxruntime-genai.dylib")
	  set(ONNXRUNTIME_GENAI_DEPENDENCY "*.dylib")
	elseif(CMAKE_SYSTEM_NAME MATCHES "AIX")
	  set(ONNXRUNTIME_GENAI_LIB "libonnxruntime-genai.a")
	  set(ONNXRUNTIME_GENAI_DEPENDENCY "*.a")
	else()
	  set(ONNXRUNTIME_GENAI_LIB "libonnxruntime-genai.so")
	  set(ONNXRUNTIME_GENAI_DEPENDENCY "*.so")
	endif()

	file(GLOB ort_genai_libs "${CMAKE_SOURCE_DIR}/ort_genai/lib/${ONNXRUNTIME_GENAI_DEPENDENCY}")

    add_executable(chat_sample chat_sample.cpp)

	# add link/include dirs for ORT GenAI
	target_link_directories(chat_sample PRIVATE ${ORT_GENAI_LIB_DIR})
	target_link_libraries(chat_sample PRIVATE ${ONNXRUNTIME_GENAI_LIB})
	target_include_directories(chat_sample PRIVATE ${CMAKE_SOURCE_DIR}/ort_genai/include)

	target_link_libraries(chat_sample PUBLIC onnxruntime-genai)

	target_compile_definitions(chat_sample PRIVATE USE_ONNXRUNTIME_GENAI=1)

	foreach(DLL_FILE ${ort_genai_libs})
		add_custom_command(
		  TARGET chat_sample POST_BUILD
		  COMMAND ${CMAKE_COMMAND} -E copy_if_different ${DLL_FILE} $<TARGET_FILE_DIR:chat_sample>
		)
	endforeach()
endif()
