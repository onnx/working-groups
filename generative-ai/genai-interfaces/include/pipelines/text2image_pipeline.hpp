#ifndef TEXT2IMAGE_PIPELINE_HPP
#define TEXT2IMAGE_PIPELINE_HPP

#include <string>
#include <set>
#include <map>
#include <any>
#include <array>
#include "pipelines/device_factory.hpp"

namespace onnx::genai::Text2Image {

struct Tensor {
    void* data;
    size_t byte_size;
    std::vector<size_t> shape;
};


struct GenerationInput {
    std::string text;

    GenerationInput(std::string text) {
        this->text = text;
    }
};


struct GenerationResult {
    Tensor tensor;
};


struct GenerationConfig
{
    size_t image_width;
    size_t image_height;
    size_t num_inference_steps;
    size_t num_images_per_prompt;
};


class Generator {
public:
    virtual ~Generator() = default;
    virtual bool IsDone() const = 0;
};


class Pipeline {
public:
    virtual ~Pipeline() = default;

    virtual GenerationResult operator()(const GenerationInput& input) = 0;
    virtual GenerationConfig get_generation_config() const = 0;
    virtual void set_generation_config(const GenerationConfig& config) = 0;
};

} // namespace onnx::genai::Text2Image

#endif // TEXT2IMAGE_PIPELINE_HPP
