.PHONY: all prove doc lib test clean

all: prove doc lib

prove:
	why3find prove -l -x

doc:
	why3find doc -t ONNX *.mlw

lib:
	@mkdir -p lib/extract
	@rm -fr lib/extract/*
	why3 extract -D ocaml64 -o lib/extract --modular -L . -D tensor.drv sequence.Seq
	why3 extract -D ocaml64 -o lib/extract --modular -L . -D tensor.drv tensor.Shape
	why3 extract -D ocaml64 -o lib/extract --modular -L . -D tensor.drv tensor.Index
	why3 extract -D ocaml64 -o lib/extract --modular -L . -D tensor.drv tensor.Tensor
	why3 extract -D ocaml64 -o lib/extract --modular -L . -D tensor.drv opwhere.Where
	why3 extract -D ocaml64 -o lib/extract --modular -L . -D tensor.drv opmatrix.Matrix
	dune build

test:
	@dune runtest

clean:
	rm -fr lib/*.ml html
