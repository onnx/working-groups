#ifndef TEXT2TEXT_PIPELINE_HPP
#define TEXT2TEXT_PIPELINE_HPP

#include <string>
#include <memory>
#include <pipelines/generation_config.hpp>

namespace onnx::genai {

struct GenerationResult {
    std::string text;
};

class Text2TextPipeline {
public:
    virtual ~Text2TextPipeline() = default;

    virtual GenerationResult operator()(const std::string& input) = 0;

    virtual GenerationConfig get_generation_config() const = 0;
    virtual void set_generation_config(const GenerationConfig& config) = 0;
};

} // namespace onnx::genai

#endif // TEXT2TEXT_PIPELINE_HPP
