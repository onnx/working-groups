.PHONY: all prove doc lib test clean

all: prove doc lib

prove:
	why3find prove -l -x

doc:
	why3find doc -t ONNX *.mlw

lib:
	@rm -f lib/*__*.ml lib/*.bak
	why3 extract -D ocaml64 -o lib --modular -L . -D tensor.drv sequence.Seq
	why3 extract -D ocaml64 -o lib --modular -L . -D tensor.drv tensor.Shape
	why3 extract -D ocaml64 -o lib --modular -L . -D tensor.drv tensor.Tensor
	why3 extract -D ocaml64 -o lib --modular -L . -D tensor.drv opwhere.Where
	@rm -f lib/*.bak
	dune build

test:
	@dune build
	@_build/default/test/test.exe

clean:
	rm -fr lib/*.ml html
