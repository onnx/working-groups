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
- [Informal specification](ops/spec/informal/) 
- [Formal specification](ops/spec/formal/) 
- [Guidelines](ops/docs/guidelines/) 
  - to [write informal specifications](./ops/docs/guidelines/informal.md)
  - to write formal specifications (TBC)
  - to write tests (TBC)
  - [to manage the items's lifecycle](./ops/docs/guidelines/lifecycle.md)
- [Code and documentation generated from Why3](ops/code/)
- [Why3 installation guide](ops/docs/installation/)
- [Informal specification template](ops/spec/informal/common/template.md)
- [Tensor library formal specification](ops/spec/formal/common/libs/tensor/)
- [Tensor library documentation](ops/docs/tensor_lib/)
