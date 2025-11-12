# Directory Structure

This repository contains both formal and informal specifications for operators and graph, documentation, tests, and verification tools for various operators. The project is organized as follows:

## General Structure

```plaintext
sonnx/
├── ops/
│   ├── spec/
│   │   ├── informal/
│   │   │   ├── common
│   │   │   ├── add/
│   │   │   │   ├── assets
│   │   │   │   ├── reviews
│   │   │   │   ├── tests
│   │   │   │   └── README.md
│   │   │   ├── conv
│   │   │   └── ...
│   │   └── formal/
│   │       ├── common/
│   │       │   ├── libs
│   │       │   └── Makefile
│   │       ├── add
│   │       ├── conv
│   │       └── ...
│   ├── code/
│   │   ├── common/
│   │   │   ├── drivers
│   │   │   ├── Makefile
│   │   │   └── libs
│   │   ├── add/
│   │   │   ├── generated_code/
│   │   │   │   ├── ocaml_code
│   │   │   │   └── c_code
│   │   │   ├── generated_doc
│   │   │   └── tests
│   │   ├── conv
│   │   └── ...
│   └── docs/
│       ├── guidelines
│       └── tensor_lib

└── graph
```
## Main content 
- **Informal specification** [Link](ops/spec/informal/) 
- **Formal specification** [Link](ops/spec/formal/) 
- **Guidelines to informal and formal specification** [Link](ops/docs/guidelines/)
- **Code and documentation generated from Why3** [Link](ops/code/)
- **Why3 installation guide** [Link](ops/docs/installation/)
- **Informal specification template** [Link](ops/spec/informal/common/template.md)
- **Tensor library formal specification** [Link](ops/spec/formal/common/libs/tensor/)
- **Tensor library documentation** [Link](ops/docs/tensor_lib/)
