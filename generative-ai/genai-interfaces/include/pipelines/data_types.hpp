#ifndef DATA_TYPES_HPP
#define DATA_TYPES_HPP

#include <vector>
#include <string>


namespace onnx::genai {

    struct Tensor {
        void* data;
        std::vector<size_t> shape;
        size_t type_id;
        std::string framework_id;
    };

} // namespace onnx::genai

#endif // DATA_TYPES_HPP
