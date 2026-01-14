# Makefile for libvector

.PHONY: all prove update doc lib clean

all: prove doc lib
	@echo "------------------------------------------"

prove:
	@echo "------------------------------------------"
	@echo "--- Proofs"
	@echo "------------------------------------------"
	@why3find prove *.mlw -l

update:
	why3find prove *.mlw -l -s -m -x

doc:
	@echo "------------------------------------------"
	@echo "--- Documentation"
	@echo "------------------------------------------"
	@rm -fr html
	@why3find doc *.mlw -t "Tensor Library"

EXTRACT=-D c -D cdriver.drv -L . --modular --interface -o lib

lib:
	@echo "------------------------------------------"
	@echo "--- Extraction"
	@echo "------------------------------------------"
	@rm -fr lib
	@why3 extract $(EXTRACT) libvector.CIndex
	@cd lib && gcc -c *.c
	@find lib -type f

clean:
	rm -fr lib html
