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
