# ONNX Formal Methods

To install the tool-chain:

    $ apt-get opam
    $ opam install why3find alt-ergo

To install the VSCode extension:

    $ wget https://git.frama-c.com/pub/why3find/-/jobs/1177337/artifacts/raw/vscode/why3-platform-1.1.1.vsix
    $ code --install-extension why3-platform-1.1.1.vsix

Documentation:

- [Why3](https://www.why3.org)
- [Why3 Manual](https://www.why3.org/doc/)
- [Why3 Standard Library](https://www.why3.org/stdlib/)
- [Why3find](https://git.frama-c.com/pub/why3find)

# Proving

    $ make prove
    why3find prove -l -x
    Theory opwhere.FlatWhere: ✔ (-)
    Theory opwhere.Where: ✔ (2)
    Theory utils.Product: ✔ (2)
    Theory tensor.FlatTensor: ✔ (14)
    Theory tensor.Tensor: ✔ (1)
    Theory sequence.Seq: ✔ (24)
    Theory sequence.Codomain: ✔ (6)
    Cache 53/53
    Proofs ✔ (49) (unchanged)
    Provers 691ms, depth: 3
    - alt-ergo@2.5.4       (  49) ( 12ms -  44ms - 691ms)
    - split_vc             (   8)

# Documentation

    $ make doc
    why3find doc *.mlw
    Generated /Users/correnson/onnx/html/index.html

# Extraction & Test

    $ make lib   # extract and compile the lib
    $ make test  # compile and execute the tests

The OCaml extracted code from Why3 is in the `lib` directory, which also contains
hand-written files:

 - `lib/dune` OCaml compilation directives
 - `lib/tensor.mli` Public API of the Tensor library
 - `lib/tensor.ml` Bindings of the public API to the extracted code
 - `lib/extract/*.ml` Extracted code from Why3 specifications

The unit tests are written in OCaml in `test` directory:

 - `test/dune` OCaml compilation directives
 - `test/test.ml` OCaml unit tests using the Tensor library
