cmake_minimum_required(VERSION 3.14)
project(genai_interfaces LANGUAGES CXX)

# Define header-only interface library
add_library(genai_interfaces INTERFACE)

# Include directories for consumers (both build and install)
target_include_directories(genai_interfaces INTERFACE
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>
)

include(CMakePackageConfigHelpers)

# Write version file
write_basic_package_version_file(
    "${CMAKE_CURRENT_BINARY_DIR}/genai_interfacesConfigVersion.cmake"
    VERSION 1.0.0
    COMPATIBILITY AnyNewerVersion
)

# Write package configuration file
configure_package_config_file(
    "${CMAKE_CURRENT_SOURCE_DIR}/genai_interfacesConfig.cmake.in"
    "${CMAKE_CURRENT_BINARY_DIR}/genai_interfacesConfig.cmake"
    INSTALL_DESTINATION lib/cmake/genai_interfaces
)

# Install headers
install(
    DIRECTORY include/
    DESTINATION include
)

# Install the target + export set
install(
    TARGETS genai_interfaces
    EXPORT genai_interfacesTargets
)

# Install export set
install(
    EXPORT genai_interfacesTargets
    FILE genai_interfacesTargets.cmake
    NAMESPACE genai_interfaces::
    DESTINATION lib/cmake/genai_interfaces
)

# Install configuration files
install(
    FILES
        "${CMAKE_CURRENT_BINARY_DIR}/genai_interfacesConfig.cmake"
        "${CMAKE_CURRENT_BINARY_DIR}/genai_interfacesConfigVersion.cmake"
    DESTINATION lib/cmake/genai_interfaces
)
