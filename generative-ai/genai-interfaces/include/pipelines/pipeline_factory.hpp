#ifndef PIPELINE_FACTORY_HPP
#define PIPELINE_FACTORY_HPP

#include <functional>
#include <map>
#include <stdexcept>
#include <filesystem>

#include "pipelines/text2text_pipeline.hpp"
#include "pipelines/text2image_pipeline.hpp"

namespace onnx::genai {

// A function pointer type for creating a pipeline instance.
using PipelineText2TextCreator = std::function<std::shared_ptr<onnx::genai::Text2Text::Pipeline>(const std::filesystem::path& models_path, const std::vector<Device> devices)>;
using PipelineText2ImageCreator = std::function<std::shared_ptr<onnx::genai::Text2Image::Pipeline>(const std::filesystem::path& models_path, const std::vector<Device> devices)>;


class Text2TextPipelineFactory {
public:
    static Text2TextPipelineFactory& GetInstance() {
        static Text2TextPipelineFactory instance;
        return instance;
    }

    void Register(const std::string& name, PipelineText2TextCreator creator) {
        m_creators[name] = creator;
    }

    std::shared_ptr<onnx::genai::Text2Text::Pipeline> Create(
        const std::string& name,
        const std::filesystem::path& models_path,
        const std::vector<Device> devices) {

        auto it = m_creators.find(name);
        if (it == m_creators.end()) {
            throw std::runtime_error("Unregistered GenAI framework: " + name);
        }
        return it->second(models_path, devices); // Call the registered creator function.
    }

private:
    Text2TextPipelineFactory() = default;
    std::map<std::string, PipelineText2TextCreator> m_creators;
};


class Text2ImagePipelineFactory {
public:
    static Text2ImagePipelineFactory& GetInstance() {
        static Text2ImagePipelineFactory instance;
        return instance;
    }

    void Register(const std::string& name, PipelineText2ImageCreator creator) {
        m_creators[name] = creator;
    }

    std::shared_ptr<onnx::genai::Text2Image::Pipeline> Create(
        const std::string& name,
        const std::filesystem::path& models_path,
        const std::vector<Device> devices) {

        auto it = m_creators.find(name);
        if (it == m_creators.end()) {
            throw std::runtime_error("Unregistered GenAI framework: " + name);
        }
        return it->second(models_path, devices); // Call the registered creator function.
    }

private:
    Text2ImagePipelineFactory() = default;
    std::map<std::string, PipelineText2ImageCreator> m_creators;
};

} // namespace onnx::genai

#endif // PIPELINE_FACTORY_HPP
