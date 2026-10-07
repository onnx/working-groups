# Makefile for libvector

.PHONY: all prove update doc lib cc clean

all: prove doc lib
	@echo "------------------------------------------"

prove:
	@echo "------------------------------------------"
	@echo "--- Proofs"
	@echo "------------------------------------------"
	@why3find prove *.mlw -l -s -x

update:
	why3find prove *.mlw -l -s -x -m

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
	@why3 extract $(EXTRACT) libtensor.CTensor
	@cd lib && gcc -c *.c
	@find lib -type f | sort

clean:
	rm -fr lib html